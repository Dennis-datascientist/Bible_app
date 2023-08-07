# Bible Verse Topic Modelling

This repository contains code for a Bible study project that uses topic modelling to assign topics to Bible verses. The main model used is the Latent Dirichlet Allocation (LDA) from the `gensim` Python library.

## How It Works

1. Preprocessing: The text of the Bible is cleaned and prepared for modelling. This involves tokenization, removing stop words, and lemmatization.
2. Topic Modelling: An LDA model is trained on the preprocessed text, learning to assign each verse to one of 10 topics.

## Running the Code

To run the code, you will need Python 3.x and the following libraries:
- pandas
- gensim
- nltk
- sklearn

## Output

The output of the model is a CSV file where each Bible verse has been assigned a topic. This is saved as `bible_data_set_with_topics.csv`.

# Bible Study App

This is a web app created with Streamlit that allows users to explore Bible verses by searching for specific words or by selecting a topic of interest.

## Features

- Search for Verses: Enter a word or phrase and the app will return all verses containing that word or phrase.
- Explore by Topic: Choose a topic from the dropdown menu to see all verses that have been assigned to that topic by our topic model.

## Running the App

To run the app, you will need Python 3.x and the following libraries:
- streamlit
- pandas

You can run the app with the command `streamlit run app.py`.

## Deployment

The app is designed to be easily deployed on any web hosting service that supports Python,

## Acknowledgements

The Bible text used in this app is from the King James Version. The topic assignments were made using an LDA model trained on the text of the Bible.


