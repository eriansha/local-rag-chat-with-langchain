import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA


NOTES_DIR = "notes"
TIMESTAMP_FILE = "file_timestamps.json"
FAISS_INDEX = "faiss_index"

def get_file_timestamps():
    timestamps = {}
    for filename in os.listdir(NOTES_DIR):
        path = os.path.join(NOTES_DIR, filename)
        if os.path.isfile(path):
            modified_time = os.path.getmtime(path)
            timestamps[filename] = modified_time
    return timestamps

def load_previous_timestamps():
    if not os.path.exists(TIMESTAMP_FILE):
        return {}
    with open(TIMESTAMP_FILE, "r") as f:
        return json.load(f)

def save_timestamps(timestamps):
    with open(TIMESTAMP_FILE, "w") as f:
        json.dump(timestamps, f, indent=2)

# compare timestamp on each file and see if it's different or not
# if the timestamp is difference, we can assume the file is updated
# then, we can decide to generate new vector store
def detect_changes(old, new):
    for file, mtime in new.items():
        if file not in old or mtime != old[file]:
            return True

    return False

def embed_document():
    # Load notes from the local directory
    loader = DirectoryLoader("notes", glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # Generate embeddings and store them in FAISS
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    # save index to local
    vectorstore.save_local(FAISS_INDEX)

    return vectorstore

def load_existing_document():
    # generate embeddings and load FAISS Index
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(FAISS_INDEX, embeddings, allow_dangerous_deserialization=True)

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    old_timestamps = load_previous_timestamps()
    new_timestamps = get_file_timestamps()

    is_changes = detect_changes(old_timestamps, new_timestamps)

    save_timestamps(new_timestamps)

    vectorstore = embed_document() if is_changes else load_existing_document()

    # Create a retriever-based QA chain
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0),
        retriever=retriever,
    )

    # Interactive Q&A
    print("🧠 Ask me anything based on your notes (type 'exit' to quit)")
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break
        answer = qa_chain.invoke(query)
        print("🤖:", answer)