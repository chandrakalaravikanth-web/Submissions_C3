"""Privacy & Security Agent"""

from typing import Dict, Any
import re

class PrivacyAgent:
    """Analyzes privacy and security"""
    
    def __init__(self, llm_factory):
        self.llm_factory = llm_factory
        self.name = "🔒 Privacy & Security Agent"
    
    def analyze(self, image_data: str, context: str) -> Dict[str, Any]:
        """Analyze design"""
        
        prompt = f"""You are a Privacy and Security UX Expert.

Context: {context}

Analyze privacy & security:
1. Data Collection - Transparency
2. Privacy Controls - User control
3. Security Patterns - Trust signals
4. GDPR Compliance - Regulation adherence
5. Cookie Consent - Implementation
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
