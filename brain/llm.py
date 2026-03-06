"""
🧠 LLM BRAIN - OPENAI INTEGRATION
===================================
Handles natural language processing and conversational AI.
Uses OpenAI GPT for intelligent responses.
"""

import openai
import logging
import json
from datetime import datetime
from config import (
    OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE,
    OPENAI_MAX_TOKENS, CONTEXT_INJECTION_PROMPT,
    USER_NAME, ASSISTANT_NAME, ERROR_MESSAGES
)

logger = logging.getLogger(__name__)

# Configure OpenAI API
openai.api_key = OPENAI_API_KEY


class JarvisBrain:
    """
    LLM-powered conversational engine.
    Manages context, conversation history, and intelligent responses.
    """
    
    def __init__(self):
        """Initialize the brain with empty conversation history."""
        self.conversation_history = []
        self.max_history = 10
        
    def add_to_history(self, role, content):
        """
        Add a message to conversation history.
        
        Args:
            role (str): "user" or "assistant"
            content (str): Message content
        """
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        
        # Keep only recent history to avoid token limits
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def get_response(self, user_input, use_context=True):
        """
        Get AI response from OpenAI API.
        
        Args:
            user_input (str): User's message
            use_context (bool): Include conversation history
            
        Returns:
            dict: {
                "response": str,
                "success": bool,
                "tokens_used": int
            }
        """
        if not user_input or not isinstance(user_input, str):
            return {
                "response": ERROR_MESSAGES["unknown_command"],
                "success": False,
                "tokens_used": 0
            }
        
        try:
            # Build messages list
            messages = []
            
            # Add system context
            if use_context:
                messages.append({
                    "role": "system",
                    "content": CONTEXT_INJECTION_PROMPT
                })
            
            # Add conversation history
            if use_context and self.conversation_history:
                messages.extend(self.conversation_history)
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=OPENAI_TEMPERATURE,
                max_tokens=OPENAI_MAX_TOKENS,
                timeout=10
            )
            
            # Extract response
            assistant_message = response['choices'][0]['message']['content'].strip()
            tokens_used = response['usage']['total_tokens']
            
            # Update history
            self.add_to_history("user", user_input)
            self.add_to_history("assistant", assistant_message)
            
            logger.info(f"LLM Response - Tokens: {tokens_used}")
            
            return {
                "response": assistant_message,
                "success": True,
                "tokens_used": tokens_used
            }
            
        except openai.error.AuthenticationError:
            logger.error("OpenAI API authentication failed")
            return {
                "response": "API authentication failed. Check your API key.",
                "success": False,
                "tokens_used": 0
            }
            
        except openai.error.RateLimitError:
            logger.warning("OpenAI rate limit exceeded")
            return {
                "response": "I'm handling too many requests. Please try again in a moment.",
                "success": False,
                "tokens_used": 0
            }
            
        except openai.error.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return {
                "response": ERROR_MESSAGES["api_failure"],
                "success": False,
                "tokens_used": 0
            }
            
        except Exception as e:
            logger.error(f"Unexpected error in get_response: {e}")
            return {
                "response": "An unexpected error occurred.",
                "success": False,
                "tokens_used": 0
            }
    
    def ask_coding_question(self, question):
        """
        Specialized method for coding-related questions.
        
        Args:
            question (str): Coding question
            
        Returns:
            str: Code explanation or solution
        """
        prompt = f"""
        The user is asking a coding question. Provide a concise, practical answer.
        Question: {question}
        
        Keep the response brief (2-3 sentences max) and suited for voice delivery.
        """
        
        result = self.get_response(prompt, use_context=False)
        return result["response"]
    
    def ask_general_question(self, question):
        """
        Handle general knowledge questions.
        
        Args:
            question (str): Any question
            
        Returns:
            str: Answer
        """
        return self.get_response(question)["response"]
    
    def summarize_context(self):
        """
        Generate a summary of the current conversation context.
        Useful for memory refresh.
        
        Returns:
            str: Brief summary of conversation
        """
        if not self.conversation_history:
            return "No active conversation."
        
        # Use last 5 messages for summary
        recent = self.conversation_history[-5:]
        summary_prompt = "Summarize this conversation: " + str(recent)
        
        result = self.get_response(summary_prompt, use_context=False)
        return result["response"]


# Global brain instance
_brain_instance = None


def get_brain():
    """Get or create global brain instance."""
    global _brain_instance
    if _brain_instance is None:
        _brain_instance = JarvisBrain()
    return _brain_instance


def ask_llm(user_input):
    """
    Simple function to ask the LLM something.
    
    Args:
        user_input (str): Question or request
        
    Returns:
        str: LLM response
    """
    brain = get_brain()
    result = brain.get_response(user_input)
    return result["response"]
