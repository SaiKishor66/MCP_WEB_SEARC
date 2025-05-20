# 🚀 MCP_Web_Search – Smart Web Agent by Sai Kishor

A powerful Streamlit-based web agent powered by MCP Agent + Puppeteer + OpenAI, capable of browsing websites, performing actions like clicking and scrolling, extracting and summarizing content, and capturing screenshots — all through natural language commands.

---
## 📸 Demo

![Screenshot 2025-05-20 16:43:32](https://github.com/user-attachments/assets/23f7c96e-e02d-4b16-9ea7-b24c8b9903a5)

---

## 🧠 Features

- 🌐 Navigate to any website via text commands
- 🖱️ Click buttons, scroll pages, and interact with content
- 📝 Extract and summarize information from pages
- 📷 Capture screenshots of webpage elements
- 🔁 Perform multi-step automated browsing tasks

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) – Frontend interface  
- [Puppeteer](https://pptr.dev/) – Browser automation  
- [MCP Agent](https://github.com/microsoft/mcp) – Agent orchestration  
- [OpenAI API](https://platform.openai.com/) – LLM integration  

---

## 📁 Project Structure

📦MCP_Web_Search  
┣ 📜 smart_web_agent.py # Main Streamlit app  
┣ 📜 README.md # Project documentation  
┗ 📜 requirements.txt # Python dependencies  

---

## 🚀 Getting Started

### 📦 Usage Guide

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/MCP_Web_Search.git
cd MCP_Web_Search

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your OpenAI API Key
# For Linux / macOS
export OPENAI_API_KEY=your_openai_api_key

# For Windows CMD
set OPENAI_API_KEY=your_openai_api_key

# 4. Run the app
streamlit run smart_web_agent.py
