from nltk.tokenize import word_tokenize  # Ensure you import this

# 1.2.1 Create a Sentiment Analysis Function
def get_sentiment_counts(tweet_text, lexicon):

    #This function takes the text of a tweet and returns a count of each of the 10 sentiment categories.

    #Parameters:
    #tweet_text (str): The text of the tweet.
    #lexicon (DataFrame): The NRC Emotion Lexicon (filtered to only include associated emotions).

    #Returns:
    #dict: A dictionary with sentiment categories as keys and their counts as values.

    # Tokenize the tweet text into words
    tokens = word_tokenize(tweet_text.lower())  # Lowercasing for matching

    # Initialize a dictionary to store sentiment counts
    sentiment_counts = {emotion: 0 for emotion in lexicon['emotion'].unique()}

    # Check each token in the tweet text
    for token in tokens:
        # Check if the token is in the NRC Emotion Lexicon
        emotion_matches = lexicon[lexicon['word'] == token]

        # For each matching emotion, increment the corresponding count
        for _, row in emotion_matches.iterrows():
            sentiment_counts[row['emotion']] += 1  # Increment the count for the emotion

    return sentiment_counts
