import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

def main():
    load_dotenv()
    #st.write("OPENAI_API_KEY:", st.secrets["OPENAI_API_KEY"])
    #os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"]
    st.set_page_config(page_title="Ask your PDF", page_icon="📄", layout="centered", initial_sidebar_state="expanded")
    st.header("Ask your PDF")

    #upload file
    pdf = st.file_uploader("Upload your PDF", type=["pdf"])

    #extract text of the file
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

    
    #split into chunks
        text_splitter = CharacterTextSplitter(separator = "\n",chunk_size = 1000,chunk_overlap = 200,length_function = len)
        chunks = text_splitter.split_text(text)

    #create embeddings

        embeddings = OpenAIEmbeddings()

    #Document's Semantic search

        knowledge_base = FAISS.from_texts(chunks, embeddings)

    #user input capture
        user_question = st.text_input("Ask your question here")
        if user_question:
            docs = knowledge_base.similarity_search(user_question)
    
    #Using Langauage models to construct the answer
            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type ="stuff")
            response = chain.run(input_documents = docs, question = user_question)

            st.write(response)

if __name__ == '__main__':
    main()