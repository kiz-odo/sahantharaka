#!/usr/bin/env python3
"""
Setup script for Sri Lanka Tourism Chatbot
This script initializes the entire project with all necessary components.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class TourismChatbotSetup:
    def __init__(self):
        self.project_root = Path.cwd()
        self.rasa_bot_dir = self.project_root / "rasa_bot"
        self.web_interface_dir = self.project_root / "web_interface"
        self.database_dir = self.project_root / "database"

    def print_banner(self):
        """Print the setup banner"""
        print("=" * 60)
        print("🇱🇰 Sri Lanka Tourism Chatbot - Setup")
        print("=" * 60)
        print("This script will set up the complete tourism chatbot project.")
        print("It includes Rasa chatbot, web interface, and database setup.")
        print("=" * 60)

    def check_python_version(self):
        """Check if Python version is compatible"""
        print("🔍 Checking Python version...")
        if sys.version_info < (3, 8):
            print("❌ Python 3.8 or higher is required!")
            sys.exit(1)
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

    def install_dependencies(self):
        """Install Python dependencies"""
        print("\n📦 Installing Python dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, capture_output=True, text=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("Please install dependencies manually: pip install -r requirements.txt")
            return False
        return True

    def setup_rasa(self):
        """Set up Rasa chatbot"""
        print("\n🤖 Setting up Rasa chatbot...")
        
        # Change to rasa_bot directory
        os.chdir(self.rasa_bot_dir)
        
        try:
            # Initialize Rasa project if not already done
            if not (self.rasa_bot_dir / "config.yml").exists():
                print("Initializing Rasa project...")
                subprocess.run(["rasa", "init", "--no-prompt"], check=True, capture_output=True)
                print("✅ Rasa project initialized")
            
            # Train the model
            print("Training Rasa model...")
            subprocess.run(["rasa", "train"], check=True, capture_output=True)
            print("✅ Rasa model trained successfully")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Rasa setup failed: {e}")
            return False
        finally:
            # Return to project root
            os.chdir(self.project_root)
        
        return True

    def setup_database(self):
        """Set up the database"""
        print("\n🗄️ Setting up database...")
        
        try:
            # Run database migration
            subprocess.run([sys.executable, "database/migrate.py"], check=True, capture_output=True)
            print("✅ Database setup completed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Database setup failed: {e}")
            return False
        
        return True

    def create_env_file(self):
        """Create .env file with default configuration"""
        print("\n⚙️ Creating environment configuration...")
        
        env_content = """# Sri Lanka Tourism Chatbot Environment Configuration

# Database Configuration
DATABASE_URL=sqlite:///tourism_chatbot.db

# Rasa Server Configuration
RASA_SERVER_URL=http://localhost:5005

# Language Detection
LANGUAGE_DETECTION_ENABLED=true

# Web Interface Configuration
PORT=5000
FLASK_DEBUG=false

# Optional: PostgreSQL Configuration (uncomment to use PostgreSQL)
# DATABASE_URL=postgresql://username:password@localhost:5432/tourism_db

# Optional: MySQL Configuration (uncomment to use MySQL)
# DATABASE_URL=mysql://username:password@localhost:3306/tourism_db
"""
        
        env_file = self.project_root / ".env"
        if not env_file.exists():
            with open(env_file, "w") as f:
                f.write(env_content)
            print("✅ Created .env file with default configuration")
        else:
            print("ℹ️ .env file already exists")

    def create_startup_scripts(self):
        """Create startup scripts for easy deployment"""
        print("\n🚀 Creating startup scripts...")
        
        # Create start_rasa.sh
        rasa_script = """#!/bin/bash
# Start Rasa server for Sri Lanka Tourism Chatbot

echo "🤖 Starting Rasa server..."
cd "$(dirname "$0")/rasa_bot"

# Check if model exists
if [ ! -f "models/latest.tar.gz" ]; then
    echo "❌ Rasa model not found. Please run setup.py first."
    exit 1
fi

# Start Rasa server
rasa run --enable-api --cors "*" --port 5005
"""
        
        with open(self.project_root / "start_rasa.sh", "w") as f:
            f.write(rasa_script)
        os.chmod(self.project_root / "start_rasa.sh", 0o755)
        
        # Create start_web.sh
        web_script = """#!/bin/bash
# Start web interface for Sri Lanka Tourism Chatbot

echo "🌐 Starting web interface..."
cd "$(dirname "$0")/web_interface"

# Start Flask application
python app.py
"""
        
        with open(self.project_root / "start_web.sh", "w") as f:
            f.write(web_script)
        os.chmod(self.project_root / "start_web.sh", 0o755)
        
        # Create start_all.sh
        all_script = """#!/bin/bash
# Start all services for Sri Lanka Tourism Chatbot

echo "🚀 Starting Sri Lanka Tourism Chatbot..."

# Start Rasa server in background
echo "🤖 Starting Rasa server..."
cd "$(dirname "$0")/rasa_bot"
rasa run --enable-api --cors "*" --port 5005 &
RASA_PID=$!

# Wait a moment for Rasa to start
sleep 5

# Start web interface
echo "🌐 Starting web interface..."
cd "$(dirname "$0")/web_interface"
python app.py &
WEB_PID=$!

echo "✅ All services started!"
echo "📡 Rasa server: http://localhost:5005"
echo "🌐 Web interface: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user to stop
trap "echo '🛑 Stopping services...'; kill $RASA_PID $WEB_PID; exit" INT
wait
"""
        
        with open(self.project_root / "start_all.sh", "w") as f:
            f.write(all_script)
        os.chmod(self.project_root / "start_all.sh", 0o755)
        
        print("✅ Created startup scripts")

    def create_test_script(self):
        """Create a test script to verify the setup"""
        print("\n🧪 Creating test script...")
        
        test_script = """#!/usr/bin/env python3
\"\"\"
Test script for Sri Lanka Tourism Chatbot
This script tests the basic functionality of the chatbot.
\"\"\"

import requests
import json
import time

def test_rasa_server():
    \"\"\"Test if Rasa server is running\"\"\"
    try:
        response = requests.get("http://localhost:5005/status", timeout=5)
        if response.status_code == 200:
            print("✅ Rasa server is running")
            return True
        else:
            print("❌ Rasa server returned error")
            return False
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to Rasa server")
        return False

def test_web_interface():
    \"\"\"Test if web interface is running\"\"\"
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                print("✅ Web interface is running")
                return True
            else:
                print("❌ Web interface health check failed")
                return False
        else:
            print("❌ Web interface returned error")
            return False
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to web interface")
        return False

def test_chat_functionality():
    \"\"\"Test basic chat functionality\"\"\"
    try:
        response = requests.post("http://localhost:5000/api/chat", 
                               json={"message": "Hello", "session_id": "test_session"},
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Chat functionality is working")
                return True
            else:
                print("❌ Chat functionality failed")
                return False
        else:
            print("❌ Chat API returned error")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Chat test failed: {e}")
        return False

def main():
    \"\"\"Run all tests\"\"\"
    print("🧪 Testing Sri Lanka Tourism Chatbot...")
    print("=" * 50)
    
    tests = [
        ("Rasa Server", test_rasa_server),
        ("Web Interface", test_web_interface),
        ("Chat Functionality", test_chat_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\\nTesting {test_name}...")
        if test_func():
            passed += 1
        time.sleep(1)
    
    print("\\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The chatbot is ready to use.")
        print("\\n🌐 Open http://localhost:5000 in your browser to start chatting!")
    else:
        print("⚠️ Some tests failed. Please check the setup and try again.")

if __name__ == "__main__":
    main()
"""
        
        with open(self.project_root / "test_chatbot.py", "w") as f:
            f.write(test_script)
        os.chmod(self.project_root / "test_chatbot.py", 0o755)
        
        print("✅ Created test script")

    def print_completion_message(self):
        """Print completion message with next steps"""
        print("\n" + "=" * 60)
        print("🎉 Setup completed successfully!")
        print("=" * 60)
        print("\n📋 Next steps:")
        print("1. Start the chatbot:")
        print("   ./start_all.sh")
        print("\n2. Or start services separately:")
        print("   ./start_rasa.sh    # Terminal 1")
        print("   ./start_web.sh     # Terminal 2")
        print("\n3. Test the setup:")
        print("   python test_chatbot.py")
        print("\n4. Open in browser:")
        print("   http://localhost:5000")
        print("\n📚 Documentation:")
        print("   - README.md for detailed instructions")
        print("   - Check the docs/ folder for additional information")
        print("\n🔧 Configuration:")
        print("   - Edit .env file to customize settings")
        print("   - Modify rasa_bot/domain.yml for chatbot responses")
        print("   - Update web_interface/templates/ for UI changes")
        print("\n" + "=" * 60)

    def run_setup(self):
        """Run the complete setup process"""
        self.print_banner()
        
        # Check Python version
        self.check_python_version()
        
        # Install dependencies
        if not self.install_dependencies():
            print("❌ Setup failed at dependency installation")
            return False
        
        # Setup Rasa
        if not self.setup_rasa():
            print("❌ Setup failed at Rasa setup")
            return False
        
        # Setup database
        if not self.setup_database():
            print("❌ Setup failed at database setup")
            return False
        
        # Create environment file
        self.create_env_file()
        
        # Create startup scripts
        self.create_startup_scripts()
        
        # Create test script
        self.create_test_script()
        
        # Print completion message
        self.print_completion_message()
        
        return True

def main():
    """Main function"""
    setup = TourismChatbotSetup()
    success = setup.run_setup()
    
    if not success:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()