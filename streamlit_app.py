
import pandas as pd
import streamlit as st
import datetime
import random
import openai
import os

openai.api_key = st.secrets["general"]["OPENAI_KEY"]


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
def summarize_verse(verse_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize this excerpt: {verse_text}",
        temperature=0.7,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response["choices"][0]["text"]
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
st.title("Bible Study App with AI Assistant")

# Create columns for layout
st.sidebar.header('Search Options')
user_choice = st.sidebar.radio('Choose an option:', 
                               ( 'Get Chapter', 
                                'Search by Topic', 
                                'Model Guide')) # added this line

# Display daily devotional
citation, text = get_daily_devotional(data)
st.header('Daily Devotional')
st.markdown(f"**Today's Verse ({citation}):** {text}")



if user_choice == 'Get Chapter':
    book_input = st.text_input('Enter the name of the Chapter:')
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

elif user_choice == 'Model Guide':
    verse_input = st.text_input('Enter the verse you would like to summarize:')
    search_button = st.button('Generate Summary')
    
    if search_button and verse_input:
        summary = summarize_verse(verse_input)
        st.write("Model Guide:")
        st.write(summary)

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
regenerate_button = st.button('Generate Response', icon="search")

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
    st.markdown(f"Thank you for the feedback! You found the response **{selected_feedback}**.")

if __name__ == "__main__":

    st.sidebar.header('Bible Study App')
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
