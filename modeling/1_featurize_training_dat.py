"""
1_featurize_training_data.py

This file:
- reads in the hand-tagged training data
- featurizes the training data using the Sentence class
- merges in relevant features from the raw yelp data
- splits data into development and pure holdout sets and writes these to disk

"""

import os
import pandas as pd
import ipdb 

PATH_TO_DATA = "/var/www/sandbox/ben/opinion-mining/data/"
PATH_TO_SENT = "/var/www/sandbox/ben/opinion-mining/data/Sentiment/" # hand-tagged training data
PATH_TO_YELP = '/var/www/sandbox/ben/opinion-mining/data/yelp_data/raw/yelp_academic_dataset_review.json' # raw Yelp data

train_fnames = [fname for fname in os.listdir(PATH_TO_SENT) if fname.startswith("Training")]

'''
TEMPORARILY REMOVING THIS STEP - STILL IN ORIGINAL

# LOAD THE TRAINING DATA....
print "Reading in the training data..."
train_dfs = [pd.read_csv(PATH_TO_SENT+fname) for fname in train_fnames]
ipdb.set_trace()
for df in train_dfs:
    df.columns = ['review_id', 'sentence', 'sentiment'] #clean up column names for merging

# MERGE THE TRAINING DAT....
print "Merging training data..."
base_df = train_dfs.pop()
for remaining_df in train_dfs:
    base_df = base_df.append(remaining_df, ignore_index=True)

'''
base_df = pd.read_csv(PATH_TO_SENT + train_fnames[0]) ### MY ADDITION

# fix stray value
base_df.sentiment[base_df.sentiment=='Neutral'] = 'Negative'

# READ IN THE YELP DATA....
print "Reading in the Yelp data..."
processed_df = pd.read_csv(PATH_TO_DATA + 'yelp_data/processed.csv')

# keep only what's needed
keeps =['business_id', 'review_id', 'user_id', 'review_stars', 'user_avg_stars']
processed_df = processed_df[keeps]

# Merge the two data frames
print "Merging training and Yelp data frames & importing Sentence (slowish)"
final_df = base_df.merge(processed_df, how='left', on='review_id')

# drop a few unmatched values
# ipdb.set_trace()
# final_df = final_df[~final_df.business_id.isnull()]
final_df = final_df.dropna(axis = 0, subset = ['sentence', 'business_id']) ## MY ADDITION HOPING IT DOESN"T MESS THINGS UP
final_df.to_pickle('final_df.pkl') ## REMOVE

# FEATURIZE

## Import Sentence class from this project
import sys
sys.path.append("/var/www/sandbox/ben/opinion-mining")
from classes.sentence import Sentence

print "Featurizing the training data frame (may take a little while)"

sents = [Sentence(sent) for sent in final_df.sentence]

for sent, stars in zip(sents, final_df.review_stars): 
	sent.stars =  stars # pass the number of stars in

featurized_df = pd.DataFrame([sent.get_features() for sent in sents])

featurized_df['sentiment'] = final_df.sentiment
featurized_df = featurized_df[~featurized_df.sentiment.isnull()]

print "Done."
ipdb.set_trace()

# Adjust sentiment labels
featurized_df.sentiment[featurized_df.sentiment=='Positive'] = 1
featurized_df.sentiment[featurized_df.sentiment=='Negative'] = -1
featurized_df.sentiment[featurized_df.sentiment=='Objective'] = 0

# Create 'opinionated' variable
featurized_df['opinionated'] = 0
featurized_df['opinionated'][featurized_df.sentiment!= 0] = 1

# Write to disk in two parts (development and pristine holdout)
import random
random.seed(117) #repeatability

print "Writing out a random sample (20%)"
rows = random.sample(featurized_df.index, int(len(featurized_df)*.2))

df_holdout = featurized_df.ix[rows].copy()
df_devel = featurized_df.drop(rows).copy()

# Write to disk
df_holdout.to_csv("./data/featurized_pristine_holdout.csv", index=False)
df_devel.to_csv("./data/featurized_development.csv", index=False)

print "Done."










