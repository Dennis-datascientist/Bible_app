import pandas as pd
import streamlit as st

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
    return verses

def get_verses_by_topic(topic):
    verses = data[data['topic'] == topic]
    return verses

# Streamlit app layout and logic
st.set_page_config(
    page_title="Bible Study App",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Set the title
st.title("Bible Study App")

# Create columns for layout
col1, col2 = st.columns(2)



with col1:
    st.header("Search Verses")
    st.write("Enter a word or phrase to search for it in the Bible.")
    search_input = st.text_input('', key='search_input')

    if st.button('Search'):
        verses = search_verses(search_input)
        if not verses.empty:
            st.subheader("Search Results:")
            for index, row in verses.iterrows():
                st.info(f"**{row['book']} {row['chapter']}:{row['verse']}**\n{row['text']}")
        else:
            st.error('No verses found containing the given word.')

with col2:
    st.header("Explore by Topic")
    st.write("Select a topic to see related verses.")
    topic_input = st.selectbox('', list(topic_mapping.values()), key='topic_input')

    if st.button('Explore'):
        verses = get_verses_by_topic(list(topic_mapping.keys())[list(topic_mapping.values()).index(topic_input)])
        if not verses.empty:
            st.subheader("Topic Verses:")
            for index, row in verses.iterrows():
                 st.info(f"**{row['book']} {row['chapter']}:{row['verse']}**\n{row['text']}")
        else:
            st.error('No verses found for the given topic.')
# Display information about the app at the end of the page
st.markdown("""
This app allows you to explore Bible verses either by searching for a specific word or by selecting a topic of interest. 
Whether you're here for study, inspiration, or curiosity, we hope you find what you're looking for.

_**Note:** The results are based on the King James Version of the Bible._

*Developed by Dennis Mwangi (whatsapp : 0768022630)*
""", unsafe_allow_html=True)
