import pandas as pd
import streamlit as st
import datetime
import random

# Load data
data = pd.read_csv('bible_data_set_with_topics.csv')


# Define the mapping of topic numbers to names
topic_mapping = {
    0: 'Heavenly Knowledge',
    1: 'Faith and Belief',
    2: 'Physical and Spiritual Existence',
    3: 'Love and Relationships',
    4: 'Great Deeds and Sacrifices',
    5: 'Life and Death',
    6: 'Holiness and Sin',
    7: 'Coming of Life',
    8: 'Work of Christ',
    9: 'Laws and Kingdom',
}


# Define functions
def search_verses(word):
    verses = data[data['text'].str.contains(word, case=False)]
    # Sample from the first, middle, and last sections of the dataframe
    first_section = verses[:len(verses)//3].sample(3)
    middle_section = verses[len(verses)//3:2*len(verses)//3].sample(3)
    last_section = verses[2*len(verses)//3:].sample(4)
    return pd.concat([first_section, middle_section, last_section])

def get_verses_by_topic(topic):
    verses = data[data['topic'] == topic]
    # Sample from the first, middle, and last sections of the dataframe
    first_section = verses[:len(verses)//3].sample(3)
    middle_section = verses[len(verses)//3:2*len(verses)//3].sample(3)
    last_section = verses[2*len(verses)//3:].sample(4)
    return pd.concat([first_section, middle_section, last_section])


def get_book(book):
    verses = data[data['book'] == book]
    return verses


def get_daily_devotional(data):
    today = datetime.date.today() 
    random.seed(today.toordinal())
    verse = data.sample(n=1, random_state=today.toordinal())
    citation = f"{verse['book'].values[0]} {verse['chapter'].values[0]}:{verse['verse'].values[0]}"
    text = verse['text'].values[0]
    return citation, text

# Set the title
st.title("Bible Study App")

# Create columns for layout
st.sidebar.header('Search Options')
user_choice = st.sidebar.radio('Choose an option:', ('Search Keyword/Theme', 'Get Book', 'Search by Topic'))
 
# Display daily devotional
citation, text = get_daily_devotional(data)
st.header('Daily Devotional')
st.markdown(f"**Today's Verse ({citation}):** {text}")



if user_choice == 'Search Keyword/Theme':
    search_input = st.text_input('Enter text to search Bible verses:')
    if search_input:
        verses = search_verses(search_input)
        if not verses.empty:
            for index, row in verses.iterrows():
                st.write(f"{row['book']} {row['chapter']}:{row['verse']} , {row['text']}")
        else:
            st.write('No verses found containing the given word.')

elif user_choice == 'Get Book':
    book_input = st.text_input('Enter the name of the book:')
    if book_input:
        verses = get_book(book_input)
        if not verses.empty:
            for index, row in verses.iterrows():
                st.write(f"{row['book']} {row['chapter']}:{row['verse']} , {row['text']}")
        else:
            st.write('No verses found from the given book.')

elif user_choice == 'Search by Topic':
    topic_input = st.selectbox('Choose a topic:', list(topic_mapping.values()), key='topic_input')

    if topic_input:
        # Here, we're getting the numerical ID of the topic that corresponds to the topic name.
        topic_id = list(topic_mapping.keys())[list(topic_mapping.values()).index(topic_input)]
        verses = get_verses_by_topic(topic_id)
        if not verses.empty:
            for index, row in verses.iterrows():
                st.write(f"{row['book']} {row['chapter']}:{row['verse']} , {row['text']}")
        else:
            st.write('No verses found for the selected topic.')

if __name__ == "__main__":

    st.sidebar.header('Bible Study App')
    st.sidebar.markdown("""
    This app allows you to explore Bible verses either by searching for a specific word, getting a specific book, or by selecting a topic of interest. 
    Whether you're here for study, inspiration, or curiosity, we hope you find what you're looking for.

    _**Note:** The results are based on the King James Version of the Bible._

    *Developed by Dennis Mwangi (whatsapp : 0768022630)*
    """, unsafe_allow_html=True)
