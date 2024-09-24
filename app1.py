import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import CSVLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
import pandas as pd
from io import StringIO

# Set up the OpenAI API key
api_openai = "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"
llm = ChatOpenAI(api_key=api_openai)

# Set the title of the Streamlit app
st.title('Climate Change Report Generator')

# Upload the CSV file
csv_file_upload = st.file_uploader('Choose a CSV file', type=['csv'])

# If a CSV file is uploaded, load and process the data
if csv_file_upload is not None:
    # Read the CSV data into a pandas DataFrame
    string_data = StringIO(csv_file_upload.getvalue().decode('utf-8'))
    data = pd.read_csv(string_data)

    # Display the uploaded data as a table
    st.write("Uploaded Data:", data)

    # Define the prompt template for generating the climate report
    prompt_template = """You are an expert report maker and a climate expert. The provided dataset will be related to how the temperature has changed over the years. Your job is to make the report on how the climate has changed and predict how it can cause harm to human life."""

    # Set up the final ChatPromptTemplate
    prompt_template_final = ChatPromptTemplate(
        messages=[prompt_template]
    )

    # Get the user input question (optional if you want the user to ask questions)
    question = st.text_input("Enter your question related to climate change (optional)")

    # If the user provides a question, we use it, otherwise we stick to the default report task
    if question:
        user_question = question
    else:
        user_question = "Please analyze the dataset and provide a report on climate change and its potential effects."

    # Use the new chaining mechanism with RunnableSequence
    chain = prompt_template_final | llm

    # Call the chain with the dataset and user question to get the report
    if st.button('Generate Climate Report'):
        with st.spinner('Generating report...'):
            # Generate the response using the LLM
            response = chain.invoke({"question": user_question})
            
            # Display the generated climate report
            st.write("Generated Climate Report:")
            st.write(response)
