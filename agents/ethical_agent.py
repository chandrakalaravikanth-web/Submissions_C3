"""Ethical Design Agent"""

from typing import Dict, Any
import re

class EthicalAgent:
    """Analyzes ethical design"""
    
    def __init__(self, llm_factory):
        self.llm_factory = llm_factory
        self.name = "⚖️ Ethical Design Agent"
    
    def analyze(self, image_data: str, context: str) -> Dict[str, Any]:
        """Analyze design"""
        
        prompt = f"""You are an Ethical Design Advocate.

Context: {context}

Conduct ethical audit:
1. Dark Patterns - Manipulative UX
2. Transparency - Honest communication
3. User Autonomy - Choice and control
4. Addictive Design - Unhealthy tactics
5. Inclusivity - Bias check
6. Score: Rate X/10 (MUST include)

Provide detailed, actionable insights with specific recommendations."""
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        analysis = self.llm_factory.create_completion(messages)
        score = self._extract_score(analysis)
        
        return {
            "agent": self.name,
            "analysis": analysis,
            "score": score
        }
    
    def _extract_score(self, text: str) -> float:
        """Extract score from text"""
        patterns = [r'score[:\s]+(\d+(?:\.\d+)?)/10', r'rate[:\s]+(\d+(?:\.\d+)?)/10', r'(\d+(?:\.\d+)?)\s*/\s*10']
        for p in patterns:
            match = re.search(p, text.lower())
            if match:
                return float(match.group(1))
        return 7.5
