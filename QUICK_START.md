# Quick Start Guide - Sri Lanka Tourism Chatbot

Get your multilingual tourism chatbot up and running in minutes!

## 🚀 Quick Setup (5 minutes)

### 1. Prerequisites
- Python 3.8 or higher
- Git

### 2. Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd sri_lanka_tourism_chatbot

# Run automated setup (this will install everything)
python setup.py
```

### 3. Start the Chatbot
```bash
# Start all services at once
./start_all.sh
```

### 4. Open in Browser
Visit: **http://localhost:5000**

That's it! Your chatbot is ready to use! 🎉

## 📋 What You Get

✅ **Multilingual Support**: English, Sinhala, Tamil  
✅ **Tourist Information**: Attractions, food, transport, accommodation  
✅ **Emergency Services**: Contact numbers and embassy info  
✅ **Modern Web Interface**: Responsive design with beautiful UI  
✅ **Real-time Chat**: Instant responses powered by Rasa  
✅ **Database**: Pre-populated with Sri Lanka tourism data  

## 🧪 Test the Chatbot

Try these example questions:

**English:**
- "What are the popular tourist attractions?"
- "Tell me about Sri Lankan food"
- "How do I get around Sri Lanka?"
- "Emergency contact numbers"

**Sinhala:**
- "ශ්‍රී ලංකාවේ සංචාරක ආකරෂණ මොනවාද?"
- "ශ්‍රී ලාංකික ආහාර ගැන කියන්න"

**Tamil:**
- "இலங்கையில் சுற்றுலா இடங்கள் என்ன?"
- "இலங்கை உணவு பற்றி சொல்லுங்கள்"

## 🔧 Manual Setup (Alternative)

If the automated setup doesn't work:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Rasa
```bash
cd rasa_bot
rasa init --no-prompt
rasa train
cd ..
```

### 3. Setup Database
```bash
python database/migrate.py
```

### 4. Start Services
```bash
# Terminal 1: Start Rasa
cd rasa_bot
rasa run --enable-api --cors "*" --port 5005

# Terminal 2: Start Web Interface
cd web_interface
python app.py
```

## 🌐 Access Points

- **Web Interface**: http://localhost:5000
- **Rasa Server**: http://localhost:5005
- **API Health Check**: http://localhost:5000/api/health

## 📱 Features Overview

### Welcome Screen
- Quick action buttons for common questions
- Tourism information cards
- Language selector

### Chat Interface
- Real-time messaging
- Message timestamps
- Character counter
- Voice input (coming soon)
- Typing indicators

### Supported Topics
- 🏛️ **Attractions**: Sigiriya, Nuwara Eliya, Galle Fort, Yala
- 🍽️ **Food**: Rice and Curry, Kottu Roti, Hoppers
- 🚌 **Transport**: Trains, Buses, Taxis/Tuk-tuks
- 🏨 **Accommodation**: Hotels, guesthouses, eco-lodges
- 🚨 **Emergency**: Contact numbers, tourist police
- 💰 **Currency**: Exchange rates, money exchange
- 📋 **Visa**: ETA requirements, application process
- 🌤️ **Weather**: Best time to visit, climate info

## 🔍 Troubleshooting

### Common Issues

**"Rasa command not found"**
```bash
pip install rasa
```

**"Port already in use"**
```bash
# Kill processes using ports 5000 and 5005
lsof -ti:5000 | xargs kill -9
lsof -ti:5005 | xargs kill -9
```

**"Database error"**
```bash
# Recreate database
rm tourism_chatbot.db
python database/migrate.py
```

**"Web interface not loading"**
```bash
# Check if Flask is running
curl http://localhost:5000/api/health
```

### Debug Mode
```bash
# Enable debug for development
export FLASK_DEBUG=true
python web_interface/app.py
```

## 📊 Test Your Setup

Run the automated test:
```bash
python test_chatbot.py
```

Expected output:
```
🧪 Testing Sri Lanka Tourism Chatbot...
==================================================

Testing Rasa Server...
✅ Rasa server is running

Testing Web Interface...
✅ Web interface is running

Testing Chat Functionality...
✅ Chat functionality is working

==================================================
Test Results: 3/3 tests passed
🎉 All tests passed! The chatbot is ready to use.
```

## 🎯 Next Steps

### Customization
1. **Add more attractions**: Edit `database/migrate.py`
2. **Modify responses**: Edit `rasa_bot/domain.yml`
3. **Change UI**: Edit `web_interface/templates/index.html`
4. **Add new intents**: Edit `rasa_bot/data/nlu.yml`