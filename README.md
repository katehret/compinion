# Compinion: Analysing complexity and subjectivity

#### Replication data and scripts for: The interplay of complexity and subjectivity in opinionated discourse. (version 1.0)

### Description

This repository comprises the original data, scripts and extensive statistics for the analysis of text complexity and subjectivity described in the related publication

* Ehret, Katharina, and Maite Taboada (submitted). "The interplay of complexity and subjectivity in opinionated discourse. *Discourse Studies*. 

This publication is a large-scale, quantitative analysis of text complexity and various markers of subjectivity in opinionated discourse. Specifically, the authors investigate how text complexity interacts with markers of subjectivity to characterise (i) opinion articles, (ii) reader comments, and (iii) news articles. Methodologically, conditional inference trees and random forests are used to unravel the interactions between text complexity and subjectivity. Text complexity is defined in terms of Kolmogorov complexity, i.e., the complexity of a text is measured as the length of the shortest possible description necessary to regenerate the original text. Subjectivity is operationalised as the frequency of lexico-grammatical markers of subjectivity and argumentation which have been well-established in research on sentiment, evaluation, stance and Appraisal. 

The data published in this repository was retrieved from the [Simon Fraser University opinion and comments corpus] (https://github.com/sfu-discourse-lab/SOCC) (SOCC) and a custom-made corpus of general news articles from the Canadian online newspaper [The Globe and Mail](https://www.theglobeandmail.com/). 


### Overview and description of folders and files

This repository contains the following resources:

1. Subjectivity. This folder contains the lists of argumentation and subjectivity markers used for measuring the concept subjectivity in Ehret & Taboada (in preparation). It contains two subfolders

* other_features: stance adverbials.csv, connectives.csv and modals.csv

* socal_features: socal_invariant, socal_variant

other_features contains lists of stance adverbials, connectives and modals which are "invariant features", i.e. they cannot take different forms.
socal_features contains lists of positive and negative adverbs, which classify as "invariant features" as well as negative and positive adjectives, nouns and verbs, which classify as "variant features", i.e. they can take different forms such as plural, comparative or third person singular. All positive and negative features were taken from SOCAL (REF) and have a valency of |4| and |5|.

2. Scripts. This folder contains the scripts for data generation, clean-up and the retrieval of the subjectivity markers.

* sub_marker.py This script retrieves the raw text frequencies of the above listed argumentation and subjectivity markers.

3. Statistics
