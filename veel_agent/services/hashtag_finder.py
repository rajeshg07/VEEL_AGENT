# from veel_agent.services.base_node import BaseNode
# from veel_agent.schemas.state import StateDict
# from veel_agent.configs.logging_config import logging

# logger = logging.getLogger(__name__)



# class HashtagFinder(BaseNode):
#     def process(self, state: StateDict) -> StateDict:
#         logger.info(f"Running hashtag finder for: {state['query']}")
#         if not state["flags"].get("hashtag"):
#             state["hashtags"] = [f"#{state['query'].replace(' ', '')}"]
#             state["flags"]["hashtag"] = True
#         state["current_step"] += 1
#         return state


import os
import requests
import re
from dotenv import load_dotenv
from veel_agent.services.base import BaseNode #need to change

# Load environment variables from .env file
load_dotenv()

class SerpApiHashtagNode(BaseNode):
    def __init__(self):
        super().__init__(name="SerpApi Hashtag Node")
        self.api_key = os.getenv("SERPAPI_API_KEY", "")
        
    def __call__(self, state):
        self.log(state, "Fetching hashtags via SerpApi Google Search")
        
        if not self.api_key:
            self.log(state, "No SerpApi API key found in .env file", level="WARNING")
            state.hashtags = self._get_fallback_hashtags(state.input)
            return state
            
        try:
            # We'll search for trending hashtags related to the query
            query = f"trending hashtags {state.input} marketing"
            
            url = "https://serpapi.com/search"
            params = {
                "engine": "google",
                "q": query,
                "num": 100,  # Get more results to extract hashtags from
                "api_key": self.api_key
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract hashtags from organic results
                hashtags = set()
                
                # Process organic results
                organic_results = data.get("organic_results", [])
                for result in organic_results:
                    title = result.get("title", "")
                    snippet = result.get("snippet", "")
                    
                    # Extract hashtags from title and snippet
                    hashtags.update(self._extract_hashtags(title))
                    hashtags.update(self._extract_hashtags(snippet))
                
                # If we found hashtags, use them
                if hashtags:
                    state.hashtags = list(hashtags)[:10]  # Limit to 10 hashtags
                    self.log(state, f"Found {len(state.hashtags)} hashtags")
                else:
                    self.log(state, "No hashtags found, using fallback", level="WARNING")
                    state.hashtags = self._get_fallback_hashtags(state.input)
            else:
                self.log(state, f"SerpApi error: {response.status_code}", level="ERROR")
                state.hashtags = self._get_fallback_hashtags(state.input)
        except Exception as e:
            state.hashtags = self._get_fallback_hashtags(state.input)
            self.log(state, f"Exception in API call: {e}", level="ERROR")
            
        return state
    
    def _extract_hashtags(self, text):
        """Extract hashtags from text"""
        if not text:
            return []
        
        # Find hashtags in the text
        # Pattern looks for #word where word is alphanumeric
        hashtag_pattern = r'#(\w+)'
        found_tags = re.findall(hashtag_pattern, text)
        
        # Convert to proper hashtag format
        return [f"#{tag.lower()}" for tag in found_tags]
        
    def _get_fallback_hashtags(self, query):
        """Generate fallback hashtags when API is unavailable"""
        # Convert query to keywords
        words = query.lower().replace("?", "").replace("!", "").split()
        base_words = [w for w in words if len(w) > 3]
        
        # Create some generic hashtags
        hashtags = []
        
        # Add query-specific hashtags
        for word in base_words[:3]:  # Use up to 3 words from query
            hashtags.append(f"#{word}")
            
        # Add some generic marketing hashtags
        generic_tags = [
            "#marketing", "#digital", "#socialmedia", "#trending",
            "#strategy", "#business", "#growth", "#brand",
            "#analytics", "#content", "#engagement"
        ]
        
        # Combine specific and generic, ensure we return 5-10 hashtags
        result = hashtags + generic_tags
        return result[:10]  # Return at most 10 hashtags
    