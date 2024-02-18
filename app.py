# Importing libraries

import os
import streamlit as st
import openai
from dotenv import load_dotenv
import requests
from PIL import Image

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate a 100words short story based on user title
# Take the prompt of the user and generate a short story using gpt-3.5
# return 100words story text
def story_ai_gpt35_turbo(msg):
    story_response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages = [
            {
                'role': 'system', 
                'content':"You are a bestseller story teller. Take the user input and generate an interesting 100 words-short-story for children picture book."
            },
            { 
                'role':'user',
                'content': f'{msg}'
            }
        ] ,
        temperature = 1.3,
        max_tokens = 300
    )
    story = story_response.choices[0].message.content
    return story

# Function to generate a book cover image
# return a url for us to display the image
def coverPhoto_ai(msg):
    response = openai.images.generate(
        model='dall-e-2',
        prompt = f' {msg} in van gogh style',
        n=1, # dalle2 generate up to 10 img (n=10), dalle3 generate 1 (n=1)
        size='256x256',
        quality='standard'
    )
    image_url = response.data[0].url
    return image_url


# Function to generate prompt to be used to generate book cover image
# based on the 100words story
# Using Turbo-Instruct as replacement of Davinci
# return 20words prompt for us to generate book cover image
def prompt_coverPhoto_ai(story):
    # generate a concise and descriptive prompt for us to generate the cover
    a = "Generate a one sentence with no more than 20 words, descriptive and concise image prompt for the cover of this story: {}".format(story)
    response = openai.completions.create(
        model='gpt-3.5-turbo-instruct',
        prompt=a,
        temperature=1.3,
        max_tokens=60
    )
    # print(a)
    cover_prompt = response.choices[0].text
    return cover_prompt

# Main function for Streamlit app
def main():
    st.title('AI Story Book Generator')

    # User Input
    with st.sidebar:
        user_input = st.text_area("Enter a title for your story:", height=100)
        submit_button = st.button("Generate Story")

    # Process user input
    if submit_button and user_input:
        with st.spinner("Generating your story"):
            story = story_ai_gpt35_turbo(user_input)
            coverPhoto_prompt = prompt_coverPhoto_ai(story)
            image_url = coverPhoto_ai(coverPhoto_prompt)

        # Display the story and the cover photo
        st.header("Your generated story")
        st.write(story)

        st.header("Generated Book Cover")
        img = Image.open(requests.get(image_url,stream=True).raw)
        st.image(image=img, caption="Book Cover")


if __name__ == '__main__':
    main()