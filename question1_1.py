#1.1
import pandas as pd

# Load CSV files
# So the correct paths are:
trump_tweets = trump_df = pd.read_csv('data/trump_encoded.csv')
clinton_tweets = pd.read_csv('data/clinton_encoded.csv')

# Add candidate column
trump_tweets['candidate'] = 'Donald Trump'
clinton_tweets['candidate'] = 'Hillary Clinton'

# Combine DataFrames
combined_df = pd.concat([trump_tweets, clinton_tweets], ignore_index=True)

# Display the first few rows to verify
combined_df.head()
