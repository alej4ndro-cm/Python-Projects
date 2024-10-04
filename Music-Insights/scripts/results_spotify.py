import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Directory where your CSV files are stored
DATA_DIR = ''  # Directory where you saved the raw Spotify data

# Dictionary to store artist counts per genre
genre_artist_counts = {}

# Process each CSV file in the directory
for filename in os.listdir(DATA_DIR):
    if filename.endswith('.csv'):
        genre = filename.split('_')[2].split(
            '.')[0]  # Extract genre from filename
        file_path = os.path.join(DATA_DIR, filename)
        df = pd.read_csv(file_path)

        # Count occurrences of each artist in this genre
        artists = df['Artist Names'].str.split(', ').explode()
        artist_counts = artists.value_counts()
        genre_artist_counts[genre] = artist_counts

# Plotting top artists for each genre
for genre, counts in genre_artist_counts.items():
    top_artists = counts.head(20)  # Get top 20 artists for this genre

    # Create a WordCloud
    wordcloud = WordCloud(
        width=800, height=400, background_color='white').generate_from_frequencies(counts)

    # Display the WordCloud image
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'Word Cloud for Top Artists in {genre.title()} Genre')
    plt.axis('off')
    plt.show()

print('Word cloud plotting completed.')
