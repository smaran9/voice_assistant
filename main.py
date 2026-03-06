"""
🤖 JARVIS - LLM POWERED VOICE ASSISTANT
========================================
Main entry point for the Jarvis voice assistant.

Run this file to start the assistant:
    python main.py

Features:
- Voice input/output (offline)
- LLM integration (OpenAI)
- System commands execution
- Semantic memory with vector database
- Customizable personality
- Web interface (Flask)
"""

import logging
import sys
import os
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/jarvis.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Import modules
try:
    from config import ASSISTANT_NAME, USER_NAME, PERSONALITY
    from voice import listen, speak
    from commands import process_command
    from brain import get_brain, get_memory
    from utils.personality import get_personality
    
    logger.info("All modules imported successfully")
except ImportError as e:
    logger.error(f"Failed to import modules: {e}")
    print(f"❌ Import Error: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)


class JarvisAssistant:
    """Main assistant class - manages the listening loop and response pipeline."""
    
    def __init__(self):
        """Initialize the assistant."""
        self.name = ASSISTANT_NAME
        self.user_name = USER_NAME
        self.active = False
        self.brain = get_brain()
        self.memory = get_memory()
        self.personality = get_personality()
        
        logger.info(f"Initializing {self.name}...")
        print(f"\n{'='*50}")
        print(f"🤖 {self.name.upper()} VOICE ASSISTANT")
        print(f"{'='*50}")
        print(f"User: {self.user_name}")
        print(f"Status: Ready")
        print(f"Wake Word: 'Mitra'")
        print(f"Type 'exit' or 'quit' to stop\n")
    
    def __call__(self):
        """Run the main listening loop."""
        self.run()
    
    def run(self):
        """
        Main assistant loop.
        Continuously listens for voice input and processes commands.
        """
        try:
            logger.info(f"{self.name} started")
            print(f"🎤 Listening for wake word: 'Mitra'...\n")
            
            while True:
                try:
                    # ===== STEP 1: Listen for voice input =====
                    user_input = listen()
                    
                    if not user_input:
                        continue
                    
                    print(f"📝 Processing: {user_input}\n")
                    
                    # ===== STEP 2: Check for wake word =====
                    if not self.active:
                        if any(wake_word in user_input for wake_word in ["mitra", "hey mitra"]):
                            self.active = True
                            response = self.personality.format_wake_response()
                            speak(response)
                            continue
                        else:
                            print(f"💤 Not active. Say 'Jarvis' to activate.\n")
                            continue
                    
                    # ===== STEP 3: Check for exit/sleep commands =====
                    if any(cmd in user_input for cmd in ["exit", "quit", "goodbye", "bye"]):
                        response = self.personality.get_closing()
                        speak(response)
                        logger.info(f"{self.name} stopped by user")
                        print(f"\n👋 Goodbye!")
                        break
                    
                    if any(cmd in user_input for cmd in ["sleep", "standby", "quiet"]):
                        self.active = False
                        response = self.personality.format_sleep_response()
                        speak(response)
                        print(f"😴 Entering standby mode...\n")
                        continue
                    
                    # ===== STEP 4: Route and process command =====
                    result = process_command(user_input)
                    
                    # Handle different response types
                    if isinstance(result, dict):
                        response = result.get("response", "Processing complete")
                        command_type = result.get("command_type", "unknown")
                    else:
                        response = result
                        command_type = "general"
                    
                    print(f"✅ [{command_type.upper()}] {response}\n")
                    
                    # ===== STEP 5: Speak response =====
                    speak(response)
                    
                    # ===== STEP 6: Log to memory =====
                    logger.info(f"Command: {user_input} | Type: {command_type}")
                    
                except KeyboardInterrupt:
                    print("\n\n⚠️  Interrupted by user")
                    break
                    
                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
                    error_response = self.personality.get_error_response("general")
                    speak(error_response)
                    print(f"❌ Error: {e}\n")
        
        except Exception as e:
            logger.critical(f"Critical error: {e}")
            print(f"❌ CRITICAL ERROR: {e}")
        
        finally:
            logger.info(f"{self.name} shutdown")
            print(f"\n{'='*50}")
            print(f"✓ {self.name} shutdown complete")
            print(f"{'='*50}\n")


def run_web_interface():
    """
    Alternative: Run web interface with Flask.
    Use this for HTTP-based control.
    """
    from flask import Flask, render_template, jsonify, request
    
    app = Flask(__name__, template_folder='templates', static_folder='static')
    assistant = JarvisAssistant()
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/listen', methods=['POST'])
    def listen_route():
        """API endpoint for voice input."""
        try:
            user_input = listen()
            
            if not user_input:
                return jsonify({"error": "No speech detected"}), 400
            
            result = process_command(user_input)
            
            if isinstance(result, dict):
                response = result.get("response", "Processing complete")
            else:
                response = result
            
            return jsonify({
                "input": user_input,
                "response": response
            })
        
        except Exception as e:
            logger.error(f"API error: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/status', methods=['GET'])
    def status():
        """Get assistant status."""
        return jsonify({
            "name": ASSISTANT_NAME,
            "user": USER_NAME,
            "active": True,
            "timestamp": datetime.now().isoformat()
        })
    
    logger.info("Starting web interface on http://localhost:5000")
    print("\n🌐 Starting Jarvis Web Interface")
    print("📍 Open: http://localhost:5000\n")
    
    app.run(debug=False, port=5000, host='0.0.0.0')


def main():
    """Entry point - choose mode."""
    print("\nSelect mode:")
    print("1. Voice Interface (Console)")
    print("2. Web Interface (Browser)")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        assistant = JarvisAssistant()
        assistant.run()
    
    elif choice == "2":
        try:
            run_web_interface()
        except ImportError:
            print("❌ Flask not installed. Run: pip install flask")
            sys.exit(1)
    
    elif choice == "3":
        print("Goodbye!")
        sys.exit(0)
    
    else:
        print("Invalid choice")
        sys.exit(1)


if __name__ == "__main__":
    main()
