"""
LLM helper functions for OpenAI integration
"""
import os
import json
import logging

from typing import Any, Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


def get_llm() -> OpenAI:
    """
    Get configured OpenAI client instance
    
    Returns:
        OpenAI: Configured OpenAI client
    """
    api_key = os.getenv("OPENAI_API_KEY", "lm-studio")
    base_url = os.getenv("OPENAI_API_BASE", None)
    
    client_kwargs = {"api_key": api_key}
    
    if base_url:
        client_kwargs["base_url"] = base_url
    
    return OpenAI(**client_kwargs)


def call_llm_with_structured_output(
    system_prompt: str,
    user_input: str,
    model: Optional[str] = None,
    temperature: float = 0.0
) -> Dict[str, Any]:
    """
    Call LLM and parse structured JSON output
    
    Args:
        system_prompt: System prompt with instructions
        user_input: User input/query
        model: Model name
        temperature: Temperature setting
        
    Returns:
        Dict: Parsed JSON response
        
    Raises:
        ValueError: If response is not valid JSON
    """
    if model is None:
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    client = get_llm()
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        
        # Extract content from response
        content = response.choices[0].message.content
        
        # Log response
        tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else None
        logger.info(f"Tokens Used: {tokens_used}")
        
        # Parse JSON from response
        try:
            # Try to extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            logger.info(f"Successfully parsed JSON response with {len(result)} keys")
            logger.info(f"LLM Response: \n{result}")
            return result
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from LLM response: {str(e)}")
            raise ValueError(f"LLM response is not valid JSON: {content}") from e
            
    except Exception as e:
        logger.error(f"LLM call failed: {str(e)}")
        raise


def call_llm_with_text_output(
    system_prompt: str,
    user_input: str,
    model: Optional[str] = None,
    temperature: float = 0.3
) -> str:
    """
    Call LLM and get text output
    
    Args:
        system_prompt: System prompt with instructions
        user_input: User input/query
        model: Model name
        temperature: Temperature setting
        
    Returns:
        str: Text response
    """
    if model is None:
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    client = get_llm()
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        
        # Extract content from response
        content = response.choices[0].message.content
        
        # Log response
        tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else None
        logger.info(f"Tokens Used: {tokens_used}")
        
        return content
        
    except Exception as e:
        logger.error(f"LLM call failed: {str(e)}")
        raise
