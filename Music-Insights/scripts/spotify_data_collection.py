import requests
import pandas as pd
import time
import logging

# Spotify API endpoints
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'
PLAYLISTS_ENDPOINT = '/browse/categories/{category_id}/playlists'

# Your Spotify API credentials
CLIENT_ID = ''  # your CLIENT_ID
CLIENT_SECRET = ''  # your CLIENT_SECRET

# Directory to save the raw Spotify data
RAW_DATA_DIR = ''  # Directory where you saved the raw Spotify data

# Setting up logging
logging.basicConfig(level=logging.INFO)


def get_api_response(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            # Handle rate limits
            retry_after = int(response.headers.get(
                'Retry-After', 60))  # Default to 60 seconds
            logging.warning(
                f'Rate limit reached. Retrying after {retry_after} seconds.')
            time.sleep(retry_after)
            return get_api_response(url, headers)
        response.raise_for_status()  # Raise an exception for HTTP error codes
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Request failed: {e}')
        return None


# Authenticate and get an access token
auth_url = 'https://accounts.spotify.com/api/token'
auth_data = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
}
auth_response = requests.post(auth_url, data=auth_data)
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

# Define a list of genre categories
genre_categories = ['pop', 'rock', 'hiphop', 'jazz', 'country']

# Iterate through each genre category
for genre in genre_categories:
    # Make a request to get playlists for the genre
    playlist_response = requests.get(
        f'{SPOTIFY_API_BASE_URL}{PLAYLISTS_ENDPOINT.format(category_id=genre)}',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    playlist_data = playlist_response.json()

    # Extract relevant data from the playlist response
    track_data = []
    for playlist in playlist_data.get('playlists', {}).get('items', []):
        if playlist is not None:  # Check if playlist is not None
            playlist_id = playlist.get('id')
            if playlist_id:
                tracks_response = requests.get(
                    f'{SPOTIFY_API_BASE_URL}/playlists/{playlist_id}/tracks',
                    headers={'Authorization': f'Bearer {access_token}'}
                )
                tracks_response_data = tracks_response.json()
                for item in tracks_response_data.get('items', []):
                    track = item.get('track')
                    if track:
                        track_name = track.get('name', '')
                        artist_names = [artist.get('name', '')
                                        for artist in track.get('artists', [])]
                        album_name = track.get('album', {}).get('name', '')
                        track_id = track.get('id', '')

                        if track_name and track_id:  # Ensure that track name and id are present
                            track_data.append({
                                'Track Name': track_name,
                                'Artist Names': ', '.join(artist_names),
                                'Album Name': album_name,
                                'Track ID': track_id,
                            })

    # Create a DataFrame and save it as a CSV file
    df = pd.DataFrame(track_data)
    csv_file_path = f'{RAW_DATA_DIR}top_200_{genre}.csv'
    df.to_csv(csv_file_path, index=False)

print('Data collection completed.')
