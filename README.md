# 🧠 Local RAG Chat with LangChain

A simple command-line chatbot powered by **LangChain**, **FAISS**, and **OpenAI**, designed to answer your questions using your **local notes**.

This project implements a lightweight version of Retrieval-Augmented Generation (RAG), where you can ask questions and get answers grounded in your `.txt` files — all stored locally.


## 📦 Features

- Load and chunk local notes from a folder
- Embed notes using OpenAI embeddings
- Store vectors locally with FAISS
- Ask natural-language questions from the terminal
- Get responses enhanced by your notes

## 🧩 Built With
- LangChain
- FAISS
- OpenAI Embeddings & Chat Models
- Python 3.9+

## 📌 Roadmap
 - [ ] Support Notion, PDF, and web article loaders
 - [ ] Add a simple UI with Streamlit
 - [ ] Enable fully offline mode (local LLM + HuggingFace embeddings)


## 🛠️ Installation

1. **Clone the repo** (or create your own project directory):

```bash
git clone https://github.com/your-username/local-rag-chat.git
cd local-rag-chat
```

2. **Install dependencies**:

```
pip install -r requirements.txt
```

3. **Set up your OpenAI API key**:
```
// .env
OPENAI_API_KEY=sk-your-openai-api-key
```

## 📝 Feeding Your Notes
Place your .txt files in a folder named notes/ in the root of the project:
```
local-rag-chat/
├── main.py
├── .env
└── notes/
    ├── note1.txt
    └── note2.txt
```
You can update or add new files anytime — just rerun the app to refresh the knowledge base.

## How to Run
Run the chatbot from the terminal:
```
python main.py
```

Then just type your question:
```
🧠 Ask me anything based on your notes (type 'exit' to quit)
You: what keytakes that i write in psychology of money summary
🤖: {'query': 'what keytakes that i write in psychology of money summary', 'result': 'Based on the provided context, the keytakes you can include in a summary of "The Psychology of Money" are:\n\n1. Financial decisions are influenced by personal life experiences and worldview.\n2. Understanding and leveraging the power of compounding for long-term financial success.\n3. Avoid letting pessimism cloud your judgment.\n4. Prioritize gaining control over your time when deciding how to use or invest money.\n5. Small number of events can determine outcomes over time.\n6. Success often comes from a few major wins that outweigh losses.\n7. Aim for long-term financial security by accumulating valuable assets rather than material possessions.'}
```
