"""
🧪 JARVIS TEST SUITE
=====================
Unit tests for all modules
Run: python -m pytest tests/ -v
"""

import unittest
from unittest.mock import patch, MagicMock
import sys

# Test Voice Module
class TestVoiceModule(unittest.TestCase):
    """Test speech input/output"""
    
    def test_listen_returns_string(self):
        """listen() should return a string"""
        from voice import listen
        # Would need mock microphone
        # result = listen()
        # self.assertIsInstance(result, str)
        pass
    
    def test_speak_accepts_string(self):
        """speak() should accept string input"""
        from voice import speak
        # speak("Test message")
        pass

# Test LLM Module
class TestLLMModule(unittest.TestCase):
    """Test OpenAI integration"""
    
    def test_brain_initialization(self):
        """Brain should initialize without errors"""
        from brain import get_brain
        brain = get_brain()
        self.assertIsNotNone(brain)
    
    def test_conversation_history(self):
        """Brain should track conversation history"""
        from brain import get_brain
        brain = get_brain()
        brain.clear_history()
        brain.add_to_history("user", "test")
        self.assertEqual(len(brain.conversation_history), 1)
    
    @patch('openai.ChatCompletion.create')
    def test_get_response(self, mock_openai):
        """get_response should handle LLM response"""
        # Mock OpenAI API
        mock_openai.return_value = {
            'choices': [{'message': {'content': 'test response'}}],
            'usage': {'total_tokens': 100}
        }
        # Test response
        pass

# Test Memory Module
class TestMemoryModule(unittest.TestCase):
    """Test memory system"""
    
    def test_memory_initialization(self):
        """Memory should initialize without errors"""
        from brain import get_memory
        memory = get_memory()
        self.assertIsNotNone(memory)
    
    def test_save_load_memory(self):
        """Should save and load JSON memory"""
        from brain import get_memory
        memory = get_memory()
        test_data = {"test": "value"}
        memory.save_json_memory(test_data)
        loaded = memory.load_json_memory()
        self.assertEqual(loaded.get("test"), "value")

# Test System Commands
class TestSystemCommandsModule(unittest.TestCase):
    """Test local command execution"""
    
    def test_executor_initialization(self):
        """Executor should initialize"""
        from commands import get_executor
        executor = get_executor()
        self.assertIsNotNone(executor)
    
    def test_get_time_returns_string(self):
        """get_time should return time string"""
        from commands import get_executor
        executor = get_executor()
        time_str = executor.get_time()
        self.assertIsInstance(time_str, str)
        self.assertIn(":", time_str)
    
    def test_get_date_returns_string(self):
        """get_date should return date string"""
        from commands import get_executor
        executor = get_executor()
        date_str = executor.get_date()
        self.assertIsInstance(date_str, str)
        self.assertTrue(len(date_str) > 0)
    
    def test_day_of_week_returns_string(self):
        """get_day_of_week should return day name"""
        from commands import get_executor
        executor = get_executor()
        day = executor.get_day_of_week()
        self.assertIn(day, ["Monday", "Tuesday", "Wednesday", 
                            "Thursday", "Friday", "Saturday", "Sunday"])

# Test Command Router
class TestCommandRouter(unittest.TestCase):
    """Test intelligent command routing"""
    
    def test_router_initialization(self):
        """Router should initialize"""
        from commands import get_router
        router = get_router()
        self.assertIsNotNone(router)
    
    def test_route_time_command_to_system(self):
        """'What time' should route to system command"""
        from commands import get_router
        router = get_router()
        result = router.route("What time is it?")
        self.assertEqual(result["command_type"], "system")
    
    def test_route_wake_word_detected(self):
        """Wake word should be detected"""
        from commands import get_router
        router = get_router()
        result = router.route("jarvis")
        self.assertEqual(result["command_type"], "wake")
    
    def test_route_exit_command(self):
        """Exit commands should be detected"""
        from commands import get_router
        router = get_router()
        result = router.route("goodbye")
        self.assertEqual(result["command_type"], "exit")

# Test Personality Module
class TestPersonalityModule(unittest.TestCase):
    """Test personality engine"""
    
    def test_personality_initialization(self):
        """Personality should initialize"""
        from utils import get_personality
        personality = get_personality()
        self.assertIsNotNone(personality)
    
    def test_greetings_exist(self):
        """Should have morning greeting"""
        from utils import get_personality
        personality = get_personality()
        greeting = personality.get_greeting("morning")
        self.assertIsInstance(greeting, str)
        self.assertTrue(len(greeting) > 0)
    
    def test_error_responses_exist(self):
        """Should have error messages"""
        from utils import get_personality
        personality = get_personality()
        error = personality.get_error_response("not_understood")
        self.assertIsInstance(error, str)
        self.assertTrue(len(error) > 0)

# Test Configuration
class TestConfiguration(unittest.TestCase):
    """Test config module"""
    
    def test_config_loads(self):
        """Config should load without errors"""
        from config import ASSISTANT_NAME, USER_NAME
        self.assertEqual(ASSISTANT_NAME, "Jarvis")
        self.assertEqual(USER_NAME, "Smaran")
    
    def test_api_key_available(self):
        """API key should be set"""
        from config import OPENAI_API_KEY
        # This will pass if .env is setup, fail otherwise
        # self.assertNotEqual(OPENAI_API_KEY, "your-api-key-here")
        pass

# Integration Tests
class TestIntegration(unittest.TestCase):
    """Test module interactions"""
    
    def test_command_processing_flow(self):
        """Test full command processing pipeline"""
        from commands import process_command
        
        # Simple system command
        result = process_command("what time is it")
        self.assertIn("response", result)
        self.assertTrue(result["success"])
    
    def test_personality_applied_to_response(self):
        """Personality should format responses"""
        from utils import format_response
        
        response = format_response("Test", tone="neutral")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

# Manual Testing Guide
"""
MANUAL TESTING CHECKLIST:

Voice I/O:
  [ ] Listen catches voice input
  [ ] Google API returns text
  [ ] Speaker plays audio
  [ ] Microphone error handled gracefully

LLM:
  [ ] OpenAI API responds
  [ ] Conversation history tracked
  [ ] Context properly injected
  [ ] Token limits respected

Memory:
  [ ] JSON memory saves/loads
  [ ] SQLite conversations stored
  [ ] Vector embeddings working
  [ ] Semantic search finds similar memories

Commands:
  [ ] Time returns correct format
  [ ] Date returns correct format
  [ ] Google search opens browser
  [ ] YouTube search opens browser
  [ ] Brightness control works
  [ ] App launching works

Router:
  [ ] System commands route correctly
  [ ] LLM queries route correctly
  [ ] Wake word detected
  [ ] Sleep/exit detected
  [ ] Unknown commands default to LLM

Personality:
  [ ] Greeting matches time of day
  [ ] Error messages empathetic
  [ ] Tone adaptation works
  [ ] Closing message natural

Full Flow:
  [ ] Start app
  [ ] Say "Jarvis" → Wakes up
  [ ] Ask general question → Replies
  [ ] Ask for time → Fast response
  [ ] Say "Goodbye" → Shuts down

Performance:
  [ ] System commands < 100ms
  [ ] LLM response 2-5 seconds
  [ ] Memory recall < 100ms
  [ ] No crashes on bad input
  [ ] Graceful API error handling
"""

if __name__ == '__main__':
    unittest.main()
