import asyncio
import aiohttp
import logging
import pandas as pd
import lyricsgenius

# Spotify API endpoints
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'
PLAYLISTS_ENDPOINT = '/browse/categories/{category_id}/playlists'

# Your Spotify API credentials
CLIENT_ID = ''  # your CLIENT_ID
CLIENT_SECRET = ''  # your CLIENT_SECRET

# Genius API setup
GENIUS_ACCESS_TOKEN = ''  # your GENIUS_ACCESS_TOKEN
genius = lyricsgenius.Genius(
    GENIUS_ACCESS_TOKEN, remove_section_headers=True, timeout=10)

# Directory to save the raw Spotify data
RAW_DATA_DIR = ''  # Directory where you saved the raw Genius data

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


async def get_api_response(session, url, headers):
    async with session.get(url, headers=headers) as response:
        if response.status == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            logging.warning(
                f'Rate limit reached. Retrying after {retry_after} seconds.')
            await asyncio.sleep(retry_after)
            return await get_api_response(session, url, headers)
        response.raise_for_status()
        return await response.json()


async def fetch_playlist_data(session, playlist, access_token):
    if playlist is None:
        return []

    playlist_id = playlist.get('id')
    if not playlist_id:
        return []

    tracks_url = f'{SPOTIFY_API_BASE_URL}/playlists/{playlist_id}/tracks'
    tracks_response_data = await get_api_response(session, tracks_url, headers={'Authorization': f'Bearer {access_token}'})

    if tracks_response_data is None:
        return []

    track_data = []
    for item in tracks_response_data.get('items', []):
        track = item.get('track')
        if track:
            track_name = track.get('name', '')
            artist_names = [artist.get('name', '')
                            for artist in track.get('artists', [])]
            album_name = track.get('album', {}).get('name', '')
            track_id = track.get('id', '')

            # Synchronous call to fetch lyrics
            lyrics = get_lyrics(artist_names[0], track_name)

            track_data.append({
                'Track Name': track_name,
                'Artist Names': ', '.join(artist_names),
                'Album Name': album_name,
                'Track ID': track_id,
                'Lyrics': lyrics
            })

    return track_data

# Function to get lyrics from Genius (synchronous)


def get_lyrics(artist, song):
    try:
        song = genius.search_song(song, artist)
        if song:
            return song.lyrics
    except Exception as e:
        logging.error(f"Error occurred while fetching lyrics: {e}")
    return None


# Define a list of genre categories
# genre_categories = ['pop', 'rock', 'hiphop', 'jazz', 'country']
genre_categories = ['disco']


async def main():
    # Authenticate and get an access token
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    async with aiohttp.ClientSession() as session:
        auth_response = await session.post(auth_url, data=auth_data)
        auth_response_data = await auth_response.json()
        access_token = auth_response_data['access_token']

        for genre in genre_categories:
            try:
                logging.info(f'Processing genre: {genre}')
                playlist_url = f'{SPOTIFY_API_BASE_URL}{PLAYLISTS_ENDPOINT.format(category_id=genre)}'
                playlist_data = await get_api_response(session, playlist_url, headers={'Authorization': f'Bearer {access_token}'})

                if playlist_data is None:
                    logging.warning(f'No data returned for genre: {genre}')
                    continue

                tasks = [fetch_playlist_data(session, playlist, access_token)
                         for playlist in playlist_data.get('playlists', {}).get('items', [])]
                results = await asyncio.gather(*tasks)

                track_data = [item for sublist in results for item in sublist]
                df = pd.DataFrame(track_data)
                csv_file_path = f'{RAW_DATA_DIR}/top_200_{genre}_with_lyrics.csv'
                df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
                logging.info(f'File saved: {csv_file_path}')
            except Exception as e:
                logging.error(f'Error processing genre {genre}: {e}')

asyncio.run(main())
