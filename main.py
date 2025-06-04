from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

# Load notes from the local directory
loader = DirectoryLoader("notes", glob="**/*.txt", loader_cls=TextLoader)
documents = loader.load()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# Generate embeddings and store them in FAISS
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)

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
