import re
import os
import pandas as pd
import sys

def countInvariants(featurePath, dataPath, outFolder):
    """Count occurences of invariant features in the data

    args:
            featurePath: path to directory containing the feature files
            dataPath: path to directory containing data files

    return:
            csv files containing counts of each feature
    """
    # set variables for output path
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)
    
    dataFiles = os.listdir(dataPath)

    # first for loop loops over each feature file
    for featureFile in os.listdir(featurePath):
        if featureFile.split('.')[-1] != "csv":
            continue
        # try to open feature file, else throw error
        try:
            features = pd.read_csv(featurePath + '/' + featureFile)
            # write headers to csv file
            with open(outFolder + "/" + featureFile.split('/')[-1], "a") as out:
                out.write("words," + ",".join(dict(zip(list(features.ix[:,0]), [0]*len(list(features.ix[:,0])))).keys()) + "\n")
            # second for loop loops over data files
            for file in dataFiles:
                totalFeatures = 0
                result = file
                # try to open data file, else throw error
                try:
                    with open(dataPath + '/' + file) as f:
                        data = f.read()
                    # final for loop loops through features to count occurences in data file
                    for feature in list(features.ix[:,0]):
                        featureSum = len(re.findall('\\b' + feature + '\\b', data))
                        result += "," + str(featureSum)
                        totalFeatures += featureSum
                except IOError:
                    print("failed to open the file: " + file)

                with open(outFolder + "/" + featureFile.split('/')[-1], "a") as out:
                    out.write(result + "\n")
        except IOError:
            print("failed to open the feature file: " + featureFile)

def countVariants(featurePath, dataPath, outFolder):
    from nltk.stem import WordNetLemmatizer
    from nltk import pos_tag
    from nltk.tokenize import word_tokenize
    TAG_POS_DICT_ADJ = {"JJ": 'a', "JJR": 'a', "JJS": 'a'}
    TAG_POS_DICT_VERB = {"VB":'v', "VBD":'v', 'VBG':'v', 'VBN': 'v', 'VBP':'v', 'VBZ':'v'}
    TAG_POS_DICT_NOUN = {'NN':'n', 'NNS':'n', 'NNP':'n', 'NNPS':'n'}
    TAG_POS_DICT = {'a':TAG_POS_DICT_ADJ, 'v': TAG_POS_DICT_VERB, 'n': TAG_POS_DICT_NOUN}

    if not os.path.exists(outFolder):
        os.makedirs(outFolder)
    
    files = os.listdir(dataPath)

    for featuresFile in os.listdir(featurePath):
        if featuresFile.split('.')[-1] != "csv":
            continue
        try:
            features = pd.read_csv(featurePath + '/' + featuresFile)
            with open(outFolder + "/" + featuresFile.split('/')[-1], "a") as out:
                out.write("words," + ",".join\
                    (dict(zip(list(features.ix[:,0]), [0]*len(list(features.ix[:,0])))).keys()) + "\n")
            for file in files:
                result = file
                try:
                    with open(dataPath + '/' + file) as f:
                        text = f.read()
                    featureType = featuresFile[0]
                    DICT = TAG_POS_DICT[featureType]
                    text = re.sub(r'\xe2\x80\x9c', ' ', text)
                    text = re.sub(r'\xe2\x80\x93', ' ', text)
                    tokens = word_tokenize(text)
                    tokensPOS = pos_tag(tokens)
                    lemmatizer = WordNetLemmatizer()
                    featureCount = dict(zip(list(features.ix[:,0]), [0]*len(features)))
                    for token in tokensPOS:
                        word, tag = token
                        if tag in DICT:
                            wordLemma = lemmatizer.lemmatize(word, DICT[tag])
                            if wordLemma in featureCount:
                                featureCount[wordLemma] += 1
                    counts = featureCount.values()
                    result += "," + ",".join([str(c) for c in counts])
                except IOError:
                    print("failed to open the file: " + file)
            
                with open(outFolder + "/" + featuresFile.split('/')[-1], "a") as out:
                    out.write(result + "\n")
        except IOError:
            print("failed to open the features file: " + featuresFile)      


def totalCount(dataPath, outPath):
    outFolder = outPath
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)

    for file in os.listdir(dataPath):
        df = pd.read_csv(dataPath + "/" + file)
        with open(outFolder + "/" + file.split('.')[0] + "_totals.csv", "a") as out:
            out.write("file," + file.split('.')[0] + "_totals" + "\n")
            i = 0
            for line in df.sum(axis = 1, numeric_only = True):
                out.write(str(df.iloc[i]['words']) + "," + str(line) + "\n")
                i += 1

# Input: path to the folder containing the corpus
# Output: file containing 
def aggregateTotals(dataPath):
    import string
    with open("./Subjectivity/results/total_counts/aggregate_totals.csv", "a") as out:
        out.write("filename,textType,year,tokens" + "\n")
    for file in os.listdir(dataPath):
        with open(dataPath + '/' + file) as f:
            data = f.read()
        data = data.translate(str.maketrans('', '', string.punctuation))
        total = file + "," + file[:min([ind for ind in [file.find(str(num)) for num in range(0,10)] if ind > 0])]
        total += "," + file[min([ind for ind in [file.find(str(num)) for num in range(1,10)] if ind > 0]):min([ind for ind in [file.find(str(num)) for num in range(1,10)] if ind > 0])+4]
        total += "," + str(len(data)) + "\n"
        with open("./Subjectivity/results/total_counts/aggregate_totals.csv", "a") as out:
            out.write(total)

    # add columns for adverbials, connectives and modals
    for file in os.listdir("./Subjectivity/results/total_counts/other"):
        df = pd.read_csv("./Subjectivity/results/total_counts/other/" + file)
        dg = pd.read_csv("./Subjectivity/results/total_counts/aggregate_totals.csv")
        dg[file.split("_")[0] + "_raw"] = df.iloc[ : , 1]
        dg.to_csv("./Subjectivity/results/total_counts/aggregate_totals.csv", index=False)
    
    # sum adverbials, connectives and modals
    df = pd.read_csv("./Subjectivity/results/total_counts/aggregate_totals.csv")
    df["argumentativeMarkers_raw"] = df.iloc[ : , 4:7].sum(axis=1)
    df.to_csv("./Subjectivity/results/total_counts/aggregate_totals.csv", index=False)

    # sum negative subjective markers
    temp = pd.DataFrame()
    for file in os.listdir("./Subjectivity/results/total_counts/socal"):
        if file.split("_")[1] == "negative":
            df = pd.read_csv("./Subjectivity/results/total_counts/socal/" + file)
            temp[file] = df.iloc[ : , 1]
    dg = pd.read_csv("./Subjectivity/results/total_counts/aggregate_totals.csv")
    dg["subjectiveNegative_raw"] = temp.iloc[ : , 0:4].sum(axis=1)
    dg.to_csv("./Subjectivity/results/total_counts/aggregate_totals.csv", index=False)

    # sum positive subjective markers
    temp = pd.DataFrame()
    for file in os.listdir("./Subjectivity/results/total_counts/socal"):
        if file.split("_")[1] == "positive":
            df = pd.read_csv("./Subjectivity/results/total_counts/socal/" + file)
            temp[file] = df.iloc[ : , 1]
    dg = pd.read_csv("./Subjectivity/results/total_counts/aggregate_totals.csv")
    dg["subjectivePositive_raw"] = temp.iloc[ : , 0:4].sum(axis=1)
    dg.to_csv("./Subjectivity/results/total_counts/aggregate_totals.csv", index=False)

    # sum subjective markers
    df = pd.read_csv("./Subjectivity/results/total_counts/aggregate_totals.csv")
    df["subjectiveMarkers_raw"] = df.iloc[ : , 8:10].sum(axis=1)
    df.to_csv("./Subjectivity/results/total_counts/aggregate_totals.csv", index=False)


def main(corpusFolderDir):
    countInvariants("./Subjectivity/other_features", corpusFolderDir, "./Subjectivity/results/other_counts")
    countInvariants("./Subjectivity/socal_features/socal_invariant", corpusFolderDir, "./Subjectivity/results/socal_counts/invariant")
    countVariants("./Subjectivity/socal_features/socal_variant", corpusFolderDir, "./Subjectivity/results/socal_counts/variant")
    totalCount("./Subjectivity/results/other_counts", "./Subjectivity/results/total_counts/other")
    totalCount("./Subjectivity/results/socal_counts/invariant", "./Subjectivity/results/total_counts/socal")
    totalCount("./Subjectivity/results/socal_counts/variant", "./Subjectivity/results/total_counts/socal")
    aggregateTotals(corpusFolderDir)
    return 0

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='count the features in different corpus')
    parser.add_argument('corpus_path', type=str, help='the path to corpus folder')
    args = parser.parse_args()

    main(args.corpus_path)
