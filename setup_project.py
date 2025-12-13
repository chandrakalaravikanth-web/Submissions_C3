"""
Automatic Project Setup Script
Run this FIRST to create all necessary files and folders
"""

import os
import sys

def create_folder_structure():
    """Create all required folders"""
    folders = ['agents', 'graph', 'modules', 'tools', 'utils', 'tests']
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Created folder: {folder}/")
        
        # Create __init__.py in each folder
        init_file = os.path.join(folder, '__init__.py')
        with open(init_file, 'w') as f:
            f.write('"""Package initialization"""\n')
        print(f"✅ Created: {folder}/__init__.py")

def create_config():
    """Create config.py"""
    content = '''"""
Configuration Management
"""

import os
from typing import Optional
from pydantic import BaseModel

class Config(BaseModel):
    """Application configuration"""
    
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    MODEL_NAME: str = "anthropic/claude-3.5-sonnet"
    MAX_TOKENS: int = 2500
    TEMPERATURE: float = 0.7
    APP_TITLE: str = "AI Design Intelligence"
    APP_ICON: str = "🤖"
    
    class Config:
        env_file = ".env"

config = Config()

def set_api_key(api_key: str):
    """Set the API key dynamically"""
    config.OPENROUTER_API_KEY = api_key
    os.environ["OPENROUTER_API_KEY"] = api_key

def get_api_key() -> Optional[str]:
    """Get the configured API key"""
    return config.OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY")
'''
    
    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Created: config.py")

def create_llm_factory():
    """Create modules/llm_factory.py"""
    content = '''"""LLM Factory for creating AI clients"""

from openai import OpenAI
from config import config

class LLMFactory:
    """Factory for creating LLM clients"""
    
    def __init__(self):
        self.client = None
    
    def get_client(self) -> OpenAI:
        """Get or create OpenAI client"""
        if not self.client and config.OPENROUTER_API_KEY:
            self.client = OpenAI(
                base_url=config.OPENROUTER_BASE_URL,
                api_key=config.OPENROUTER_API_KEY
            )
        return self.client
    
    def create_completion(self, messages: list, max_tokens: int = 2500):
        """Create a completion"""
        client = self.get_client()
        if not client:
            raise ValueError("No API key configured")
        
        try:
            response = client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=messages,
                max_tokens=max_tokens,
                temperature=config.TEMPERATURE
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"LLM API Error: {str(e)}")
'''
    
    with open('modules/llm_factory.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Created: modules/llm_factory.py")

def create_logger():
    """Create utils/logger.py"""
    content = '''"""Logging utilities"""

import logging
import sys

def setup_logger(name: str = "DesignAnalysis", level: int = logging.INFO):
    """Setup application logger"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if logger.handlers:
        return logger
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
'''
    
    with open('utils/logger.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Created: utils/logger.py")

def create_agents():
    """Create all agent files"""
    
    agent_template = '''"""{{NAME}} Agent"""

from typing import Dict, Any
import re

class {{CLASS_NAME}}:
    """{{DESCRIPTION}}"""
    
    def __init__(self, llm_factory):
        self.llm_factory = llm_factory
        self.name = "{{DISPLAY_NAME}}"
    
    def analyze(self, image_data: str, context: str) -> Dict[str, Any]:
        """Analyze design"""
        
        prompt = f"""{{PROMPT}}

Context: {context}

{{ANALYSIS_POINTS}}

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
        patterns = [r'score[:\\s]+(\\d+(?:\\.\\d+)?)/10', r'rate[:\\s]+(\\d+(?:\\.\\d+)?)/10', r'(\\d+(?:\\.\\d+)?)\\s*/\\s*10']
        for p in patterns:
            match = re.search(p, text.lower())
            if match:
                return float(match.group(1))
        return 7.5
'''
    
    agents = {
        'brand_agent.py': {
            'NAME': 'Brand Consistency',
            'CLASS_NAME': 'BrandAgent',
            'DESCRIPTION': 'Analyzes brand consistency',
            'DISPLAY_NAME': '🏷️ Brand Consistency Agent',
            'PROMPT': 'You are a Brand Strategist expert.',
            'ANALYSIS_POINTS': '''Analyze brand consistency:
1. Brand Alignment - Values reflection
2. Color Guidelines - Brand color adherence  
3. Typography - Brand font usage
4. Tone & Voice - Communication style
5. Logo & Assets - Implementation
6. Score: Rate X/10 (MUST include)'''
        },
        'aesthetic_agent.py': {
            'NAME': 'Aesthetic Quality',
            'CLASS_NAME': 'AestheticAgent',
            'DESCRIPTION': 'Analyzes aesthetic quality',
            'DISPLAY_NAME': '✨ Aesthetic Quality Agent',
            'PROMPT': 'You are a Design Aesthetics Expert.',
            'ANALYSIS_POINTS': '''Analyze aesthetic quality:
1. Visual Appeal - First impression
2. Balance & Harmony - Composition
3. Modernity - Contemporary design
4. Sophistication - Polish level
5. Emotional Impact - Feelings evoked
6. Score: Rate X/10 (MUST include)'''
        },
        'conversion_agent.py': {
            'NAME': 'Conversion Optimization',
            'CLASS_NAME': 'ConversionAgent',
            'DESCRIPTION': 'Analyzes conversion optimization',
            'DISPLAY_NAME': '💰 Conversion Optimization Agent',
            'PROMPT': 'You are a CRO specialist.',
            'ANALYSIS_POINTS': '''Analyze conversion potential:
1. CTA Analysis - Effectiveness
2. Layout Optimization - Funnel design
3. Friction Points - Journey obstacles
4. Trust Signals - Credibility
5. Value Proposition - Clarity
6. Score: Rate X/10 (MUST include)'''
        },
        'monetization_agent.py': {
            'NAME': 'Monetization',
            'CLASS_NAME': 'MonetizationAgent',
            'DESCRIPTION': 'Analyzes monetization strategy',
            'DISPLAY_NAME': '💳 Monetization Agent',
            'PROMPT': 'You are a Monetization Strategy Expert.',
            'ANALYSIS_POINTS': '''Analyze monetization UX:
1. Ad Placement - Intrusiveness
2. Subscription Flow - Payment UX
3. In-App Purchases - IAP implementation
4. Pricing Display - Transparency
5. Value Communication - Benefits
6. Score: Rate X/10 (MUST include)'''
        },
        'privacy_agent.py': {
            'NAME': 'Privacy & Security',
            'CLASS_NAME': 'PrivacyAgent',
            'DESCRIPTION': 'Analyzes privacy and security',
            'DISPLAY_NAME': '🔒 Privacy & Security Agent',
            'PROMPT': 'You are a Privacy and Security UX Expert.',
            'ANALYSIS_POINTS': '''Analyze privacy & security:
1. Data Collection - Transparency
2. Privacy Controls - User control
3. Security Patterns - Trust signals
4. GDPR Compliance - Regulation adherence
5. Cookie Consent - Implementation
6. Score: Rate X/10 (MUST include)'''
        },
        'ethical_agent.py': {
            'NAME': 'Ethical Design',
            'CLASS_NAME': 'EthicalAgent',
            'DESCRIPTION': 'Analyzes ethical design',
            'DISPLAY_NAME': '⚖️ Ethical Design Agent',
            'PROMPT': 'You are an Ethical Design Advocate.',
            'ANALYSIS_POINTS': '''Conduct ethical audit:
1. Dark Patterns - Manipulative UX
2. Transparency - Honest communication
3. User Autonomy - Choice and control
4. Addictive Design - Unhealthy tactics
5. Inclusivity - Bias check
6. Score: Rate X/10 (MUST include)'''
        },
        'trend_agent.py': {
            'NAME': 'Trend Analysis',
            'CLASS_NAME': 'TrendAgent',
            'DESCRIPTION': 'Analyzes design trends',
            'DISPLAY_NAME': '📈 Trend Analysis Agent',
            'PROMPT': 'You are a Design Trend Analyst.',
            'ANALYSIS_POINTS': '''Analyze trend alignment:
1. Current Trends - 2024-2025 trends
2. Dated Elements - Outdated patterns
3. Emerging Patterns - Cutting-edge techniques
4. Industry Standards - Best practices
5. Future-Proofing - Design longevity
6. Score: Rate X/10 (MUST include)'''
        }
    }
    
    for filename, data in agents.items():
        content = agent_template
        for key, value in data.items():
            content = content.replace('{{' + key + '}}', value)
        
        filepath = os.path.join('agents', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created: agents/{filename}")

def main():
    """Main setup function"""
    print("\n🚀 Starting Project Setup...\n")
    
    create_folder_structure()
    print()
    
    create_config()
    create_llm_factory()
    create_logger()
    print()
    
    create_agents()
    print()
    
    print("✅ Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Make sure you have app.py and graph/workflow.py in place")
    print("2. Run: python app.py")
    print("3. Enter your OpenRouter API key when prompted")
    print("\n🎉 Ready to analyze designs!\n")

if __name__ == "__main__":
    main()