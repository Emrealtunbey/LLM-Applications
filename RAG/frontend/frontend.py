import streamlit as st
import requests

st.title("RAG Chat bot")

question = st.text_input("Sorunu sor")

if st.button("Sor"):
    response = requests.post(
        "http://backend:8000/askLLM",
        json={"user_input": question}
    )
    st.write(response.json()["answer"])