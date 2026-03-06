"""
🔊 TEXT-TO-SPEECH MODULE
=========================
Handles voice output with customizable rate, volume, and voice selection.
Supports offline speech synthesis for privacy and reliability.
"""

import pyttsx3
import logging
from config import TEXT_TO_SPEECH, ASSISTANT_NAME

logger = logging.getLogger(__name__)


class VoiceAssistant:
    """Manages text-to-speech synthesis."""
    
    def __init__(self):
        """Initialize the TTS engine with configured settings."""
        self.engine = pyttsx3.init(TEXT_TO_SPEECH["engine"])
        self._configure_voice()
        
    def _configure_voice(self):
        """Configure voice parameters (rate, volume, voice index)."""
        try:
            # Get available voices
            voices = self.engine.getProperty('voices')
            
            # Select voice (0 = Male, 1 = Female)
            voice_index = min(
                TEXT_TO_SPEECH["voice_index"], 
                len(voices) - 1
            )
            self.engine.setProperty('voice', voices[voice_index].id)
            
            # Set speech rate
            self.engine.setProperty('rate', TEXT_TO_SPEECH["rate"])
            
            # Set volume (0.0 to 1.0)
            self.engine.setProperty('volume', TEXT_TO_SPEECH["volume"])
            
            logger.info(f"Voice initialized: {voices[voice_index].name}")
            
        except Exception as e:
            logger.error(f"Error configuring voice: {e}")
    
    def speak(self, text):
        """
        Convert text to speech and play it.
        
        Args:
            text (str): Text to speak
        """
        if not text or not isinstance(text, str):
            logger.warning("Invalid text input for speech")
            return
        
        try:
            # Add visual indicator
            print(f"🔊 {ASSISTANT_NAME}: {text}")
            
            # Queue and play speech
            self.engine.say(text)
            self.engine.runAndWait()
            
            # Ensure cleanup
            self.engine.stop()
            
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            print(f"❌ Failed to speak: {text}")
    
    def set_rate(self, rate):
        """
        Adjust speech rate dynamically.
        
        Args:
            rate (int): Words per minute (50-300)
        """
        rate = max(50, min(300, rate))
        self.engine.setProperty('rate', rate)
        
    def set_volume(self, volume):
        """
        Adjust volume dynamically.
        
        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        volume = max(0.0, min(1.0, volume))
        self.engine.setProperty('volume', volume)


# Global instance for backward compatibility
_voice_instance = None


def get_voice_engine():
    """Get or create global voice engine instance."""
    global _voice_instance
    if _voice_instance is None:
        _voice_instance = VoiceAssistant()
    return _voice_instance


def speak(text):
    """
    Global function for simple speech output.
    Called from legacy code.
    
    Args:
        text (str): Text to speak
    """
    engine = get_voice_engine()
    engine.speak(text)
