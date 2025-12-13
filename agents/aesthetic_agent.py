"""Aesthetic Quality Agent"""

from typing import Dict, Any
import re

class AestheticAgent:
    """Analyzes aesthetic quality"""
    
    def __init__(self, llm_factory):
        self.llm_factory = llm_factory
        self.name = "✨ Aesthetic Quality Agent"
    
    def analyze(self, image_data: str, context: str) -> Dict[str, Any]:
        """Analyze design"""
        
        prompt = f"""You are a Design Aesthetics Expert.

Context: {context}

Analyze aesthetic quality:
1. Visual Appeal - First impression
2. Balance & Harmony - Composition
3. Modernity - Contemporary design
4. Sophistication - Polish level
5. Emotional Impact - Feelings evoked
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
