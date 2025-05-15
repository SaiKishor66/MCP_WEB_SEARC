import asyncio
import os
import streamlit as st

api_key = st.secrets["OPENAI_API_KEY"]

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm import RequestParams

# Page config
st.set_page_config(page_title="Smart Web Agent", layout="wide")

# Custom CSS styling
st.markdown("""
    <style>
        .main-header {
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            color: #4CAF50;
            margin-bottom: 20px;
        }
        .block-container {
            padding-top: 2rem;
        }
        textarea {
            font-size: 16px !important;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 8px 16px;
        }
        footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# Main title
st.markdown("<h1 class='main-header'>Smart Web Agent 🤖</h1>", unsafe_allow_html=True)
st.markdown("Empower your browsing with intelligent navigation, automation, and interaction.")

# Sidebar
with st.sidebar:
    st.markdown("## 💡 Try These Commands")
    st.markdown("### 🔗 Navigation")
    st.markdown("- Go to `wikipedia.org/wiki/computer_vision`")
    st.markdown("### 🖱️ Interaction")
    st.markdown("- Click on 'Object Detection' and take a screenshot")
    st.markdown("### 📋 Multi-step Tasks")
    st.markdown("- Navigate, scroll, and summarize the wiki page")

    st.caption("⚙️ Powered by Puppeteer + LLM")

# Command input
st.markdown("## 🧠 Enter Your Command Below")
query = st.text_area("",
                     placeholder="Ask me to browse a site, click something, extract info, summarize content...",
                     height=100
                     )

# Init session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.mcp_app = MCPApp(name="smart_web_agent")
    st.session_state.mcp_context = None
    st.session_state.mcp_agent_app = None
    st.session_state.browser_agent = None
    st.session_state.llm = None
    st.session_state.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(st.session_state.loop)


# Agent setup
async def setup_agent():
    if not st.session_state.initialized:
        try:
            st.session_state.mcp_context = st.session_state.mcp_app.run()
            st.session_state.mcp_agent_app = await st.session_state.mcp_context.__aenter__()

            st.session_state.browser_agent = Agent(
                name="browser",
                instruction="""You are a helpful web browsing assistant that can interact with websites using puppeteer.
                - Navigate to websites and perform browser actions (click, scroll, type)
                - Extract information from web pages
                - Take screenshots of page elements when useful
                - Provide concise summaries of web content using markdown
                - Follow multi-step browsing sequences to complete tasks
                """,
                server_names=["puppeteer"]
            )

            await st.session_state.browser_agent.initialize()
            st.session_state.llm = await st.session_state.browser_agent.attach_llm(OpenAIAugmentedLLM)

            logger = st.session_state.mcp_agent_app.logger
            tools = await st.session_state.browser_agent.list_tools()
            logger.info("Tools available:", data=tools)

            st.session_state.initialized = True
        except Exception as e:
            return f"Error during initialization: {str(e)}"
    return None


# Agent runner
async def run_mcp_agent(message):
    if not os.getenv("OPENAI_API_KEY"):
        return "❌ Error: OPENAI_API_KEY not set"

    try:
        error = await setup_agent()
        if error:
            return error

        response = await st.session_state.llm.generate_str(
            message=message,
            request_params=RequestParams(use_history=True)
        )

        return response
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Button and response
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("🚀 Run", use_container_width=True):
        with st.spinner("Running your web agent..."):
            response_result = st.session_state.loop.run_until_complete(run_mcp_agent(query))

        st.markdown("## 📬 Response")
        st.markdown(response_result)

# Footer / Credit
st.markdown("""
    <hr>
    <center>
    <p style="font-size: 14px;">🔧 Powered by MCP Agent + Streamlit</p>
    </center>
""", unsafe_allow_html=True)
