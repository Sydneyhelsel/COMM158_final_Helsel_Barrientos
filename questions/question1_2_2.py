# 1.2.2 Apply the self-defined function to the text column of the merged data frame from #1.1.
# First, create a cleaned text column
combined_df['cleaned_text'] = combined_df['text'].apply(clean_text)

# Apply the sentiment analysis function to each tweet in the cleaned text column
sentiment_counts = combined_df['cleaned_text'].apply(lambda tweet: get_sentiment_counts(tweet, nrc_lexicon))

# Convert the dictionary of sentiment counts into separate columns
sentiment_df = pd.DataFrame(list(sentiment_counts))

# Merge the sentiment columns with the original DataFrame
merged_df_with_sentiments = pd.concat([combined_df, sentiment_df], axis=1)

# Display the updated DataFrame
print(merged_df_with_sentiments)

