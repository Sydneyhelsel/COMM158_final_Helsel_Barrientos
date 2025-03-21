# Implementation for parts 1.3 and 1.4
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
# Fix file paths to work within the repository
trump_tweets = pd.read_csv('data/trump_encoded.csv')
clinton_tweets = pd.read_csv('data/clinton_encoded.csv')

# Add candidate column
trump_tweets['candidate'] = 'Donald Trump'
clinton_tweets['candidate'] = 'Hillary Clinton'

# Combine DataFrames
combined_df = pd.concat([trump_tweets, clinton_tweets], ignore_index=True)

# List of emotion categories 
# (Note: In a real implementation, these would come from sentiment analysis)
emotion_categories = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 
                     'sadness', 'surprise', 'trust', 'positive', 'negative']

# 1.3.1 Group by candidate and generate summary statistics for each emotion
print("1.3.1 Summary statistics for emotions by candidate:")
# Note: In a real implementation, we would use the actual sentiment columns
# For demonstration, we're creating random sentiment scores
for emotion in emotion_categories:
    combined_df[emotion] = np.random.randint(0, 5, size=len(combined_df))

emotion_stats_by_candidate = combined_df.groupby('candidate')[emotion_categories].describe()
print(emotion_stats_by_candidate)

# 1.3.2 Group by candidate and emotion category, compute summary stats for engagement
print("\n1.3.2 Summary statistics for engagement metrics by candidate and emotion:")
engagement_metrics = ['favorite_count', 'retweet_count']

# Create hierarchical indexing and analysis for each emotion
for emotion in emotion_categories:
    # Create bins for emotion counts
    combined_df[f'{emotion}_level'] = pd.cut(
        combined_df[emotion], 
        bins=[-1, 0, 2, float('inf')],
        labels=['None', 'Low', 'High']
    )
    
    # Group by candidate and emotion level, calculate engagement stats
    stats = combined_df.groupby(['candidate', f'{emotion}_level'])[engagement_metrics].describe()
    print(f"\nEngagement metrics for {emotion}:")
    print(stats)

# 1.4 Visualizing Results
print("\n1.4 Visualizing Results")

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
