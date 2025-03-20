#1.2 (first cleaning data)
import nltk
!wget https://raw.githubusercontent.com/aditeyabaral/lok-sabha-election-twitter-analysis/master/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt

# Download the 'punkt' tokenizer and 'punkt_tab'
nltk.download('punkt')
nltk.download('punkt_tab')

import re

# Function to clean text
def clean_text(text):
    # Remove mentions (@username) and hashtags (#hashtag)
    text = re.sub(r'@[\w]+', '', text)  # Remove mentions
    text = re.sub(r'#[\w]+', '', text)  # Remove hashtags

    # Remove non-alphabetical characters (punctuation, numbers, etc.)
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Only keep alphabets and spaces

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

#1.2 Now sentiment analysis
# Load NRC Emotion Lexicon
from nltk.tokenize import word_tokenize
nrc_lexicon = pd.read_csv("NRC-Emotion-Lexicon-Wordlevel-v0.92.txt",
                          sep="\t",
                          header=None,
                          names=["word", "emotion", "association"])

# Filter out non-associated words
nrc_lexicon = nrc_lexicon[nrc_lexicon["association"] == 1].drop(columns=["association"])

# Function to calculate emotion scores for each tweet
def get_emotion_scores(text):
    tokens = word_tokenize(str(text).lower())  # Tokenize and lowercase text
    emotions = pd.Series(0, index=nrc_lexicon['emotion'].unique())  # Initialize counts

    # Filter NRC for words that appear in the text
    matched_words = nrc_lexicon[nrc_lexicon['word'].isin(tokens)]

    # Count emotions
    emotion_counts = matched_words['emotion'].value_counts()

    # Update the initialized emotions Series with counts
    emotions.update(emotion_counts)

    return emotions


# Apply the cleaning function to the text column
combined_df['cleaned_text'] = combined_df['text'].apply(clean_text)

# Check the cleaned text
print(combined_df['cleaned_text'].head())

# Now apply the sentiment analysis using the cleaned text
emotion_columns = combined_df['cleaned_text'].apply(get_emotion_scores)

# Combine the emotion scores with the original DataFrame
combined_df = pd.concat([combined_df, emotion_columns], axis=1)

# Display the updated DataFrame
combined_df
