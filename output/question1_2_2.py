
# Apply the function to the cleaned text
sentiment_counts = combined_df['cleaned_text'].apply(lambda tweet: get_sentiment_counts(tweet, nrc_lexicon))

# Convert the dictionary of sentiment counts into separate columns
sentiment_df = pd.DataFrame(list(sentiment_counts))

# Add a threshold to make emotion detection more selective
# For each emotion column, create a boolean column indicating if the score exceeds a threshold
threshold = 2  # Adjust this value as needed
for emotion in sentiment_df.columns:
    sentiment_df[f'{emotion}_significant'] = sentiment_df[emotion] > threshold

# Calculate the percentage of tweets with significant emotions
for emotion in sentiment_df.columns:
    if '_significant' in emotion:
        percent = sentiment_df[emotion].mean() * 100
        print(f"Tweets with significant {emotion.replace('_significant', '')}: {percent:.1f}%")

# Merge the sentiment columns with the original DataFrame
merged_df_with_sentiments = pd.concat([combined_df, sentiment_df], axis=1)


