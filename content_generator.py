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
    "title": "Brand Insights, Article Generation, and Media Insights Schema",
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
                    ],
                    "description": "The industry the brand belongs to."
                },
                "productOrServiceType": {
                    "type": "string",
                    "enum": [
                        "SaaS", "PaaS", "IaaS", "Consumer Goods",
                        "B2B Services", "B2C Services", "Other"
                    ],
                    "description": "The type of product or service the brand offers."
                },
                "targetAudience": {
                    "type": "string",
                    "enum": [
                        "Small Businesses", "Enterprise Companies",
                        "Freelancers", "Students", "Tech-Savvy Professionals",
                        "General Consumers", "Other"
                    ],
                    "description": "The primary audience for the brand."
                }
            },
            "required": ["brandName", "industryType", "productOrServiceType", "targetAudience"]
        },
        "productServiceDetails": {
            "type": "object",
            "properties": {
                "features": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "A list of key features of the product or service."
                },
                "USPs": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Unique Selling Points of the product or service."
                },
                "primaryProblemSolved": {
                    "type": "string",
                    "description": "The main problem the product or service aims to solve."
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
                    ],
                    "description": "The type of article to generate."
                },
                "articleLength": {
                    "type": "integer",
                    "description": "The desired length of the article in words.",
                    "minimum": 100
                },
                "keywordsToEmphasize": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Keywords to highlight in the article."
                },
                "callToAction": {
                    "type": "string",
                    "description": "Optional call-to-action text.",
                    "default": None
                }
            },
            "required": ["articleType", "articleLength", "keywordsToEmphasize"]
        },
        "mediaInsights": {
            "type": "object",
            "properties": {
                "primaryAudienceDemographics": {
                    "type": "string",
                    "description": "Demographics of the primary audience."
                },
                "painPointsAddressed": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Pain points the product or service addresses."
                },
                "competitors": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of competitors in the market."
                },
                "marketPosition": {
                    "type": "string",
                    "description": "How the brand positions itself in comparison to competitors."
                }
            },
            "required": ["primaryAudienceDemographics", "painPointsAddressed", "competitors", "marketPosition"]
        }
    },
    "required": ["basicInfo", "productServiceDetails", "articleDetails", "mediaInsights"]
}

def validate_input(data: Dict[str, Any]) -> None:
    """
    Validate input data against the JSON schema
    """
    try:
        validate(instance=data, schema=SCHEMA)
    except ValidationError as e:
        raise ValueError(f"Input validation failed: {str(e)}")

def send_to_content_insight(input_data: Dict[str, Any]) -> Dict[str, Any]:
    # This function is not implemented in the provided code
    # It should send the input data to a content insight API and return the analysis
    return {}

def generate_article(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate an article using both GROQ and content insight APIs based on the provided input data
    """
    try:
        # Validate input data against schema
        validate_input(input_data)
        
        # First, get content insight analysis
        content_insight = send_to_content_insight(input_data)
        
        # Prepare prompt for GROQ using content insight and media insights
        prompt = f"""
        Generate an article with the following details:
        
        Brand: {input_data['basicInfo']['brandName']}
        Industry: {input_data['basicInfo']['industryType']}
        Target Audience: {input_data['basicInfo']['targetAudience']}
        
        Key Features:
        {', '.join(input_data['productServiceDetails']['features'])}
        
        USPs:
        {', '.join(input_data['productServiceDetails']['USPs'])}
        
        Primary Problem Solved:
        {input_data['productServiceDetails']['primaryProblemSolved']}
        
        Media Insights:
        - Primary Audience Demographics: {input_data['mediaInsights']['primaryAudienceDemographics']}
        - Pain Points Addressed: {', '.join(input_data['mediaInsights']['painPointsAddressed'])}
        - Market Position: {input_data['mediaInsights']['marketPosition']}
        - Competitors: {', '.join(input_data['mediaInsights']['competitors'])}
        
        Content Insight Analysis:
        {content_insight.get('analysis', 'No additional insights available')}
        
        Article Type: {input_data['articleDetails']['articleType']}
        Required Length: {input_data['articleDetails']['articleLength']} words
        Keywords to Emphasize: {', '.join(input_data['articleDetails']['keywordsToEmphasize'])}
        """
        
        # Generate article using GROQ
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional content writer who specializes in creating engaging and informative articles."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=4000,
            top_p=1,
            stream=False
        )
        
        # Extract the generated article
        generated_article = chat_completion.choices[0].message.content
        
        return {
            "article": generated_article,
            "content_insight": content_insight
        }
        
    except ValidationError as e:
        raise Exception(f"Input validation error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating article: {str(e)}")

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
        },
        "mediaInsights": {
            "primaryAudienceDemographics": "Large enterprises with 1000+ employees",
            "painPointsAddressed": [
                "Inefficient workflows",
                "Lack of data-driven insights",
                "Insufficient security measures"
            ],
            "competitors": [
                "Microsoft",
                "Amazon Web Services",
                "Google Cloud"
            ],
            "marketPosition": "Leader in enterprise automation solutions"
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
