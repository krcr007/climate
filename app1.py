import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import CSVLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Set up the OpenAI API key
api_openai = "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"
llm = ChatOpenAI(api_key=api_openai)

# Set the title of the Streamlit app
st.title('Climate Change Report Generator')

# Upload the CSV file
csv_file_upload = st.file_uploader('Choose a CSV file', type=['csv'])

# If a CSV file is uploaded, load and process the data
if csv_file_upload is not None:
    # Load the CSV data using LangChain CSVLoader
    data = CSVLoader(csv_file_upload).load()

    # Display the uploaded data as a table
    st.write("Uploaded Data:", data)

    # Define the prompt template for generating the climate report
    prompt_template = """You are a expert Report maker and also a climate expert. The provided dataset will be related to how the temperature has changed over the years. Your job is to make the report on how the climate has changed and predict how it can cause harm to human life."""

    # Set up the final ChatPromptTemplate
    prompt_template_final = ChatPromptTemplate(
        [
            prompt_template,
            ("user", "{question}")
        ]
    )

    # Get the user input question (optional if you want the user to ask questions)
    question = st.text_input("Enter your question related to climate change (optional)")

    # If the user provides a question, we use it, otherwise we stick to the default report task
    if question:
        user_question = question
    else:
        user_question = "Please analyze the dataset and provide a report on climate change and its potential effects."

    # Create the LLMChain with the prompt template and model
    chain = llm|prompt_template_final

    # Call the chain with the dataset and user question to get the report
    if st.button('Generate Climate Report'):
        with st.spinner('Generating report...'):
            # Generate the response using the LLM
            response = chain.run({"question": user_question})

            # Display the generated climate report
            st.write("Generated Climate Report:")
            st.write(response)

