# 🚀 Quick Start Guide - Sri Lanka Tourism Chatbot

## 📋 Prerequisites

- Python 3.7+
- Basic dependencies (Flask, Flask-CORS)

## ⚡ Quick Test (No Dependencies)

Run the standalone test to verify all components work:

```bash
python standalone_test.py
```

This will test:
- ✅ Language detection (5 languages)
- ✅ Intent recognition
- ✅ Knowledge base
- ✅ Full conversation flow

## 🌐 Full Web Demo (With Flask)

### 1. Install Dependencies
```bash
pip install flask flask-cors flask-sqlalchemy flask-migrate
```

### 2. Run the Application
```bash
python run.py
```

### 3. Open Demo
Navigate to: `http://localhost:5000/chatbot_demo.html`

## 🔧 API Testing

### Health Check
```bash
curl http://localhost:5000/api/chatbot/health
```

### Create Session
```bash
curl -X POST http://localhost:5000/api/chatbot/session/create \
  -H "Content-Type: application/json" \
  -d '{"language": "en"}'
```

### Send Message
```bash
curl -X POST http://localhost:5000/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"session_id": "YOUR_SESSION_ID", "message": "Hello!"}'
```

## 📱 Demo Features

### 🌍 Try Different Languages
- **English**: "Hello, what can I visit in Sri Lanka?"
- **Sinhala**: "ආයුබෝවන්, ශ්‍රී ලංකාවේ මොනාද බලන්න පුළුවන්?"
- **Tamil**: "வணக்கம், இலங்கையில் என்ன பார்க்கலாம்?"
- **Chinese**: "你好，斯里兰卡有什么可以参观的？"
- **French**: "Bonjour, que puis-je visiter au Sri Lanka?"

### 🎯 Try Different Intents
- **Attractions**: "Tell me about Sigiriya"
- **Food**: "What's the local cuisine like?"
- **Transport**: "How do I get around?"
- **Weather**: "What's the weather like?"
- **Help**: "Can you help me plan my trip?"

### 👥 Switch Tour Guides
- **Saru**: Cultural expert (temples, history, traditions)
- **Anjali**: Nature lover (wildlife, beaches, outdoors)

## 🎉 What to Expect

### Beautiful Interface
- Modern gradient design
- Responsive mobile-friendly layout
- Real-time typing indicators
- Interactive suggestion buttons
- Language and guide selectors

### Intelligent Responses
- Accurate language detection
- Context-aware replies
- Cultural insights and tips
- Emergency information
- Local etiquette guidance

### Multilingual Experience
- Seamless language switching
- Culturally appropriate responses
- Unicode support for all scripts
- Localized suggestions

## 🔍 Troubleshooting

### Python Import Errors
If you see import errors, run the standalone test first:
```bash
python standalone_test.py
```

### Flask Not Available
Install Flask or use the standalone test:
```bash
pip install flask flask-cors
# OR
python standalone_test.py
```

### Port Already in Use
Change the port in `run.py` or kill existing processes:
```bash
lsof -ti:5000 | xargs kill -9
```

## 📊 Success Indicators

### ✅ Standalone Test Output
```
🇱🇰 Sri Lanka Tourism Chatbot - Standalone Test
📝 Testing Language Detection...
  ✅ Expected: en, Got: en (0.65)
  ✅ Expected: si, Got: si (1.00)
🎯 Testing Intent Recognition...
  ✅ 'Hello there!' -> greeting (0.30)
🤖 Testing Full Chatbot...
  ✅ All tests completed successfully!
```

### ✅ Web Demo Working
- Demo loads at `localhost:5000/chatbot_demo.html`
- Language buttons work
- Messages send and receive responses
- Status shows "🟢 Online"

### ✅ API Responses
```json
{
  "status": "healthy",
  "service": "Sri Lanka Tourism Chatbot API",
  "supported_languages": {...},
  "available_guides": [...]
}
```

## 🎯 Ready for Production

Once working locally, the chatbot can be deployed to:
- **Cloud platforms**: AWS, Google Cloud, Heroku
- **Web servers**: Apache, Nginx
- **Container platforms**: Docker, Kubernetes
- **Mobile apps**: Via REST API integration

Enjoy exploring Sri Lanka with your AI-powered multilingual tour guide! 🇱🇰✨