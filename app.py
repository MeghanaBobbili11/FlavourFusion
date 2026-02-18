
import streamlit as st
import random
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")


def get_joke():
    jokes = [
        "Why don't programmers like nature? It has too many bugs.",
        "Why do Java developers wear glasses? Because they don't see sharp.",
        "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "Why did the developer go broke? Because he used up all his cache.",
        "Why do programmers mix up Christmas and Halloween? Because Oct 31 == Dec 25.",
        "Why was the computer cold? It left its Windows open."
    ]
    return random.choice(jokes)


def recipe_generation(user_input, word_count):

    st.write("⏳ Generating your recipe...")
    st.write(
        f"While I work on creating your blog, here’s a little joke to keep you entertained:\n\n😂 {get_joke()}"
    )

    prompt = f"""
    Write a detailed and engaging recipe blog on the topic: {user_input}.
    The blog should be approximately {word_count} words long.

    Structure the blog as follows:
    - Catchy Title
    - Serves, Prep Time, Cook Time
    - Ingredients
    - Step-by-step Instructions (numbered)
    - Tips
    - Serving Suggestions
    - Engaging Conclusion
    """

    try:
        response = model.generate_content(prompt)
        st.success("🎉 Your recipe is ready!")
        return response.text

    except Exception as e:
        st.error(f"Error generating recipe: {e}")
        return None


st.set_page_config(page_title="Flavour Fusion", page_icon="🍲", layout="centered")

st.title("🍲 Flavour Fusion: AI-Driven Recipe Blogging")
st.write("🤖 Hello! I’m Flavour Fusion, your friendly AI chef. Let’s create a fantastic recipe together!")

topic = st.text_input("Topic", placeholder="e.g., Vegan Chocolate Cake")
word_count = st.number_input("Number of words", min_value=200, max_value=2000, value=800, step=100)

if st.button("Generate Recipe"):

    if topic.strip() == "":
        st.warning("Please enter a recipe topic.")
    else:
        with st.spinner("Cooking up something delicious... 🍳"):
            blog_content = recipe_generation(topic, word_count)

        if blog_content:
            st.markdown("---")
            st.markdown(blog_content)

            st.download_button(
                label="📥 Download Recipe",
                data=blog_content,
                file_name=f"{topic.replace(' ', '_')}_recipe.txt",
                mime="text/plain"
            )
