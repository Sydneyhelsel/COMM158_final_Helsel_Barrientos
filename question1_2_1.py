from nltk.tokenize import word_tokenize  # Ensure you import this
# Download the 'punkt' tokenizer and 'punkt_tab'
nltk.download('punkt')
nltk.download('punkt_tab')

# 1.2.1 Create a Sentiment Analysis Function

    # Fix the sentiment analysis function and apply it to cleaned text
def get_sentiment_counts(tweet_text, lexicon):
    # Tokenize the tweet text into words
    tokens = word_tokenize(str(tweet_text).lower())  # Lowercasing for matching
    
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

