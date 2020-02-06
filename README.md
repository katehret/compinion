# Compinion: Analysing complexity and subjectivity

## Replication data and scripts for: Ehret, Katharina and Maite Taboada (in preparation). The interplay of complexity and subjectivity in opinionated discourse. To be submitted to: Discourse Studies.

This repository contains the following resources:

1. Subjectivity. This folder contains the lists of argumentation and subjectivity markers used for measuring the concept subjectivity in Ehret & Taboada (in preparation). It contains two subfolders

- other_features: stance adverbials.csv, connectives.csv and modals.csv

- socal_features: socal_invariant, socal_variant

other_features contains lists of stance adverbials, connectives and modals which are "invariant features", i.e. they cannot take different forms.
socal_features contains lists of positive and negative adverbs, which classify as "invariant features" as well as negative and positive adjectives, nouns and verbs, which classify as "variant features", i.e. they can take different forms such as plural, comparative or third person singular. All positive and negative features were taken from SOCAL (REF) and have a valency of |4| and |5|.

2. Scripts. This folder contains the scripts for data generation, clean-up and the retrieval of the subjectivity markers.

- sub_marker.py: This script retrieves the raw text frequencies of the above listed argumentation and subjectivity markers.
