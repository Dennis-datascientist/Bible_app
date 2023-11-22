
import pandas as pd
import streamlit as st
import datetime
import random
import openai
import os
from streamlit_elements import elements, mui, html


openai.api_key = st.secrets["general"]["OPENAI_KEY"]

# Theming for serene and calm colors
primaryColor = "#6c757d"
backgroundColor = "#f8f9fa"
secondaryBackgroundColor = "#ffffff"
textColor = "#000000"
font = "sans serif"

st.set_page_config(layout="wide", page_title="Bible Study App", page_icon=":book:")

# Custom CSS for the theme
st.markdown(
    f"""
    <style>
        .reportview-container .main .block-container{{
            max-width: 90%;
            padding-top: 5rem;
            padding-right: 5rem;
            padding-left: 5rem;
            padding-bottom: 5rem;
        }}
        .reportview-container .main {{
            color: {textColor};
            background-color: {backgroundColor};
        }}
        .sidebar .sidebar-content {{
            background-color: {secondaryBackgroundColor};
        }}
        header .decoration {{
            background-color: {primaryColor};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page:", ["Home", "Search by Book", "Search by Topic", "Daily Devotional", "Ask the Model"])

# Load data
data = pd.read_csv('bible_data_set_with_topics.csv')

# Define functions
def generate_summary(verse):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize this bible verse: {verse}",
        temperature=0.5,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0, 
        presence_penalty=0.0
    )
    return response["choices"][0]["text"]

verse_input = st.text_input("Enter verse:")
if st.button("Summarize"):
    summary = generate_summary(verse_input)
    st.write(summary)
# Define functions
def generate_follow_up(verse, user_response):
    if len(user_response) < 120:
        new_prompt = f"The user responded: {user_response}\n\nGenerate a follow-up discussion prompt about {verse}:"
        ai_followup = openai.Completion.create(
            engine="text-davinci",
            prompt=new_prompt,
        )
        return ai_followup["choices"][0]["text"]
    else:
        # user gave enough input, no follow up needed
        return "You gave a comprehensive response. No follow-up is needed."

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
with elements("welcome_msg"):
    mui.Typography("Welcome to the Bible Study App with AI Assistance", variant="h4")


# Create columns for layout
st.sidebar.header('Search Options')
user_choice = st.sidebar.radio('Choose an option:', 
                               ( 'Home', 
                                'Search by Book', 
                                'search by Topic',
                                'Daily Devotional',
                                'Ask the model')) 



# Main app layout
if page == "Home":
    st.title("Welcome to the Bible Study App")
    st.markdown("Explore Bible verses, understand different topics, and engage with AI for insights.")
    # Any additional content for the home page...

elif page == "Search by Book":
    st.title("Search by Book")
    book_input = st.text_input('Enter the name of the book:')
    if st.button('Search'):
        with st.spinner('Searching...'):
            if book_input:
                verses = get_book(book_input)
                if not verses.empty:
                    for index, row in verses.iterrows():
                        st.write(f"{row['book']} {row['chapter']}:{row['verse']} , {row['text']}")
                else:
                    st.write('No verses found for the given book.')
            else:
                st.warning("Please enter a book name before searching.")

elif page == "Search by Topic":
    st.title("Search by Topic")
    topic_input = st.selectbox('Choose a topic:', list(topic_mapping.values()))
    if topic_input:
        topic_id = list(topic_mapping.keys())[list(topic_mapping.values()).index(topic_input)]
        verses = get_verses_by_topic(topic_id)
        if not verses.empty:
            for index, row in verses.iterrows():
                st.write(f"{row['book']} {row['chapter']}:{row['verse']} , {row['text']}")

elif page == "Daily Devotional":
    st.title("Daily Devotional")
    citation, text = get_daily_devotional(data)

    # Responsive layout with two columns
    col1, col2 = st.beta_columns([1, 2])  

    with col1:
        st.markdown("**Today's Verse**")
        st.markdown(f"**{citation}**")

    with col2:
        st.markdown("**Verse Explanation:**")
        st.markdown(text)


elif page == "Ask the Model":
    st.title("Ask the Model")
    st.markdown("You can ask the model questions about a particular verse, topic, or general Bible-related inquiries.")
    user_question = st.text_input('Enter your question:')
    if st.button('Generate Response'):
        with st.spinner('Generating AI response...'):
            if user_question:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=user_question,
                    temperature=0.5,
                    max_tokens=2000
                )
                st.write(response.choices[0].text.strip())


st.markdown(
"""
## Ask the Model
You can ask the model questions about a particular verse, topic, or general Bible-related inquiries. Here are some examples:
- "Can you explain the concept of faith in the Bible?"
- "What is the significance of the resurrection of Jesus Christ? cite from bible 6 verses"
"""
)



# Input + Button
user_question = st.text_input('Enter your question:')
regenerate_button = st.button('Generate Response')

# Loading animation while generating response
with st.spinner('Generating AI response...'):
    if regenerate_button and user_question:
        response_a = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_question,
            temperature=0.5,
            max_tokens=2000
        )
        st.write(response_a.choices[0].text.strip())

# Feedback
feedback_options = ['Very Useful', 'Somewhat Useful', 'Not Useful']
selected_feedback = st.radio("Was the AI's response helpful?", feedback_options)
if selected_feedback:
    st.markdown(f"Thank you for the feedback!")

import matplotlib.pyplot as plt

# Example function to create a simple bar chart
def plot_theme_frequency(data):
    theme_counts = data['theme'].value_counts()
    plt.figure(figsize=(10,6))
    plt.bar(theme_counts.index, theme_counts.values)
    plt.xlabel('Themes')
    plt.ylabel('Frequency')
    plt.title('Frequency of Bible Themes')
    return plt

if page == "Theme Analysis":
    st.title("Bible Theme Analysis")
    chart = plot_theme_frequency(data)
    st.pyplot(chart)



if __name__ == "__main__":

    st.sidebar.markdown(
"""
## Capabilities and Limitations

### Capabilities
1. The application can search Bible verses, topic, or book name.
2. The application allows users to engage in a conversation with an AI  about a specific verse or topic.
3. The application can generate a summary of a selected verse.
4. The application presents a new daily devotional verse each day.

### Limitations
1. The AI generates responses based on training data, and it might not always provide accurate theological insights.
2. The verse summary function is an automated process and the quality of the summary depends on the AI's understanding of the verse.
4. Questions asked to the AI should be structured properly to get meaningful responses.

    Developed by Dennis Mwangi (whatsapp : 0768022630)
"""
)
