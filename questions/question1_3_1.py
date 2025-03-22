# 1.3.1 Group by candidate and generate summary statistics for each emotion category
import pandas as pd
import numpy as np

# Load data
trump_tweets = pd.read_csv('data/trump_encoded.csv')
clinton_tweets = pd.read_csv('data/clinton_encoded.csv')

# Add candidate column
trump_tweets['candidate'] = 'Donald Trump'
clinton_tweets['candidate'] = 'Hillary Clinton'

# Combine DataFrames
combined_df = pd.concat([trump_tweets, clinton_tweets], ignore_index=True)

# Clean text and perform sentiment analysis
import re

def clean_text(text):
    # Remove mentions (@username) and hashtags (#hashtag)
    text = re.sub(r'@[\w]+', '', text)  # Remove mentions
    text = re.sub(r'#[\w]+', '', text)  # Remove hashtags
    # Remove non-alphabetical characters (punctuation, numbers, etc.)
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Only keep alphabets and spaces
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text

# Load lexicon
nrc_lexicon = pd.read_csv("NRC-Emotion-Lexicon-Wordlevel-v0.92.txt", 
                         sep="\t", 
                         header=None, 
                         names=["word", "emotion", "association"])
nrc_lexicon = nrc_lexicon[nrc_lexicon["association"] == 1].drop(columns=["association"])

def get_sentiment_counts(tweet_text, lexicon):
    # Clean the text
    cleaned_text = clean_text(str(tweet_text))
    
    # Use simple split as the TA confirmed is acceptable
    words = cleaned_text.split()
    
    # Initialize counts for each emotion
    sentiment_counts = {emotion: 0 for emotion in lexicon['emotion'].unique()}
    
    # Count emotions for each word, allowing duplicates
    for word in words:
        # Find matching emotions for this word
        matches = lexicon[lexicon['word'] == word]
        for _, row in matches.iterrows():
            sentiment_counts[row['emotion']] += 1
    
    return sentiment_counts

# First, create a cleaned text column
combined_df['cleaned_text'] = combined_df['text'].apply(clean_text)

# Apply the sentiment analysis function to cleaned text
sentiment_counts = combined_df['cleaned_text'].apply(lambda tweet: get_sentiment_counts(tweet, nrc_lexicon))

# Convert the dictionary of sentiment counts into separate columns
sentiment_df = pd.DataFrame(list(sentiment_counts))

# Merge the sentiment columns with the original DataFrame
merged_df_with_sentiments = pd.concat([combined_df, sentiment_df], axis=1)

# Define emotion categories
emotion_categories = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 
                     'sadness', 'surprise', 'trust', 'positive', 'negative']

# 1.3.1 Group by candidate and generate summary statistics for each emotion
print("1.3.1 Summary statistics for emotions by candidate:")
emotion_stats_by_candidate = merged_df_with_sentiments.groupby('candidate')[emotion_categories].describe()
print(emotion_stats_by_candidate)
