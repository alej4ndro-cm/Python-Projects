import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Define helper functions


def clean_lyrics(lyrics):
    if not isinstance(lyrics, str):
        return ''  # Return an empty string if the input is not a string

    lyrics = lyrics.lower()
    lyrics = re.sub(r'\[.*?\]', '', lyrics)  # Remove text in brackets
    lyrics = re.sub(r'[^\w\s]', '', lyrics)  # Remove punctuation
    # Replace newline characters with space
    lyrics = re.sub(r'\n', ' ', lyrics)
    lyrics = re.sub(r'\d+', '', lyrics)      # Remove numbers
    # Aggressively remove 'na' and its variations
    lyrics = re.sub(r'\bna\b', '', lyrics)   # Remove isolated 'na'
    lyrics = re.sub(r'na+', ' ', lyrics)     # Remove repeated patterns of 'na'

    # Tokenize and remove specific unwanted words or sounds
    unwanted_patterns = {'na', '2018', 'wan', 'tony', 'thy', 'me', 'da', 'gga', 'gon', 'em', 'hes', 'feat', 'ta', 'ah',
                         'ima', 'ooh', 'im', 'like', 'ooh', 'uh', 'ya', 'denzel', 'woo', 'la', 'scott', 'yo', 'vincent',
                         'curry', 'scp', 'thee', 'um', 'que', 'en', 'mme', 'guermantes', 'le', 'uhhuh', 'ft', 'de', 'se',
                         'un', 'por', 'mr', 'la', 'da', 'na na', 'na-na', 'uh huh'}
    for pattern in unwanted_patterns:
        lyrics = re.sub(r'\b' + re.escape(pattern) + r'\b', '', lyrics)

    return lyrics


def word_frequency(lyrics):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(lyrics)
    words = [word for word in words if word not in stop_words and len(
        word) > 1]  # Remove stop words and very short words
    return Counter(words)


# Main script execution
genres = ['pop', 'rock', 'hiphop', 'jazz', 'country']

for genre in genres:
    file_path = f'***Path directory where you saved the raw Spotify data***/top_200_{genre}_with_lyrics.csv'
    try:
        df = pd.read_csv(file_path, encoding='utf-8')

        # Clean and analyze lyrics
        df['clean_lyrics'] = df['Lyrics'].apply(clean_lyrics)
        total_word_count = Counter()
        df['clean_lyrics'].apply(
            lambda lyrics: total_word_count.update(word_frequency(lyrics)))

        # Create and display a word cloud
        wordcloud = WordCloud(
            width=800, height=400, background_color='white').generate_from_frequencies(total_word_count)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Word Cloud for {genre.title()} Genre')
        plt.show()

        # Create and display a bar chart for top N words
        top_n = 20
        top_words = total_word_count.most_common(top_n)
        words, counts = zip(*top_words)
        plt.figure(figsize=(10, 5))
        plt.bar(words, counts)
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.title(
            f'Top {top_n} Most Frequent Words in {genre.title()} Genre Lyrics')
        plt.show()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred while processing {genre} genre: {e}")
