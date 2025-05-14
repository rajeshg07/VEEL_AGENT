# from veel_agent.services.base_node import BaseNode
# from veel_agent.schemas.state import StateDict
# from veel_agent.configs.logging_config import logging

# logger = logging.getLogger(__name__)



# class TrendAnalyzer(BaseNode):
#     def process(self, state: StateDict) -> StateDict:
#         logger.info(f"Running trend analyzer for: {state['query']}")
#         if not state["flags"].get("trend"):
#             state["trend"] = f"Trending topics for: {state['query']}"
#             state["flags"]["trend"] = True
#         state["current_step"] += 1
#         return state


import os
import requests
from dotenv import load_dotenv
from veel_agent.services.base import BaseNode #need to change

# Load environment variables from .env file
load_dotenv()

class SerpApiTrendNode(BaseNode):
    def __init__(self):
        super().__init__(name="SerpApi Trend Node")
        self.api_key = os.getenv("SERPAPI_API_KEY", "")
        
    def __call__(self, state):
        self.log(state, "Fetching trends using SerpApi Google Trends")
        
        if not self.api_key:
            self.log(state, "No SerpApi API key found in .env file", level="WARNING")
            state.trends = self._get_fallback_trends(state.input)
            return state
            
        try:
            url = "https://serpapi.com/search"
            params = {
                "engine": "google_trends",
                "q": state.input,
                "data_type": "TIMESERIES",
                "api_key": self.api_key
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                # Extract interest over time data
                timeline_data = data.get("interest_over_time", {}).get("timeline_data", [])
                
                # Convert to the format our application expects
                trends = {}
                for point in timeline_data:
                    date = point.get("date", "")
                    value = point.get("values", [{}])[0].get("value", 0)
                    if date:
                        trends[date] = value
                
                if trends:
                    state.trends = trends
                    self.log(state, f"Found {len(trends)} trend data points")
                else:
                    state.trends = self._get_fallback_trends(state.input)
                    self.log(state, "No trend data found, using fallback", level="WARNING")
            else:
                self.log(state, f"SerpApi error: {response.status_code}", level="ERROR")
                state.trends = self._get_fallback_trends(state.input)
        except Exception as e:
            state.trends = self._get_fallback_trends(state.input)
            self.log(state, f"Error fetching trends: {e}", level="ERROR")
            
        return state
    
    def _get_fallback_trends(self, query):
        """Generate fallback trend data when API is unavailable"""
        import random
        from datetime import datetime, timedelta
        
        # Create fake trend data for the last 7 days
        trends = {}
        today = datetime.now()
        
        for i in range(7):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            # Generate a sensible random value between 25-100
            value = random.randint(25, 100)
            trends[date] = value
            
        return trends
        