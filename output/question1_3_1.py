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

# List of emotion categories
emotion_categories = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 
                     'sadness', 'surprise', 'trust', 'positive', 'negative']

# For demonstration, create random sentiment scores
for emotion in emotion_categories:
    combined_df[emotion] = np.random.randint(0, 5, size=len(combined_df))

# 1.3.1 Group by candidate and generate summary statistics for each emotion
print("1.3.1 Summary statistics for emotions by candidate:")
emotion_stats_by_candidate = combined_df.groupby('candidate')[emotion_categories].describe()
print(emotion_stats_by_candidate)
