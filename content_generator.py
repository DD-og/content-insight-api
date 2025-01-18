import os
import json
from groq import Groq
from typing import Dict, Any
from jsonschema import validate, ValidationError

# Initialize GROQ client
client = Groq(
    api_key="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"
)

# JSON Schema definition
SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "basicInfo": {
            "type": "object",
            "properties": {
                "brandName": {
                    "type": "string",
                    "description": "The name of the brand."
                },
                "tagline": {
                    "type": "string",
                    "description": "Optional tagline for the brand.",
                    "default": None
                },
                "industryType": {
                    "type": "string",
                    "enum": [
                        "Technology", "Healthcare", "Finance", "Retail",
                        "Education", "Entertainment", "Other"
                    ]
                },
                "productOrServiceType": {
                    "type": "string",
                    "enum": [
                        "SaaS", "PaaS", "IaaS", "Consumer Goods",
                        "B2B Services", "B2C Services", "Other"
                    ]
                },
                "targetAudience": {
                    "type": "string",
                    "enum": [
                        "Small Businesses", "Enterprise Companies",
                        "Freelancers", "Students", "Tech-Savvy Professionals",
                        "General Consumers", "Other"
                    ]
                }
            },
            "required": ["brandName", "industryType", "productOrServiceType", "targetAudience"]
        },
        "productServiceDetails": {
            "type": "object",
            "properties": {
                "features": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "USPs": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "primaryProblemSolved": {
                    "type": "string"
                }
            },
            "required": ["features", "USPs", "primaryProblemSolved"]
        },
        "articleDetails": {
            "type": "object",
            "properties": {
                "articleType": {
                    "type": "string",
                    "enum": [
                        "Blog", "News Article", "Press Release",
                        "Case Study", "Whitepaper", "Other"
                    ]
                },
                "articleLength": {
                    "type": "integer",
                    "minimum": 100
                },
                "keywordsToEmphasize": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "callToAction": {
                    "type": "string",
                    "default": None
                }
            },
            "required": ["articleType", "articleLength", "keywordsToEmphasize"]
        }
    },
    "required": ["basicInfo", "productServiceDetails", "articleDetails"]
}

def validate_input(data: Dict[str, Any]) -> None:
    """
    Validate input data against the JSON schema
    """
    try:
        validate(instance=data, schema=SCHEMA)
    except ValidationError as e:
        raise ValueError(f"Input validation failed: {str(e)}")

def generate_article(input_data: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    """
    Generate an article using GROQ API based on the provided input data
    """
    tagline = input_data['basicInfo'].get('tagline', '')
    call_to_action = input_data['articleDetails'].get('callToAction', '')
    
    prompt = f"""
    Generate a detailed {input_data['articleDetails']['articleType']} about {input_data['basicInfo']['brandName']}.
    
    Brand Information:
    - Industry: {input_data['basicInfo']['industryType']}
    - Product/Service Type: {input_data['basicInfo']['productOrServiceType']}
    - Target Audience: {input_data['basicInfo']['targetAudience']}
    {f'- Tagline: {tagline}' if tagline else ''}
    
    Key Features:
    {', '.join(input_data['productServiceDetails']['features'])}
    
    USPs:
    {', '.join(input_data['productServiceDetails']['USPs'])}
    
    Primary Problem Solved:
    {input_data['productServiceDetails']['primaryProblemSolved']}
    
    Keywords to Emphasize:
    {', '.join(input_data['articleDetails']['keywordsToEmphasize'])}
    
    Required length: {input_data['articleDetails']['articleLength']} words
    {f'Call to Action: {call_to_action}' if call_to_action else ''}
    
    Please generate a well-structured article that incorporates all these elements while maintaining a professional tone.
    The article should be engaging, informative, and highlight the unique value proposition of the product/service.
    Make sure to naturally incorporate the keywords throughout the text.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=2000,
        top_p=1,
        stream=False
    )

    return {
        "articleGeneration": {
            "englishArticle": chat_completion.choices[0].message.content
        }
    }

def main():
    # Example input data
    input_data = {
        "basicInfo": {
            "brandName": "TechCorp Solutions",
            "tagline": "Empowering Enterprise Innovation",
            "industryType": "Technology",
            "productOrServiceType": "SaaS",
            "targetAudience": "Enterprise Companies"
        },
        "productServiceDetails": {
            "features": [
                "Cloud Integration",
                "AI-Powered Analytics",
                "Real-time Monitoring",
                "Custom Workflows",
                "Enterprise Security"
            ],
            "USPs": [
                "24/7 Support",
                "99.9% Uptime",
                "Enterprise-grade Security",
                "Custom Integration Options"
            ],
            "primaryProblemSolved": "Streamlining business operations through intelligent automation and analytics"
        },
        "articleDetails": {
            "articleType": "Blog",
            "articleLength": 800,
            "keywordsToEmphasize": [
                "automation",
                "efficiency",
                "scalability",
                "enterprise solutions",
                "digital transformation"
            ],
            "callToAction": "Schedule a demo today to see how TechCorp can transform your business operations."
        }
    }

    try:
        # Validate input data
        validate_input(input_data)
        
        # Generate article
        result = generate_article(input_data)
        
        # Print the result
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
