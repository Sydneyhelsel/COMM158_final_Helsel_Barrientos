# Part 3: Open Ended Exploration - Hashtag Analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter

# This exploration examines the hashtags used by Trump and Clinton during the election,
# testing the hypothesis that Trump used more actionable and negative hashtags than Clinton,
# and analyzing the emotional content and engagement of tweets containing these hashtags.

# Research question: Did Trump use more actionable and negative hashtags than Clinton?
# Analysis method: Frequency analysis of hashtags, categorization of hashtag types,
# emotion profile analysis, and engagement metrics comparison.

# Note: 
# - Fixed 'mcincle' to 'rncincle' in hashtag extraction
# - Combined 'maga' and 'makeamericagreatagain' as one hashtag theme
# - Combined 'votetrump' and 'trump2016' as one hashtag theme
# - Categorized hashtags as 'Event-related', 'Action-oriented', 'Negative/Attack', or 'Other'

# Extract hashtags from original tweets
def extract_hashtags(text):
    # Use regex to find all hashtags
    hashtags = re.findall(r'#(\w+)', str(text))
    
    # Normalize specific hashtags
    normalized = []
    for tag in hashtags:
        tag = tag.lower()
        # Fix mcincle to rncincle
        if tag == 'mcincle':
            normalized.append('rncincle')
        else:
            normalized.append(tag)
    
    return normalized

# Normalize and combine similar hashtags
def normalize_hashtags(hashtags):
    normalized = []
    for tag in hashtags:
        # Combine MAGA-related hashtags
        if tag in ['maga', 'makeamericagreatagain']:
            normalized.append('maga/makeamericagreatagain')
        # Combine Trump campaign hashtags
        elif tag in ['votetrump', 'trump2016']:
            normalized.append('votetrump/trump2016')
        else:
            normalized.append(tag)
    return normalized

# Function to get hashtag emotion data - for combined hashtags
def get_hashtag_emotions(df, hashtag):
    # For combined hashtags, split and check for either one
    if '/' in hashtag:
        tag1, tag2 = hashtag.split('/')
        mask = (df['text'].str.contains(f'#{tag1}', case=False, na=False) | 
                df['text'].str.contains(f'#{tag2}', case=False, na=False))
    else:
        mask = df['text'].str.contains(f'#{hashtag}', case=False, na=False)
    
    hashtag_tweets = df[mask]
    
    if len(hashtag_tweets) == 0:
        return None
    
    # Calculate average emotion scores
    emotion_scores = hashtag_tweets[emotion_categories].mean()
    
    # Calculate average engagement
    engagement = {
        'favorite_count': hashtag_tweets['favorite_count'].mean(),
        'retweet_count': hashtag_tweets['retweet_count'].mean(),
        'tweet_count': len(hashtag_tweets)
    }
    
    return pd.Series({**emotion_scores, **engagement})

# Categorize hashtags
def categorize_hashtag(tag):
    if tag in event_hashtags:
        return 'Event-related'
    elif tag in action_hashtags:
        return 'Action-oriented'
    elif tag in negative_hashtags:
        return 'Negative/Attack'
    else:
        return 'Other'

# Analysis:
"""
Though It would've been intriguing to see whether or not there was any interaction between engagement levels and the expected outcome of the election, I felt it was flawed for a multitude of reasons. The First of that is that the sample is way too small. Sure there are 12000 lines of tweets, but to truly understand whether or not it is a predictor of elections (something that already changes so much in the 4 years between elections) you would need a much larger sample and that's limited to just 4 elections, one of which, was while it was still a relatively small app. Instead of analyzing election outcomes, I decided to focus on whether or not there was an increased engagement with certain hashtags, which hashtags were used the most by each set of candidate related tweets, and the emotion surrounding a given hashtag. From the 6 charts (3 types, 1 for each candidate) I put together I was able to make 3 conclusions. The first is that Hillary related tweets used almost exclusively event-related hashtags, with the exception of "#imwithher" and "#tbt," which is in extreme contrast to Trump related tweets who used more actionable and targeted hashtags, like "#crookedhillary," "#draintheswamp," and "#americafirst" all of which spoke down on Hillary's campaign. The second conclusion I was able to make was that Hillary related tweets with hashtags were generally much more emotional than Trump related tweets. The final conclusion is that Trump's choice to shift toward more targeted and actionable messaging generally worked from a marketing and engagement perspective on social media as we see with the tweets. Trump related tweets across the board had more engagement with his most used hashtags than Hillary, having significantly higher favorite and retweet counts.
"""
