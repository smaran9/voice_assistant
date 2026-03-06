"""
🎭 PERSONALITY ENGINE
======================
Customizable personality and response styling.
Makes the assistant feel natural, consistent, and charming.
"""

import logging
import random
from config import PERSONALITY, USER_NAME, ASSISTANT_NAME

logger = logging.getLogger(__name__)


class PersonalityEngine:
    """
    Manages assistant personality, tone, and response formatting.
    """
    
    def __init__(self):
        """Initialize personality with config settings."""
        self.name = ASSISTANT_NAME
        self.user_name = USER_NAME
        self.personality = PERSONALITY
        
    def format_response(self, response, tone="neutral"):
        """
        Format response with personality touches.
        
        Args:
            response (str): Raw response text
            tone (str): Response tone (neutral, casual, formal, motivational)
            
        Returns:
            str: Formatted response
        """
        if not response:
            return "I'm processing that request."
        
        # Add personality prefix
        if random.random() > 0.5:
            response = f"{self.personality['prefix']}, {self.user_name}. {response}"
        
        # Apply tone
        if tone == "motivational":
            response = self._add_motivation(response)
        elif tone == "casual":
            response = self._add_casual_touches(response)
        elif tone == "formal":
            response = self._add_formality(response)
        
        return response
    
    def _add_motivation(self, text):
        """Add motivational touches to response."""
        motivational_phrases = [
            "You've got this.",
            "That's a great question.",
            "Smart thinking.",
            "Let's make it happen.",
            "You're on the right track."
        ]
        return f"{text} {random.choice(motivational_phrases)}"
    
    def _add_casual_touches(self, text):
        """Make response more casual and friendly."""
        return text
    
    def _add_formality(self, text):
        """Add formal language."""
        return text
    
    def get_greeting(self, time_of_day="morning"):
        """
        Generate time-appropriate greeting.
        
        Args:
            time_of_day (str): morning, afternoon, evening, night
            
        Returns:
            str: Greeting message
        """
        greetings = {
            "morning": f"Good morning, {self.user_name}. Ready to seize the day.",
            "afternoon": f"Good afternoon, {self.user_name}. What's next?",
            "evening": f"Good evening, {self.user_name}. Winding down?",
            "night": f"Good night, {self.user_name}. Time to rest."
        }
        
        return greetings.get(time_of_day, f"Hello, {self.user_name}.")
    
    def get_closing(self):
        """
        Generate closing statement.
        
        Returns:
            str: Closing message
        """
        closings = [
            f"At your service, {self.user_name}.",
            f"Anytime, {self.user_name}.",
            f"Ready for the next task.",
            f"Standing by, {self.user_name}.",
            f"Until next time."
        ]
        
        return random.choice(closings)
    
    def get_error_response(self, error_type="general"):
        """
        Generate empathetic error responses.
        
        Args:
            error_type (str): Type of error
            
        Returns:
            str: Error message with personality
        """
        errors = {
            "general": f"I apologize, {self.user_name}. Let me try that again.",
            "not_understood": f"I didn't quite catch that. Could you repeat, {self.user_name}?",
            "api_error": "I'm having trouble reaching my systems. Technical adjustment in progress.",
            "mic_error": "I'm not hearing you clearly. Please check your microphone.",
            "unknown_command": f"That's outside my current capabilities, {self.user_name}. What else can I help with?"
        }
        
        return errors.get(error_type, errors["general"])
    
    def format_wake_response(self):
        """
        Format response when wake word is detected.
        
        Returns:
            str: Wake-up message
        """
        responses = [
            f"I'm awake, {self.user_name}. What do you need?",
            f"At your service.",
            f"Hello, {self.user_name}. I'm ready.",
            f"Activated. Awaiting your command."
        ]
        
        return random.choice(responses)
    
    def format_sleep_response(self):
        """
        Format response when going into sleep mode.
        
        Returns:
            str: Sleep message
        """
        responses = [
            f"Going into standby, {self.user_name}.",
            "Entering sleep mode. See you soon.",
            f"Rest well, {self.user_name}. I'll be here.",
            "Powering down. Wake me anytime."
        ]
        
        return random.choice(responses)
    
    def add_personality_to_llm_response(self, llm_response):
        """
        Post-process LLM response to add personality.
        
        Args:
            llm_response (str): Response from LLM
            
        Returns:
            str: Personality-enhanced response
        """
        # Truncate for voice (max 2-3 sentences)
        sentences = llm_response.split('.')
        if len(sentences) > 3:
            llm_response = '.'.join(sentences[:3]) + '.'
        
        return llm_response.strip()
    
    def get_personality_info(self):
        """
        Return current personality configuration.
        
        Returns:
            dict: Personality details
        """
        return {
            "name": self.name,
            "user_name": self.user_name,
            "tone": self.personality["tone"],
            "style": self.personality["style"]
        }


# Global personality instance
_personality_instance = None


def get_personality():
    """Get or create global personality engine instance."""
    global _personality_instance
    if _personality_instance is None:
        _personality_instance = PersonalityEngine()
    return _personality_instance


def format_response(text, tone="neutral"):
    """
    Simple function to format response with personality.
    
    Args:
        text (str): Base response
        tone (str): Response tone
        
    Returns:
        str: Formatted response
    """
    engine = get_personality()
    return engine.format_response(text, tone)
