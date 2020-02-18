# Read Me and instructions for countFeat.py


This script retrieves all markers of subjectivity and argumentation described in the related publication. The complete lists of markers are available from this repository (see **Subjectivity**). 

Note that all paths are hard-coded:

* the paths to the feature lists are hard-coded according to the hierarchy of the folder **Subjectivity** where all lists are stored. Do not change the hierarchy of this folder. 

* the script should be placed


To run the script from the command line use python3.x as follows:

``` 
> python3 countFeat.py "path to corpus directory"
```

#### Output structure

The output will follow the below hierarchy:

	- results
 	 - other_counts
  	 - socal_counts
    		- invariant
    		- variant
  	- total_counts
    		- other
    		- socal

#### Description of output files

- other_counts will contain 3 .csv files for adverbials, connectives and modals with separate counts for each word per file.
- socal_counts/invariant will contain files for positive and negative adverbs with separate counts for each word per file.
- socal_counts/variant will contain files for positive and negative adjectives, nouns and verbs with separate counts for each word per file.
- total_counts/other will contain files for each type of adverbial, connective and modal feature with the sum of that feature for each file. 
- total_counts/socal will contain files for each type of positive and negative adjective, noun and verb feature with the sum of that feature for each file. 
- total_counts also contains an aggregate_totals.csv file with all the pertinent information. Note that the token count in this file is performed by deleting punctuation and joining to the previous word:
-- don't -> dont
-- the end. And -> the end And
