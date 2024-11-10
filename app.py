# app.py
# In this file, you’ll create the user interface and make HTTP requests to the FastAPI backend to generate outfit images based on user input.


import streamlit as st
import requests

# Function to display AR in Web AR interface
def display_ar_view(image_url):
    ar_html = f"""
    <html>
    <body>
    <script src="https://aframe.io/releases/1.2.0/aframe.min.js"></script>
    <script src="https://jeromeetienne.github.io/AR.js/aframe/build/aframe-ar.min.js"></script>
    <a-scene embedded arjs>
        <a-image src="{image_url}" position="0 0 -2" scale="1 1 1"></a-image>
    </a-scene>
    </body>
    </html>
    """
    st.components.v1.html(ar_html, height=600)

# User input for style or occasion
st.title("Virtual Try-On & Personalized Fashion Stylist")
user_input = st.text_input("Enter an occasion (e.g., 'formal dinner', 'casual day out'):")

if user_input:
    # Send request to the FastAPI backend for outfit generation
    response = requests.post("http://localhost:8000/generate", json={"prompt": user_input})
    image_url = response.json().get("image_url")

    # Display the generated outfit
    st.image(image_url, caption="Generated Outfit")

    # Button to view the outfit in AR
    if st.button("View in AR"):
        display_ar_view(image_url)
