import pandas as pd
import numpy as np
from random import randint
import sys
import datetime
import nltk.data
import os
import random
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from module_variables import PATH

'''
Script to convert pilotly data into processed.csv and Training.csv for use in 1_featurize_training_dat.py, main.py
and business.py
- featurize_data script only uses: ['business_id', 'review_id', 'user_id', 'review_stars', 'user_avg_stars']
- business.py appears to use all of them but not sure if they are all necessary, can input placeholder values too

column_map = {
    'business_id': 'episode_id',
    'review_id': 'id',
    'text': 'answer',
    'user_id': 'user_id',
    'review_stars': None,#'need to get this'),
    'review_count': None,  #'can get in sql'),
    'business_overall_stars': None, #('sql with review stars'),
    'business_name': 'title', #found in panel_results table, pull in
    'business_categories': None, #Genre??
    'business_ambiance': None, #can't imagine this is important...
    'user_avg_stars': None, #need review stars (should also figure out how this is used, what if only 1 review?)
    'user_name': None #not sure if anywhere, also can't imagine how it's important
    }
'''

class ConvertPilotlyData:
	def __init__(self):
		# self.df = pd.read_csv(fname)
		self.init_columns = ['business_id', 'review_id', 'user_id']
		self.column_list = ['business_id', 'review_id', 'user_id', 'review_stars', 'user_avg_stars']
		self.column_map = {'id': 'review_id', 'answer': 'text', 'episode_name':'business_name'}
		# self.column_map = {'episode_id': 'business_id', 'id': 'review_id', 'answer': 'text'}
		# self.star_sent_map = ['Negative', 'Negative', 'Objective', 'Positive', 'Positive']
		self.star_sent_map = ['Negative', 'Negative', 'Negative', 'Objective', 'Positive']

	def fit(self, df):
		self.df = df
		self.df = self.process_data(df)
		self.df = self.add_review_stars(self.df)
		self.df = self.add_user_avg_stars(self.df)
		self.df = self.add_business_overall_stars(self.df)
		self.df = self.get_misc_cols(self.df)

		self.df = self.check_unique(self.df)

		self.sent_df = self.build_sentiment_df(self.df)

	def get_misc_cols(self, df): ### CHANGE THIS
		# df['business_name'] = 'Versailles Pilot'
		# df['business_ambiance'] = ''
		df['business_categories'] = 'Biography, Drama, History'
		df['user_name'] = 'user'
		return df


	def process_data(self, df):
		df = df[['id', 'episode_name', 'episode_id', 'qid', 'question', 'answer', 'user_id', 'sentiment_index']]
		df = df.rename(columns = self.column_map)
		self.names = list(df.business_name.unique())
		df['business_id'] = df['business_name'].apply(lambda x: self.names.index(x))
		return df

	# def add_review_stars(self, df):
	# 	# randomly assigns review stars
	# 	d = {}
	# 	review_ids = df['review_id'].values
	# 	for i in review_ids:
	# 		d[i] = randint(1,5)
	# 	df['review_stars'] = df['review_id'].apply(lambda x: d[x])
	# 	return df


	def add_review_stars(self, df):
		# assigns stars based on sentiment index
		df = df.dropna(subset = ['sentiment_index']) # drop reviews without sentiment as that's not helpful
		df['review_stars'] = df['sentiment_index'].apply(lambda x: int(5 - x))
		return df

	def add_user_avg_stars(self, df):
		mean_stars_df = df[['user_id', 'review_stars']].groupby('user_id').mean().reset_index()
		mean_stars_df = mean_stars_df.rename(columns = {'review_stars': 'user_avg_stars'})
		df = pd.merge(df, mean_stars_df, how = 'left', on = 'user_id')
		return df

	def add_business_overall_stars(self, df):
		mean_stars_df = df[['business_id', 'review_stars']].groupby('business_id').mean().reset_index()
		mean_stars_df = mean_stars_df.rename(columns = {'review_stars': 'business_overall_stars'})
		df = pd.merge(df, mean_stars_df, how = 'left', on = 'business_id')
		return df

	def check_unique(self, df):
		### CHANGE BELOW - ADJUSTING FOR DUPLICATES THAT SHOULDN'T EXIST, TRY TO FIX PROBLEM
		print 'checking unique...'
		if len(df) != len(df['review_id'].unique()):
			print 'ERROR review_id not unique'
			print 'num reviews_ids: ', len(df['review_id'].unique())
			print 'num reviews: ', len(df)
			# raise ValueError('ERROR review_id not unique')
			df = df.groupby('review_id').last().reset_index()
			if len(df) != len(df['review_id'].unique()):
				raise ValueError('ERROR review_id not unique')
		if len(df) != len(df[['user_id','qid']].groupby(['user_id', 'qid'])):
			print 'ERROR user_id not unique for given qid'
			print 'num user_id/qid: ', len(df[['user_id','qid']].groupby(['user_id', 'qid']))
			print 'num reviews: ', len(df)
			df = df.groupby(['user_id','qid']).last().reset_index()
			# raise ValueError('ERROR user_id not unique')
		return df

	def build_sentiment_df(self, df):

		# ### CHANGE BELOW - ADJUSTING FOR DUPLICATES THAT SHOULDN'T EXIST, TRY TO FIX PROBLEM
		# if len(df) != len(df['review_id'].unique()):
		# 	print 'ERROR review_id not unique'
		# 	print 'num reviews_ids: ', len(df['review_id'].unique())
		# 	print 'num reviews: ', len(df)
		# 	# raise ValueError('ERROR review_id not unique')
		# 	df = df.groupby('review_id').last().reset_index()
		# 	if len(df) != len(df['review_id'].unique()):
		# 		raise ValueError('ERROR review_id not unique')
		# if len(df) != len(df[['user_id','qid']].groupby(['user_id', 'qid'])):
		# 	print 'ERROR user_id not unique for given qid'
		# 	print 'num user_id/qid: ', len(df[['user_id','qid']].groupby(['user_id', 'qid']))
		# 	print 'num reviews: ', len(df)
		# 	df = df.groupby(['user_id','qid']).last().reset_index()
		# 	# raise ValueError('ERROR user_id not unique')



		sent_d = df[['text', 'review_id', 'review_stars']].set_index('review_id').T.to_dict()
		l = []
		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		for review_id in sent_d:
			if isinstance(sent_d[review_id]['text'], str):
				for sentence in tokenizer.tokenize(sent_d[review_id]['text']):
					if len(sentence.strip()) > 5:
						# mapped sentiment to stars option 
						l.append({'review_id': review_id, 'sentence': sentence, 
							'sentiment': self.star_sent_map[sent_d[review_id]['review_stars'] - 1]})

						# random sentiment option 
						# l.append({'review_id': review_id, 'sentence': sentence, 
						# 	'sentiment': self.star_sent_map[random.randint(0,4)]})

		return pd.DataFrame(l)

def rename(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        os.rename(pathAndFilename, 
                  os.path.join(dir, titlePattern % title + ext))


if __name__ == '__main__':
	fname = sys.argv[1]
	df = pd.read_csv(fname)
	cpd = ConvertPilotlyData()
	cpd.fit(df)
	cpd.df.to_csv('../data/pilotly_data/processed.csv')
	directory = PATH + 'data/Sentiment/'
	for f in os.listdir(directory):
		if f.startswith('Training'):
			path = os.path.join(directory, f)
			target = os.path.join(directory, f.replace('Training', 'old_Training'))
			os.rename(path, target)

	cpd.sent_df.to_csv('../data/Sentiment/Training' + str(int(datetime.datetime.now().strftime("%s"))) + '.csv')
