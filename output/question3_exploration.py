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

# [Code for hashtag analysis]

# Analysis:
"""
Though It would've been intriguing to see whether or not there was any interaction between 
engagement levels and the expected outcome of the election, I felt it was flawed for a 
multitude of reasons. The First of that is that the sample is way too small. Sure there 
are 12000 lines of tweets, but to truly understand whether or not it is a predictor of 
elections (something that already changes so much in the 4 years between elections) you 
would need a much larger sample and that's limited to just 4 elections, one of which, was 
while it was still a relatively small app.

Instead of analyzing election outcomes, I decided to focus on whether or not there was an 
increased engagement with certain hashtags, which hashtags were used the most by each 
candidate, and the emotion surrounding a given hashtag. From the 6 charts (3 types, 1 for 
each candidate) I put together I was able to make 3 conclusions.

The first is that Hillary used almost exclusively event-related hashtags, with the exception 
of "#imwithher" and "#tbt," which is in extreme contrast to Trump who used more actionable 
and targeted hashtags, like "#crookedhillary," "#draintheswamp," and "#americafirst" all 
of which spoke down on Hillary's campaign.

The second conclusion I was able to make was that Hillary's tweets with hashtags were 
generally much more emotional than Trump's.

The final conclusion is that Trump's choice to shift toward more targeted and actionable 
messaging generally worked from a marketing and engagement perspective on social media. 
Trump across the board had more engagement with his most used hashtags than Hillary, having 
significantly higher favorite and retweet counts.
"""
