# Compinion: Analysing complexity and subjectivity

#### Replication data and scripts for: The interplay of complexity and subjectivity in opinionated discourse. (version 1.0)

### Description

This repository comprises the original data, scripts and extensive statistics for the analysis of text complexity and subjectivity described in the related publication

* Ehret, Katharina, and Maite Taboada (submitted). "The interplay of complexity and subjectivity in opinionated discourse. *Discourse Studies*. 

This publication is a large-scale, quantitative analysis of text complexity and various markers of subjectivity in opinionated discourse. Specifically, the authors investigate how text complexity interacts with markers of subjectivity to characterise (i) opinion articles, (ii) reader comments, and (iii) news articles. Methodologically, conditional inference trees and random forests are used to unravel the interactions between text complexity and subjectivity. Text complexity is defined in terms of Kolmogorov complexity, i.e., the complexity of a text is measured as the length of the shortest possible description necessary to regenerate the original text. Subjectivity is operationalised as the frequency of lexico-grammatical markers of subjectivity and argumentation which have been well-established in research on sentiment, evaluation, stance and Appraisal. 

The data published in this repository was retrieved from the [Simon Fraser University opinion and comments corpus] (https://github.com/sfu-discourse-lab/SOCC) (SOCC) and a custom-made corpus of general news articles from the Canadian online newspaper [The Globe and Mail](https://www.theglobeandmail.com/). 


### Overview and description of folders and files

This repository contains the following resources (in alphabetical order):

#### Data
This folder contains the original data.

* aggregate_totals_normalised.csv The feature matrix with the individual file names as rows and textType, year, tokens, the raw and normalised feature frequencies, and the complexity scores as columns. The normalised feature frequencies of the subjectivity and argumentation markers were calculated based on the raw feature frequencies divided by the number of tokens per file and multiplied with 1000.

* markerDistributions.csv The raw frequencies of the individual subjectivity and argumentation markers per text type.

#### Subjectivity
This folder comprises the complete lists of subjectivity and argumentation markers described in the related publication. 

* other_features A folder containing the lists of the argumentation markers adverbials, connectives and modals.

* socal_features A folder with two subdirectories sampling reduced features lists of subjectivity markers from the [*Semantic Orientation CALculator*](https://github.com/sfu-discourse-lab/SO-CAL) (SO-CAL). Specifically, only subjectivity features with a valency of 4 and 5 are included.

  * socal_invariant: negative and positive adverbs.
  * socal_variant: negative and positive adjectives, nouns and verbs.
  
#### Scripts 
This folder contains the scripts for data analysis, clean-up and the retrieval of the subjectivity markers.

#### Statistics
This folder contains the original data set, all statistics described in the related publication and extensive additional stastistics. 
