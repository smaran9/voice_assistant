"""
🎤 VOICE INPUT MODULE
=======================
Handles microphone listening, noise adjustment, and speech-to-text conversion.
"""

import speech_recognition as sr
import logging
from config import MICROPHONE_SETTINGS, WAKE_WORDS, ERROR_MESSAGES

logger = logging.getLogger(__name__)


class MicrophoneListener:
    """Manages microphone input and speech recognition."""
    
    def __init__(self):
        """Initialize the speech recognizer."""
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = MICROPHONE_SETTINGS["energy_threshold"]
        self.recognizer.pause_threshold = MICROPHONE_SETTINGS["pause_threshold"]
        
    def listen(self, timeout=MICROPHONE_SETTINGS["phrase_time_limit"]):
        """
        Listen for speech input from microphone.
        
        Args:
            timeout (int): Maximum seconds to listen
            
        Returns:
            str: Recognized speech as lowercase text, or empty string if failed
        """
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Capture audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=timeout
                )
            
            # Convert speech to text using Google API
            text = self.recognizer.recognize_google(audio)
            print(f"✓ You: {text}")
            return text.lower()
            
        except sr.UnknownValueError:
            logger.warning("Speech not understood")
            return ""
            
        except sr.RequestError as e:
            logger.error(f"Google Speech API error: {e}")
            return ""
            
        except sr.MicrophoneError:
            logger.error(ERROR_MESSAGES["mic_not_found"])
            print(f"❌ {ERROR_MESSAGES['mic_not_found']}")
            return ""
            
        except Exception as e:
            logger.error(f"Unexpected error in listen(): {e}")
            return ""
    
    def detect_wake_word(self, text):
        """
        Check if wake word is in the recognized text.
        
        Args:
            text (str): Recognized speech text
            
        Returns:
            bool: True if wake word detected
        """
        if not text:
            return False
        return any(wake_word in text for wake_word in WAKE_WORDS)


def listen():
    """
    Global function for simple listening.
    Called from legacy code.
    
    Returns:
        str: Recognized speech
    """
    listener = MicrophoneListener()
    return listener.listen()
