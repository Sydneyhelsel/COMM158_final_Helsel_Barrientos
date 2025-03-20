# 1.4 Visualizing Results
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

# Calculate mean values for each emotion by candidate
favorites_by_emotion = combined_df.groupby('candidate')[emotion_categories + ['favorite_count']].apply(
    lambda x: pd.Series([
        x[x[emotion] > 0]['favorite_count'].mean() for emotion in emotion_categories
    ], index=emotion_categories)
)

retweets_by_emotion = combined_df.groupby('candidate')[emotion_categories + ['retweet_count']].apply(
    lambda x: pd.Series([
        x[x[emotion] > 0]['retweet_count'].mean() for emotion in emotion_categories
    ], index=emotion_categories)
)

# Create a figure with 2 subplots
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Plot likes by emotion
favorites_by_emotion.T.plot(kind='bar', ax=axes[0])
axes[0].set_title('Average Likes by Emotion Category', fontsize=14)
axes[0].set_xlabel('Emotion Category', fontsize=12)
axes[0].set_ylabel('Average Likes', fontsize=12)
axes[0].tick_params(axis='x', rotation=45)

# Plot retweets by emotion
retweets_by_emotion.T.plot(kind='bar', ax=axes[1])
axes[1].set_title('Average Retweets by Emotion Category', fontsize=14)
axes[1].set_xlabel('Emotion Category', fontsize=12)
axes[1].set_ylabel('Average Retweets', fontsize=12)
axes[1].tick_params(axis='x', rotation=45)

# Adjust layout and save
plt.tight_layout()
plt.savefig('output/emotion_engagement_comparison.png')
print("Visualization completed and saved to output/emotion_engagement_comparison.png")
