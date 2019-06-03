"""
General task description: write a python script that takes a 
corpus and counts a certain linguistic features which are specified in csv files.

arguments: path to input folder (corpus, collection of texts), 
list of features to be retrieved (csv file), path to output folder

output:  2 csv files with texts as rownames and features as columns. 
One csv with raw feature frequencies; one csv with normalised frequencies 
"""

"""
TASK:
sample input data: news_corpus700
1. COUNT:
	using compinion_features to count:
	- adverbials[X]
	- modals[X]
	- connectives[X]
	- adverbs_negative[X]
	- adverbs_positive

2. POS: (see resources and example)
	- tagged with POS
	- get the stemmed
"""
import re
import os
import pandas as pd
import sys

def count_invariant_feature(feature, text):
	"""count the appearance times of a invariant feature in a file

	Args:
		feautre: a string to be cound
		text: a trunck of text **NOT ONLY ONE SENTENCE**

	return:
		counts of the apperance times of corresponding feature in a text
	"""
	return len(re.findall('\\b' + feature + '\\b', text))

def count_variant_feature(features, text, features_type):
	"""count the appearance times of a invariant feature in a file

	Args:
		feautres: a list of all the features to be cound
		text: a trunck of text **NOT ONLY ONE SENTENCE**
		features_type: the type of words (noun / verb / adj)
	return:
		list of counts of the apperance times of corresponding
		 feature list in a text
	"""
	# clean text
	from nltk.stem import WordNetLemmatizer
	from nltk import pos_tag
	from nltk.tokenize import word_tokenize
	TAG_POS_DICT_ADJ = {"JJ": 'a', "JJR": 'a', "JJS": 'a'}
	TAG_POS_DICT_VERB = {"VB":'v', "VBD":'v', 'VBG':'v', 'VBN': 'v', 'VBP':'v', 'VBZ':'v'}
	TAG_POS_DICT_NOUN = {'NN':'n', 'NNS':'n', 'NNP':'n', 'NNPS':'n'}
	TAG_POS_DICT = {'a':TAG_POS_DICT_ADJ, 'v': TAG_POS_DICT_VERB, 'n': TAG_POS_DICT_NOUN}
	DICT = TAG_POS_DICT[features_type]

	text = re.sub(r'\xe2\x80\x9c', ' ', text)
	text = re.sub(r'\xe2\x80\x93', ' ', text)
	text = text.decode("utf-8")
	tokens = word_tokenize(text) # Generate list of tokens
	tokens_pos = pos_tag(tokens)
	lemmatiser = WordNetLemmatizer()
	#e.g. lemmatiser.lemmatize("studying", pos="v")
	feature_count = dict(zip(features, [0]*len(features)))
	for token in tokens_pos:
		word, tag = token
		if DICT.has_key(tag):
			word_lemm = lemmatiser.lemmatize(word, DICT[tag])
			if feature_count.has_key(word_lemm):
				feature_count[word_lemm] += 1
	return feature_count.values()

def main(corpus_folder_dir, features_folder_dir, is_variant):
	# TODO: input / output

	# count invariant features
	if is_variant:
		out_folder = "variant_feature_count_result"
		out_sum_file = out_folder + "/variant_feature_sum.csv"
	else:
		out_folder = "invariant_feature_count_result"
		out_sum_file = out_folder + "/invariant_feature_sum.csv"
	if not os.path.exists(out_folder):
			os.makedirs(out_folder)
	if not os.path.exists(corpus_folder_dir):
		raise Exception("There is no such corpus folder!", corpus_folder_dir)
	if not os.path.exists(features_folder_dir):
		raise Exception("There is no such feature folder!", features_folder_dir)
	
	files = os.listdir(corpus_folder_dir)
	feature_sum_dict = dict(zip(files, [[] for i in range(len(files))]))

	for features_file in os.listdir(features_folder_dir):
		features_total = 0
		if features_file.split('.')[-1] != "csv":
			continue
		try:
			features = pd.read_csv(features_folder_dir + '/' + features_file)
			#write header into csv file
			with open(out_folder + "/" + features_file.split('/')[-1], "a") as out:
				out.write("words," + ",".join\
					(dict(zip(list(features.ix[:,0]), [0]*len(list(features.ix[:,0])))).keys()) + "\n")
			for file in files:
				result = file
				try:
					with open(corpus_folder_dir + '/' + file) as f:
						text = f.read()
					if is_variant:
						features_type = features_file[0]
						counts = count_variant_feature(list(features.ix[:,0]), text, features_type)
						result += "," + ",".join([str(c) for c in counts])
						features_total = sum(counts)
					else:
						for feature in list(features.ix[:,0]):
							feature_appear_times = count_invariant_feature(feature, text)
							result += "," + str(feature_appear_times)
							features_total += feature_appear_times
					feature_sum_dict[file].append(str(features_total))
				except IOError:
					print("fail to open the file: " + file)

				with open(out_folder + "/" + features_file.split('/')[-1], "a") as out:
					out.write(result + "\n")
		except IOError:
			print("fail to open features file: " + features_file)

	with open(out_sum_file, "a") as out:
		header = "file_names, " + ", ".join(os.listdir(features_folder_dir)) + '\n'
		out.write(header)
		for k, v in feature_sum_dict.items():
			line = k + ',' + ",".join(v) + '\n'
			out.write(line)


if __name__ == "__main__":
	
	def boolean_string(s):
	    if s not in {'False', 'True'}:
	        raise ValueError('Not a valid boolean string')
	    return s == 'True'

	import argparse
	parser = argparse.ArgumentParser(description='count the features in different corpus')
	parser.add_argument('corpus_path', type=str,
                    help='the path to corpus folder')
	parser.add_argument('features_path', type=str,
                    help='the path to features folder')
	parser.add_argument('is_variant', type=boolean_string,
                    help='is this a variant value: input has to be: False/True')
	args = parser.parse_args()
	main(args.corpus_path, args.features_path, args.is_variant)
	
