# Read Me and instructions for countFeat.py


This script retrieves all markers of subjectivity and argumentation described in the related publication. The complete lists of markers are available from this repository (see [Subjectivity](compinion/Subjectivity). 

Note that all paths are hard-coded:

* the paths to the feature lists are hard-coded according to the hierarchy of the folder [Subjectivity](compinion/Subjectivity) where all lists are stored. Do not change the hierarchy of this folder. 

* the script should be placed


To run the script from the command line use python3.x as follows:

``` 
> python3 countFeat.py "path to corpus directory"
```

#### Output structure

The output will follow the below folder hierarchy:

	- results
 	 - other_counts
  	 - socal_counts
    	   - invariant
    	   - variant
  	- total_counts
    	   - other
    	   - socal

#### Description of output folders and files

* other_counts: This folder will contain three .csv files, one each with the filenames of the corpus as rows and the frequencies of the individual stance adverbials, connectives and modals as columns. 

* socal_counts/invariant: This folder will contain two .csv files, one for positive adverbs and one for negative adverbs, with the filenames of the corpus as rows and the frequencies of the individual adverbs as columns.

* socal_counts/variant: This folder will contain six .csv files, one for positive/negative adjectives, positive/negative nouns and positive/negative verbs, respectively. The files have the filenames of the corpus as rows and the frequencies of the individual markers as columns.

* total_counts/other: This folder will contain three files, one per marker type (stance adverbials, connectives, modals), with the total sum of the marker type per corpus file.

* total_counts/socal: This folder will contain files for six files, one per marker type (positive/negative adjectives, positive/negative nouns, positive/negative verbs), with the total sum of the marker type per corpus file. 

* total_counts/aggregate_totals.csv: This file is the final feature matrix comprising the raw feature frequencies for each type of subjectivity and argumentation marker per corpus file. The file also contains columns indicating the text type, year of publication and number of tokens for each corpus file. Note that the token counts were performed by deleting punctuation (e.g. *the end. And* -> *the end And*). Contracted word forms were joined and counted as one word (e.g. *don't* -> *dont*).
