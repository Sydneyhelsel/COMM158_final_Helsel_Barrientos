
##############################################
# === Part 3 Exploration #2 (Sydney) ===
##############################################
"""
# The previous exploration looked at engagement with certain hashtags associated with Trump and Clinton during the 2016 election. 
# To further understand the amount of engagement with these hashtags, I decided to make a graph that visualizes the engagement with the 
# top five hashtags over time. This way, we can see when certain hashtags were created, and when they were most popular. 

# My research question is: Do certain hashtags have more engagement during certain weeks of the election? 
# This could give insights into more specific questions, such as:  is there more engagement with hashtags relating to debates during debate weeks? 

# My hypothesis is that engagement with hashtags will fluctuate over time, with greater variance in engagement for hashtags associated 
# with Hillary Clinton compared to those associated with Donald Trump. This is because Clinton’s top hashtags are more event-driven, 
# leading to spikes and drops in engagement during certain times, while Trump’s hashtags function more as slogans and maintain more consistent engagement.

# Analysis method: I created a time-series graph that visualizes the engagement of the five most popular hashtags over time, 
# highlighting when each hashtag emerged and peaked.

# The visualization validates my hypothesis, confirming that hashtags vary in engagement 
# over the course of the election, and specifically that Trump’s hashtags seem to be more popular for longer periods of time.
# For example the orange line on the graph for the Trump tweets, which was for the hashtag “#Makeamericagreatagain” spans for nearly the 
# entire period of time that the data examined. Notably, it is his campaign slogan. Similarly, the “#Imwithher” hashtag from the Hilary tweets, 
# represented by the purple line, which was the most similar to a slogan out of her top five hashtags, has the longest period of engagement
# out of the five. Another insight we can make from this visualization is that engagement as a whole with certain hashtags spiked in late October 
# and early November for both candidates. This makes sense, due to the proximity to the election. I also had it confirm the sentiment (positive
# or negative) of the hashtag to see if there was a difference, but it turns out the most popular hashtags were all positive. 

#The code for the time series graph is below: 
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

##############################################
# === Load Data ===
##############################################
trump_df = pd.read_csv('data/trump_encoded.csv')
clinton_df = pd.read_csv('data/clinton_encoded.csv')
trump_df['candidate'] = 'Donald Trump'
clinton_df['candidate'] = 'Hillary Clinton'
df = pd.concat([trump_df, clinton_df], ignore_index=True)

# Convert 'created_at' to datetime
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

# Calculate engagement for each tweet
df['engagement'] = df['favorite_count'] + df['retweet_count']

##############################################
# Use hashtagged tweets with sentiment analysis
##############################################

# --- Clean text function (already in your code) ---
def clean_text(text):
    text = re.sub(r'@[\w]+', '', text)
    text = re.sub(r'#[\w]+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text

# --- Load NRC Emotion Lexicon ---
nrc = pd.read_csv('NRC-Emotion-Lexicon-Wordlevel-v0.92.txt', sep="\t", header=None,
                  names=["word", "emotion", "association"])
nrc = nrc[nrc['association'] == 1].drop(columns=['association'])

# --- Sentiment Function (raw counts) ---
def get_sentiment_counts(text, lexicon):
    tokens = word_tokenize(text)
    counts = {emotion: 0 for emotion in lexicon['emotion'].unique()}
    for token in tokens:
        matches = lexicon[lexicon['word'] == token]
        for _, row in matches.iterrows():
            counts[row['emotion']] += 1
    return counts

# --- Filter hashtagged tweets ---
df['has_hashtag'] = df['text'].str.contains(r'#\w+')
hashtagged = df[df['has_hashtag']].copy()

# --- Clean and apply sentiment analysis ---
hashtagged['cleaned_text'] = hashtagged['text'].apply(clean_text)
sentiment_counts = hashtagged['cleaned_text'].apply(lambda t: get_sentiment_counts(t, nrc))
sentiment_df = pd.DataFrame(list(sentiment_counts))
# Merge sentiment results back into hashtagged tweets
hashtagged_sentiment = pd.concat([hashtagged.reset_index(drop=True), sentiment_df.reset_index(drop=True)], axis=1)

# Compute net sentiment as positive - negative
hashtagged_sentiment['net_sentiment'] = hashtagged_sentiment['positive'] - hashtagged_sentiment['negative']

# Create a week column (Period) for aggregation
hashtagged_sentiment['week'] = hashtagged_sentiment['created_at'].dt.to_period('W')
hashtagged_sentiment['week_start'] = hashtagged_sentiment['week'].dt.start_time

##############################################
# Extract hashtags and determine top 5 per candidate
##############################################

def extract_hashtags(text):
    tags = re.findall(r'#\w+', text)
    return [tag.lower() for tag in tags]

hashtagged_sentiment['hashtags'] = hashtagged_sentiment['text'].apply(extract_hashtags)

# Explode the hashtags so each hashtag gets its own row
hs_exploded = hashtagged_sentiment.explode('hashtags')
# Remove rows with no hashtag
hs_exploded = hs_exploded[hs_exploded['hashtags'].notna()]

# Determine top 5 hashtags for each candidate by frequency
top_hashtags = {}
for candidate in hs_exploded['candidate'].unique():
    candidate_df = hs_exploded[hs_exploded['candidate'] == candidate]
    top5 = candidate_df['hashtags'].value_counts().head(5).index.tolist()
    top_hashtags[candidate] = top5

print("Top 5 Hashtags per Candidate:", top_hashtags)

# Filter hs_exploded to include only the top hashtags for each candidate
filtered_hs = hs_exploded[hs_exploded.apply(lambda row: row['hashtags'] in top_hashtags[row['candidate']], axis=1)]

##############################################
# Aggregate Engagement & Sentiment by Candidate, Hashtag, and Week
##############################################

agg = filtered_hs.groupby(['candidate', 'hashtags', 'week', 'week_start']).agg({
    'engagement': 'mean',
    'net_sentiment': 'mean'
}).reset_index()

# Compute overall net sentiment for each candidate and hashtag over the entire period
overall_sentiment = filtered_hs.groupby(['candidate', 'hashtags']).agg({
    'net_sentiment': 'mean'
}).reset_index()

# Classify overall sentiment as Positive if net sentiment > 0, else Negative
sentiment_class = {}
for _, row in overall_sentiment.iterrows():
    sentiment_class[(row['candidate'], row['hashtags'])] = "Positive" if row['net_sentiment'] > 0 else "Negative"

##############################################
# Plot: Engagement Over Time for Top Hashtags with Sentiment Annotation
##############################################

# Create one subplot per candidate
candidates = list(top_hashtags.keys())
n_candidates = len(candidates)
fig, axs = plt.subplots(n_candidates, 1, figsize=(14, 6 * n_candidates), sharex=True)
if n_candidates == 1:
    axs = [axs]

for ax, candidate in zip(axs, candidates):
    candidate_data = agg[agg['candidate'] == candidate]
    for tag in top_hashtags[candidate]:
        tag_data = candidate_data[candidate_data['hashtags'] == tag].sort_values('week')
        overall_label = sentiment_class.get((candidate, tag), "Unknown")
        # Label includes the hashtag and its overall sentiment classification
        ax.plot(tag_data['week_start'], tag_data['engagement'],
                label=f"{tag} ({overall_label})", marker='o', linestyle='-')
    ax.set_title(f"Top 5 Hashtags Engagement & Sentiment Over Time - {candidate}", fontsize=16)
    ax.set_xlabel("Week")
    ax.set_ylabel("Average Engagement")
    ax.legend()
    ax.grid(True)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.setp(ax.get_xticklabels(), rotation=45)

plt.tight_layout()
plt.savefig('output/hashtag_engagement_sentiment_over_time.png')
plt.show()
