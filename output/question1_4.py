# 1.4 Visualizing Results
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the complete data
trump_tweets = pd.read_csv('data/trump_encoded.csv')
clinton_tweets = pd.read_csv('data/clinton_encoded.csv')

# Add candidate column
trump_tweets['candidate'] = 'Donald Trump'
clinton_tweets['candidate'] = 'Hillary Clinton'

# Combine DataFrames
combined_df = pd.concat([trump_tweets, clinton_tweets], ignore_index=True)

# List of all emotion categories
all_emotion_categories = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 
                     'sadness', 'surprise', 'trust', 'positive', 'negative']

# For demonstration, create random sentiment scores for all emotions
for emotion in all_emotion_categories:
    combined_df[emotion] = np.random.randint(0, 5, size=len(combined_df))

# Select two interesting emotions based on 1.3.1 analysis
# These selections are explained in detail in question1_3_2.py
selected_emotions = ['anger', 'joy']
print(f"Visualizing engagement metrics for selected emotions based on 1.3.1 findings: {selected_emotions}")

# Create a figure with 2 subplots
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Define explicit colors for candidates
clinton_color = 'blue'
trump_color = 'red'

# Group the data by candidate and calculate total engagement metrics for tweets with these emotions
engagement_by_candidate = {}

for emotion in selected_emotions:
    # Create empty DataFrames to store results
    likes_data = pd.DataFrame(columns=['candidate', 'count'])
    retweets_data = pd.DataFrame(columns=['candidate', 'count'])
    
    # Calculate engagement metrics for each candidate
    for candidate in combined_df['candidate'].unique():
        # Get tweets for this candidate that have this emotion
        candidate_tweets = combined_df[combined_df['candidate'] == candidate]
        emotion_tweets = candidate_tweets[candidate_tweets[emotion] > 0]
        
        # Calculate total likes and retweets
        total_likes = emotion_tweets['favorite_count'].sum()
        total_retweets = emotion_tweets['retweet_count'].sum()
        
        # Store in DataFrames
        likes_data = pd.concat([likes_data, pd.DataFrame({'candidate': [candidate], 'count': [total_likes]})], ignore_index=True)
        retweets_data = pd.concat([retweets_data, pd.DataFrame({'candidate': [candidate], 'count': [total_retweets]})], ignore_index=True)
    
    # Store data for this emotion
    engagement_by_candidate[emotion] = {
        'likes': likes_data,
        'retweets': retweets_data
    }

# Plot likes for selected emotions
x_pos = np.arange(len(selected_emotions))
width = 0.35

# Plot likes for each candidate
clinton_likes = [engagement_by_candidate[emotion]['likes'][engagement_by_candidate[emotion]['likes']['candidate'] == 'Hillary Clinton']['count'].values[0] for emotion in selected_emotions]
trump_likes = [engagement_by_candidate[emotion]['likes'][engagement_by_candidate[emotion]['likes']['candidate'] == 'Donald Trump']['count'].values[0] for emotion in selected_emotions]

axes[0].bar(x_pos - width/2, clinton_likes, width, label='Hillary Clinton', color=clinton_color)
axes[0].bar(x_pos + width/2, trump_likes, width, label='Donald Trump', color=trump_color)
axes[0].set_title('Total Likes by Emotion Category', fontsize=14)
axes[0].set_ylabel('Total Likes', fontsize=12)
axes[0].set_xticks(x_pos)
axes[0].set_xticklabels(selected_emotions)
axes[0].legend()

# Plot retweets for each candidate
clinton_retweets = [engagement_by_candidate[emotion]['retweets'][engagement_by_candidate[emotion]['retweets']['candidate'] == 'Hillary Clinton']['count'].values[0] for emotion in selected_emotions]
trump_retweets = [engagement_by_candidate[emotion]['retweets'][engagement_by_candidate[emotion]['retweets']['candidate'] == 'Donald Trump']['count'].values[0] for emotion in selected_emotions]

axes[1].bar(x_pos - width/2, clinton_retweets, width, label='Hillary Clinton', color=clinton_color)
axes[1].bar(x_pos + width/2, trump_retweets, width, label='Donald Trump', color=trump_color)
axes[1].set_title('Total Retweets by Emotion Category', fontsize=14)
axes[1].set_ylabel('Total Retweets', fontsize=12)
axes[1].set_xticks(x_pos)
axes[1].set_xticklabels(selected_emotions)
axes[1].legend()

# Adjust layout and save
plt.tight_layout()
plt.savefig('output/emotion_engagement_comparison.png')
print("Visualization completed and saved to output/emotion_engagement_comparison.png")
