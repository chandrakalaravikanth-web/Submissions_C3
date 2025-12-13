"""
LangGraph Workflow for Multi-Agent Design Analysis
"""

from typing import Dict, Any
from modules.llm_factory import LLMFactory
from agents.brand_agent import BrandAgent
from agents.aesthetic_agent import AestheticAgent
from agents.conversion_agent import ConversionAgent
from agents.monetization_agent import MonetizationAgent
from agents.privacy_agent import PrivacyAgent
from agents.ethical_agent import EthicalAgent
from agents.trend_agent import TrendAgent
import re

class DesignAnalysisWorkflow:
    """Multi-agent workflow orchestrator"""
    
    def __init__(self):
        self.llm_factory = LLMFactory()
        self.agents = {
            "brand": BrandAgent(self.llm_factory),
            "aesthetic": AestheticAgent(self.llm_factory),
            "conversion": ConversionAgent(self.llm_factory),
            "monetization": MonetizationAgent(self.llm_factory),
            "privacy": PrivacyAgent(self.llm_factory),
            "ethical": EthicalAgent(self.llm_factory),
            "trends": TrendAgent(self.llm_factory)
        }
    
    def run_agent(self, agent_type: str, image_data: str, context: str) -> Dict[str, Any]:
        """Execute a specific agent"""
        agent = self.agents.get(agent_type)
        if not agent:
            return {"agent": agent_type, "analysis": "Agent not found", "score": 0}
        
        try:
            result = agent.analyze(image_data, context)
            return result
        except Exception as e:
            return {"agent": agent_type, "analysis": f"Error: {str(e)}", "score": 0}