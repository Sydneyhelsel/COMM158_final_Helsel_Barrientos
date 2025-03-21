# Part 2: Correlation Analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 2.1 Research Question: Is there a relationship between emotion categories 
# and the number of retweets or favorites?

# Use the merged DataFrame with sentiment scores from part 1.4
# Assuming we're working with the merged_df_with_sentiments from the previous parts

# Load data with sentiment scores (run parts 1.1-1.4 first)
# This loads the data and executes the previous code
exec(open('output/question1_4.py').read())

# Now we can access the merged_df_with_sentiments variable

# Define emotion categories and engagement metrics
emotion_categories = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 
                     'sadness', 'surprise', 'trust', 'positive', 'negative']
engagement_metrics = ['favorite_count', 'retweet_count']

# Calculate correlation between emotion counts and engagement metrics
print("\nResearch Question: Is there a relationship between emotion categories and engagement?")
correlation_df = merged_df_with_sentiments[emotion_categories + engagement_metrics].corr()

# Extract the correlations between emotions and engagement metrics
emotion_engagement_corr = correlation_df.loc[emotion_categories, engagement_metrics]
print("\nCorrelation between emotions and engagement metrics:")
print(emotion_engagement_corr)

# Create a heatmap to visualize the correlations
plt.figure(figsize=(10, 8))
sns.heatmap(emotion_engagement_corr, annot=True, cmap='coolwarm', vmin=-0.2, vmax=0.2)
plt.title('Correlation between Emotions and Engagement Metrics', fontsize=16)
plt.tight_layout()
plt.savefig('output/emotion_engagement_correlation.png')

# Analyze correlations separately for each candidate
fig, axes = plt.subplots(1, 2, figsize=(20, 8))

for i, candidate in enumerate(merged_df_with_sentiments['candidate'].unique()):
    # Filter data for this candidate
    candidate_df = merged_df_with_sentiments[merged_df_with_sentiments['candidate'] == candidate]
    
    # Calculate correlations
    candidate_corr = candidate_df[emotion_categories + engagement_metrics].corr()
    candidate_emotion_engagement = candidate_corr.loc[emotion_categories, engagement_metrics]
    
    # Plot heatmap
    sns.heatmap(candidate_emotion_engagement, 
                annot=True, 
                cmap='coolwarm', 
                vmin=-0.2, 
                vmax=0.2, 
                ax=axes[i])
    axes[i].set_title(f'Correlations for {candidate}', fontsize=14)

plt.tight_layout()
plt.savefig('output/emotion_engagement_correlation_by_candidate.png')

# Write your paragraph analysis here:
"""
ANALYSIS PARAGRAPH:
[Your analysis should go here. Discuss the relationship between emotion categories and 
engagement metrics (likes and retweets). Note any interesting patterns or differences 
between candidates. Interpret what the correlations mean in the context of political 
discourse on Twitter during the election.]
"""
