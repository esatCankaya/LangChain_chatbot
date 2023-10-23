🦜️🔗 LangChain_chatbot
## Introduction
Welcome to the LangChain Chatbot project! This chatbot is designed to answer questions based on a knowladge base and chat memory using an llm model.

## Features
- db_creator.py > to create a vector store from your documents.
- requirements.txt > contains related libraries that are used in this repo
- .env > to store your credentials
- app.py > actual chatbot code
- streamlit_example.py > example streamlit app code to get a User Interface

## Technologies Used
- Python, LangChain, OpenAI, FAISS, Streamlit

## Getting Started
  To use this chatbot you should do the followings:
  
  1. Prerequisites
    - Install the required dependencies listed in requirements.txt
  2. Creating environmental variables
    - Create an .env file that contains your openai api key
  3. Create your knowladge base
    - In order to question your files, first use db_creator.py file to create a vector store from your files.
  4. Using app.py
    - First you should change store_name variable according to your vectorstore name.
    - Now you can change the query inputs to your like and run the app.
  5. Using streamlit_example.py
    - First you should change store_name variable according to your vectorstore name.
    - Now you can run the app using: streamlit run ./streamlit_example.py command.
