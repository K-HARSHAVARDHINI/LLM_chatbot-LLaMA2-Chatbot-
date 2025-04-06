🤖 LLM-Powered Chatbot with SQL Integration

Chatbot Name: 🦙 LLaMA2 Chatbot

Page Title: LLaMA2 Chatbot

🧠 Overview
This project showcases a smart chatbot that combines the power of LLaMA2 🦙 with SQL integration, enabling users to interact with a structured SQLite database using natural language. Built with FastAPI and Streamlit, this end-to-end chatbot allows you to query order statuses, product pricing, customer support contacts, and more — all through an intuitive chat interface.

💡 Description
The 🦙 LLaMA2 Chatbot is designed to make data retrieval from SQL databases conversational. The project uses a lightweight, fast, and modular approach, avoiding heavyweight libraries like LangChain to ensure speed and precision.

The chatbot can: - Classify user intent using LLaMA2 via Ollama

        - Generate and execute SQL queries on a local SQLite database (order_management.db)

        - Provide fallback responses using RAG-style (Retrieval-Augmented Generation) if SQL fails

        - Maintain session-based follow-up question support

        - Log chats, format DB results naturally, and run on a stylish UI
⚙️ Features
    🔍 Natural Language to SQL Translation: Powered by LLaMA2 with retry/fallback logic

    🧠 Intent Classification: Determines if the user wants order details, support info, etc.

    📂 SQLite Database Integration: Includes order_status, product_info, support_contacts, and faq tables

    🌐 FastAPI Backend: Processes requests, generates SQL, handles memory & fallback

    🎨 Streamlit Frontend: Dark/light themes, chat bubbles, avatar mode, downloadable logs

    🧾 Session Memory: Handles follow-up questions within the same chat context

    🌍 Multilingual Ready: Placeholder logic for basic multi-language interactions.
🏗️ Folder Structure
📦LLM_chatbot/ ├── app.py # FastAPI backend (chat engine, LLaMA2 logic, SQLite) ├── ui.py # Streamlit frontend (UI for user chat) ├── order_management.py # Database setup and utility functions ├── order_management.db # Embedded SQLite database ├── requirements.txt # Python dependencies ├── README.md # Project documentation └── .env # (Optional) API keys or environment variables

🛠️ Steps for Approach
🔧 Database Initialization:

Defined in order_management.py

Tables: order_status, product_info, support_contacts, faq

Includes extended mock data for various scenarios

Functions to query order info, pricing, support contacts, and FAQs

🚀 Backend (FastAPI - app.py):

Receives input from frontend (/chat route)

Uses LLaMA2 via Ollama to: _ Classify user intent _ Generate SQL if needed

Adds retry logic: If SQL fails, falls back to RAG-based answer

Embeds database setup (init_db())

Chat session memory supported

Logs chats in SQLite (optional)

Routes: /chat, /health, /test-db

🎨 Frontend (Streamlit - ui.py):

Stylish UI with: _ Toggle for light/dark mode _ Chat bubble avatars * Chat history with clear/download buttons

Sends user queries to FastAPI backend

Displays formatted, friendly responses

Uses a fixed chatbot icon and background image

Supports downloadable chat log as ---> chat_log.txt

📊 Key Performance Indicators (KPIs)
Response Time: Optimized with minimal external calls, direct SQLite querying

Naturalness of Responses: Converts DB results into friendly language

Intent Accuracy: LLaMA2 ensures correct intent classification (e.g., support vs order)

User Experience: Clean UI, follow-up support, downloadable history

Failure Handling: Retries failed SQL, uses fallback RAG-style info when needed

🚀 Deploying the App:
You can deploy the LLaMA2 Chatbot locally or on a cloud platform like Render. Below are the steps for both methods.

🖥️ Local Deployment

    * Clone the Repository:
           git clone https://github.com/your-username/llama2-sql-chatbot.git
           cd llama2-sql-chatbot

    * Install Dependencies: Make sure you have Python 3.9+ and Ollama installed. Then install all Python requirements:
            pip install -r requirements.txt

    * Run Ollama with LLaMA2: Start the LLaMA2 model locally using Ollama:
            ollama run llama2

    * Run order_management.py file to create a order_management.db (database exection)

    * Start the FastAPI Backend: In a new terminal: uvicorn app:app --reload

    * Launch the Streamlit Frontend: In another terminal:
             streamlit run ui.py

    * Interact with the Chatbot:
Open your browser and go to: http://localhost:8501 You’ll see the chatbot interface and can start chatting!

✅ Supported Queries (Examples)

“What is the status of order ORD5678?”

“Show me the price of Galaxy Buds Pro”

“How can I reach technical support?”

“What are the FAQs?”

“Tell me about my recent order again” (Follow-up support!)

📌 Conclusion
This project highlights how powerful and efficient an LLM-powered chatbot can be when paired with SQL and smart routing. Built with speed and clarity in mind, this chatbot bridges the gap between conversational AI and structured data, giving both technical and non-technical users a delightful experience.

-Future improvements can include:

-Voice input (Whisper integration)

-PDF/file-based RAG-style context injection

-Dashboard analytics of query patterns

How to Run:
Clone this repository.

Install dependencies by running: pip install -r requirements.txt

To create database file -------------- python order_management.db

Start the FastAPI backend ------------ uvicorn app:app --reload

Run the Streamlit UI ----------------- streamlit run ui.py

background_dark = "https://wallpaperaccess.com/full/8691990.png"

background_light = "https://images.unsplash.com/photo-1603791440384-56cd371ee9a7"

icon_url = "https://img.freepik.com/premium-vector/chatbot-concept-background-realistic-style_730620-44319.jpg"

ollama model : https://ollama.com/

Here is the complete breakdown of what you’ve used and what you haven’t based on the interview task requirements and your current project setup — along with any additional features you’ve implemented beyond the spec:

💻 Tech Stack Used in This Project

Component | Tool / Implementation | Status
LLM | ✅ LLaMA2 via Ollama (local) | ✔️ Used
Backend | ✅ FastAPI (app.py) | ✔️ Used
SQL | ✅ SQLite (order_management.db) | ✔️ Used
Prompting | ❌ LangChain | ❌ Not Used (by choice for performance)
UI | ✅ Streamlit (ui.py) | ✔️ Used
✅ Features Implemented

Requirement / Feature | Status
SQL Database with 4 Required Tables | ✔️ product_info, order_status, support_contacts, faq
LLM SQL Generation (Option A) | ✔️ Implemented
RAG-style Retrieval (Option B) | ✔️ Implemented as fallback logic
Natural Language Interface (CLI/UI) | ✔️ Streamlit-based UI
Formatted SQL Output (Rephrased Answers) | ✔️ Implemented
Retry Logic for SQL Failures | ✔️ Implemented
Follow-up Questions with Session Memory | ✔️ Implemented
Health/Test Endpoints (/health, /test-db) | ✔️ Implemented in FastAPI
Logging of Chat History | ✔️ Chat log stored and downloadable
Avatar Chat Bubbles + Theme Toggle | ✔️ Implemented in Streamlit UI
Custom SQL Formatting + Details | ✔️ Implemented
Multilingual Placeholder Support | ✔️ Basic placeholder present
Background Image, Branding, Icon Setup | ✔️ Customized in UI
Deployment | ❌ Not Yet (Local-only)
❌ Not Used (from Suggestions)

Tool / Feature | Status
OpenAI GPT-3.5 / Mistral | ❌ Not Used
Flask | ❌ Not Used
MySQL / PostgreSQL | ❌ Not Used
LangChain | ❌ Not Used
Render, Hugging Face Space | ❌ Not Yet
CLI-only Interface | ❌ Not Used
✨ Additional Features Added

FastAPI health check routes (/health, /test-db)
Session memory to support follow-up questions
Avatar-based chat bubbles for more human-like interaction
Dark/Light mode toggle
Downloadable chat logs
Error handling with retry and fallback mechanisms
Intent classification logic using LLM
Embedded DB initialization logic in Python
HARSHAVARDHINI.K harsha270404@gmail.com
