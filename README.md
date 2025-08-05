# Multilingual Chatbot for Sri Lanka Tourism

A comprehensive conversational AI system designed to assist tourists visiting Sri Lanka by providing information in Sinhala, Tamil, and English languages.

## 🌟 Features

- **Multilingual Support**: Sinhala, Tamil, and English
- **Tourist Information**: Attractions, food, culture, transportation
- **Emergency Services**: Contact numbers and embassy information
- **Accommodation Guidance**: Hotel types and booking information
- **Real-time Responses**: Powered by Rasa NLU and Dialogue Management
- **Web Interface**: Modern, responsive chat interface

## 🏗️ Project Structure

```
sri_lanka_tourism_chatbot/
├── rasa_bot/                 # Rasa chatbot core
│   ├── data/                 # Training data (NLU, stories, rules)
│   ├── actions/              # Custom actions
│   └── models/               # Trained models
├── web_interface/            # Web application
│   ├── static/               # CSS, JS, images
│   └── templates/            # HTML templates
├── database/                 # Database schemas and migrations
├── data_collection/          # Training data collection scripts
└── docs/                     # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL or MySQL
- Node.js (for web interface)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sri_lanka_tourism_chatbot
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Rasa**
   ```bash
   cd rasa_bot
   rasa init
   ```

4. **Train the model**
   ```bash
   rasa train
   ```

5. **Start the services**
   ```bash
   # Terminal 1: Start Rasa server
   rasa run --enable-api --cors "*"
   
   # Terminal 2: Start web interface
   cd web_interface
   python app.py
   ```

## 📋 Supported Intents

- **Greetings**: `greet`, `goodbye`, `thank_you`
- **Tourist Information**: `ask_attraction`, `ask_food`, `ask_culture`
- **Transportation**: `ask_transport`, `ask_airport_transfer`
- **Accommodation**: `ask_hotel`, `ask_booking`
- **Emergency**: `ask_emergency`, `ask_embassy`
- **General**: `ask_weather`, `ask_currency`, `ask_visa`

## 🌐 Languages Supported

- **Sinhala** (සිංහල)
- **Tamil** (தமிழ்)
- **English**

## 🛠️ Technology Stack

- **Backend**: Python, Rasa, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: PostgreSQL/MySQL
- **NLP**: spaCy, NLTK
- **Language Detection**: langdetect

## 📊 Training Data

The chatbot is trained with:
- 20-50 examples per intent per language
- Entity annotations for locations, food items, transport modes
- Contextual dialogue flows
- Fallback responses for unknown queries

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/tourism_db
RASA_SERVER_URL=http://localhost:5005
LANGUAGE_DETECTION_ENABLED=true
```

### Database Setup

1. Create database:
   ```sql
   CREATE DATABASE tourism_db;
   ```

2. Run migrations:
   ```bash
   python database/migrate.py
   ```

## 🧪 Testing

```bash
# Test NLU model
rasa test nlu

# Test dialogue management
rasa test core

# Run interactive testing
rasa shell
```

## 📈 Performance Metrics

- **Intent Recognition Accuracy**: >90%
- **Entity Extraction F1-Score**: >85%
- **Response Time**: <2 seconds
- **Language Detection Accuracy**: >95%

## 🔮 Future Enhancements

- Voice-to-text integration
- Sentiment analysis
- Personalized recommendations
- Multimedia responses
- Live agent handoff
- Mobile app development

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact: tourism-chatbot@example.com

## 🙏 Acknowledgments

- Rasa team for the excellent framework
- Sri Lanka Tourism Development Authority for data
- Open source community for language processing tools