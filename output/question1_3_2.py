# 1.3.2 Group by candidate and each emotion category, then compute summary statistics
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

# 1.3.2 Group by candidate and emotion category, compute summary stats for engagement
print("1.3.2 Summary statistics for engagement metrics by candidate and emotion:")
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
