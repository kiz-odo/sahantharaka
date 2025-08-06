# Sri Lanka Real-Time Tourism Analytics Dashboard

A comprehensive real-time analytics dashboard for Sri Lanka's tourism sector, providing insights into tourist arrivals, popular destinations, accommodation trends, social media sentiment, and revenue analysis.

## 🎯 Project Objective

To collect real-time or near real-time data about Sri Lanka's tourism sector, analyze it, and visualize it through an interactive dashboard. This aims to provide accurate and timely information to decision-makers in the tourism industry (hotel owners, travel agencies, government bodies).

## 🚀 Key Features

### 📊 Tourist Arrivals
- Daily/Weekly/Monthly tourist arrival statistics
- Classification by country of origin
- Arrival trends and patterns
- Real-time arrival tracking

### 🗺️ Popular Destinations
- Most frequently visited places
- Tourists' preferred activities
- Geographic distribution of visitors
- Seasonal destination preferences

### 🏨 Accommodation Insights
- Hotel occupancy rates
- Booking trends and patterns
- Accommodation type preferences
- Price analysis and trends

### 📱 Social Media Sentiment
- Real-time sentiment analysis from Twitter/X, Instagram
- Positive, negative, or neutral sentiment tracking
- Emerging trends and keywords
- Brand reputation monitoring

### 💰 Revenue Analysis
- Tourism sector revenue overview
- Revenue trends and forecasting
- Economic impact analysis
- Seasonal revenue patterns

### 🔮 Forecasting (Advanced Feature)
- Predictive analytics for tourist arrivals
- Booking trend forecasting
- Revenue prediction models
- Seasonal trend analysis

## 🛠️ Technology Stack

### Backend
- **Python 3.9+** - Core programming language
- **Flask** - Web framework for API
- **Pandas & NumPy** - Data manipulation and analysis
- **Scikit-learn** - Machine learning models
- **NLTK/TextBlob** - Natural Language Processing
- **SQLAlchemy** - Database ORM

### Frontend
- **Dash (Plotly)** - Interactive web dashboard
- **HTML/CSS/JavaScript** - Custom UI components
- **Chart.js** - Additional charting capabilities
- **Bootstrap** - Responsive design framework

### Database
- **PostgreSQL** - Primary relational database
- **MongoDB** - NoSQL for unstructured data
- **Redis** - Caching and real-time data

### Data Processing
- **Apache Kafka** - Real-time data streaming
- **Celery** - Background task processing
- **Redis** - Task queue and caching

### APIs & External Services
- **Twitter API** - Social media sentiment data
- **OpenWeatherMap API** - Weather data
- **Google Maps API** - Geographic data
- **Booking.com API** - Accommodation data (simulated)

## 📁 Project Structure

```
sri-lanka-tourism-dashboard/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── tourist_data.py
│   │   ├── accommodation.py
│   │   ├── sentiment.py
│   │   └── revenue.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_collector.py
│   │   ├── sentiment_analyzer.py
│   │   ├── forecast_service.py
│   │   └── api_service.py
│   ├── dashboard/
│   │   ├── __init__.py
│   │   ├── layouts/
│   │   ├── callbacks/
│   │   └── components/
│   └── utils/
│       ├── __init__.py
│       ├── database.py
│       └── helpers.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── historical/
├── notebooks/
│   ├── data_exploration.ipynb
│   ├── model_development.ipynb
│   └── dashboard_prototyping.ipynb
├── tests/
│   ├── test_data_collection.py
│   ├── test_models.py
│   └── test_dashboard.py
├── requirements.txt
├── config.py
├── run.py
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL
- Redis
- Node.js (for frontend assets)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sri-lanka-tourism-dashboard.git
cd sri-lanka-tourism-dashboard
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

6. **Run the application**
```bash
python run.py
```

The dashboard will be available at `http://localhost:8050`

## 📊 Data Sources

### Real Data Sources
- **Sri Lanka Tourism Development Authority (SLTDA)** - Official tourism statistics
- **Bandaranaike International Airport** - Arrival/departure data
- **Social Media APIs** - Twitter, Instagram sentiment data
- **Weather APIs** - OpenWeatherMap for climate data

### Simulated Data (for development)
- Tourist arrival patterns
- Hotel booking data
- Revenue statistics
- Social media sentiment

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/tourism_db
MONGODB_URL=mongodb://localhost:27017/tourism_data

# APIs
TWITTER_API_KEY=your_twitter_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Redis
REDIS_URL=redis://localhost:6379

# Flask
SECRET_KEY=your_secret_key
DEBUG=True
```

## 📈 Dashboard Features

### Real-Time Updates
- Live data refresh every 5 minutes
- WebSocket connections for instant updates
- Real-time alerts for anomalies

### Interactive Visualizations
- Interactive charts and graphs
- Geographic maps with tourist density
- Time-series analysis
- Comparative analytics

### Export Capabilities
- PDF reports generation
- Excel data export
- API endpoints for data access
- Automated report scheduling

## 🤖 Machine Learning Features

### Sentiment Analysis
- Real-time social media sentiment processing
- Multi-language support (English, Sinhala, Tamil)
- Trend detection and alerting

### Predictive Analytics
- Tourist arrival forecasting (ARIMA, Prophet)
- Revenue prediction models
- Seasonal trend analysis
- Anomaly detection

## 🔒 Security Features

- JWT authentication
- Role-based access control
- API rate limiting
- Data encryption
- Audit logging

## 📱 Mobile Responsiveness

- Responsive design for all devices
- Mobile-optimized dashboard
- Touch-friendly interface
- Offline capability for cached data

## 🚀 Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Cloud Deployment
- AWS EC2 with RDS
- Google Cloud Platform
- Heroku
- DigitalOcean

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Sri Lanka Tourism Development Authority
- Open source community
- Contributors and maintainers

## 📞 Support

For support and questions:
- Email: support@tourism-dashboard.lk
- Documentation: [Wiki](https://github.com/yourusername/sri-lanka-tourism-dashboard/wiki)
- Issues: [GitHub Issues](https://github.com/yourusername/sri-lanka-tourism-dashboard/issues)

---

**Built with ❤️ for Sri Lanka's Tourism Industry**