import streamlit as st
import tempfile
from loguru import logger
from src.document_processing.populate_db import DocumentPopulator
from src.database.chroma_client import ChromaClient
from src.document_processing.retriever import DocumentRetriever
from src.llm.handler import LLMHandler
from pathlib import Path

def get_existing_collections():
    """Get all the existing collections in the database"""
    try:
        chroma_client = ChromaClient()
        return chroma_client.list_collections()
    except Exception as e:
        logger.error(f"Error getting existing collections: {e}")
        return []

def init_processor():
    """Initialize the processors"""
    if 'doc_processor' not in st.session_state:
        st.session_state['doc_processor'] = DocumentPopulator()
    if 'retriever' not in st.session_state:
        st.session_state['retriever'] = DocumentRetriever()
    if 'llm_handler' not in st.session_state:
        st.session_state['llm_handler'] = LLMHandler()

def init_session_state():
    """Initialize the session state"""
    if 'collections' not in st.session_state:
        st.session_state['collections'] = get_existing_collections()
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []


def upload_document():
    """Upload a document to the database"""
    st.sidebar.header("Upload Document")

    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])
    collection_name = st.sidebar.text_input("collection_name", 
                                            help="Enter a name for the collection")
    
    if uploaded_file and collection_name:
        if st.sidebar.button("Process and Upload"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.getvalue)
                tmp_path = temp_file.name

            try:
                with st.spinner("Processing and uploading document..."):
                    result = st.session_state['doc_processor'].process_file_and_add_to_db(
                        collection_name=collection_name,
                        file_path=tmp_path,
                        reset_collection=False
                    )
                    if "error" not in result:
                        st.session_state['collections'].add(collection_name)
                        st.success(f"Document uploaded to {collection_name} successfully!")
                    else:
                        st.sidebar.error(f"Error processing document: {result['error']}")
            except Exception as e:
                st.sidebar.error(f"An error occurred: {e}")
            finally:
                Path(tmp_path).unlink()

def display_chat_interface():
    """Display the chat interface"""
    st.title("Teaching Assistant")
    st.markdown("Ask questions about the uploaded documents or generate image captions")

    # Test generator
    st.sidebar.header("Test Generator")
    if st.sidebar.button("Generate Test"):
        with st.spinner("Generating test..."):
            test_result = st.session_state['doc_processor'].generate_test()
            st.sidebar.success("Test generated successfully!")
            st.sidebar.write(test_result)

    # Collection selector
    if st.session_state['collections']:
        selected_collection = st.selectbox(
            "Select a collection to chat with",
            st.session_state['collections'],
            index=0 if st.session_state['collections'] else None
        )

        # Chat interface
        for message in st.session_state['messages']:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

        # Chat input
        if prompt := st.chat_input("Ask a question about your document"):
            # Add user message to chat history
            st.session_state['messages'].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get response 
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Get context chunks
                    context = st.session_state['retriever'].get_chunks(
                        query=prompt,
                        collection_name=selected_collection
                    )['documents'][0]

                    if context:
                        # Generate response
                        response = st.session_state['llm_handler'].generate_explanation(
                            question=prompt,
                            context=context
                        )
                        st.markdown(response)
                        st.session_state['messages'].append({"role": "assistant", "content": response})
                    else:
                        st.markdown("No relevant information found in the uploaded documents.")

    else:
        st.markdown("No documents uploaded yet. Please upload a document first.")


def main():
    """Main function to run the app"""
    init_session_state()
    init_processor()

    st.set_page_config(page_title="Teaching Assistant", page_icon=":mortar_board:")
    st.sidebar.title("Teaching Assistant")
    upload_document()

    display_chat_interface()

if __name__ == "__main__":
    main()
    
    


