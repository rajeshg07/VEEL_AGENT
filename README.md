# # Marketing Agent with SerpApi Integration

# This agent uses SerpApi to fetch trending data and hashtags for marketing queries, then generates recommendations using an LLM.

# ## Setup

# 1. Get a free SerpApi API key at https://serpapi.com/users/sign_up (100 searches/month free)

# 2. Install dependencies:
# ```
# pip install langgraph langchain-openai fastapi uvicorn python-dotenv requests
# ```

# 3. Set up your environment:
#    - Copy `.env.example` to `.env`
#    - Add your SerpApi and OpenAI API keys to the `.env` file

# ## Features

# - Trend analysis using SerpApi Google Trends
# - Hashtag recommendations using SerpApi Google Search
# - Marketing recommendations via LLM
# - Command line interface
# - FastAPI REST endpoint

# ## Usage

# ### Command Line:
# ```
# python main.py
# ```

# ### API Server:
# ```
# uvicorn api:app --reload
# ```
# Then make POST requests to `/analyze` with JSON body: `{"input": "your marketing query"}