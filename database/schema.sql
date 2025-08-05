-- Sri Lanka Tourism Chatbot Database Schema
-- This file contains the complete database schema for the tourism information system

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Create tables for tourism information

-- Attractions table
CREATE TABLE IF NOT EXISTS attractions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    name_sinhala VARCHAR(255),
    name_tamil VARCHAR(255),
    location VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    description_sinhala TEXT,
    description_tamil TEXT,
    best_time_to_visit VARCHAR(255),
    entry_fee VARCHAR(100),
    how_to_reach TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    category VARCHAR(100),
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Food items table
CREATE TABLE IF NOT EXISTS food_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    name_sinhala VARCHAR(255),
    name_tamil VARCHAR(255),
    description TEXT NOT NULL,
    description_sinhala TEXT,
    description_tamil TEXT,
    ingredients TEXT,
    ingredients_sinhala TEXT,
    ingredients_tamil TEXT,
    where_to_find TEXT,
    price_range VARCHAR(100),
    category VARCHAR(100),
    is_vegetarian BOOLEAN DEFAULT FALSE,
    is_spicy BOOLEAN DEFAULT FALSE,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transport options table
CREATE TABLE IF NOT EXISTS transport_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    name_sinhala VARCHAR(255),
    name_tamil VARCHAR(255),
    description TEXT NOT NULL,
    description_sinhala TEXT,
    description_tamil TEXT,
    cost VARCHAR(255),
    availability TEXT,
    tips TEXT,
    tips_sinhala TEXT,
    tips_tamil TEXT,
    category VARCHAR(100),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Hotels table
CREATE TABLE IF NOT EXISTS hotels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    name_sinhala VARCHAR(255),
    name_tamil VARCHAR(255),
    location VARCHAR(255) NOT NULL,
    description TEXT,
    description_sinhala TEXT,
    description_tamil TEXT,
    category VARCHAR(100),
    price_range VARCHAR(100),
    amenities TEXT,
    contact_number VARCHAR(50),
    website VARCHAR(500),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    rating DECIMAL(2, 1),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Emergency contacts table
CREATE TABLE IF NOT EXISTS emergency_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name VARCHAR(255) NOT NULL,
    service_name_sinhala VARCHAR(255),
    service_name_tamil VARCHAR(255),
    contact_number VARCHAR(50) NOT NULL,
    description TEXT,
    description_sinhala TEXT,
    description_tamil TEXT,
    category VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cities table
CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    name_sinhala VARCHAR(255),
    name_tamil VARCHAR(255),
    province VARCHAR(255),
    description TEXT,
    description_sinhala TEXT,
    description_tamil TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    is_popular BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cultural information table
CREATE TABLE IF NOT EXISTS cultural_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    title_sinhala VARCHAR(255),
    title_tamil VARCHAR(255),
    content TEXT NOT NULL,
    content_sinhala TEXT,
    content_tamil TEXT,
    category VARCHAR(100),
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Weather information table
CREATE TABLE IF NOT EXISTS weather_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_id INTEGER,
    month VARCHAR(20),
    temperature_min DECIMAL(4, 1),
    temperature_max DECIMAL(4, 1),
    rainfall_mm DECIMAL(6, 2),
    description TEXT,
    description_sinhala TEXT,
    description_tamil TEXT,
    is_best_time BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id)
);

-- Chat sessions table (for analytics)
CREATE TABLE IF NOT EXISTS chat_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(255) NOT NULL,
    user_language VARCHAR(10),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    message_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat messages table (for analytics)
CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(255) NOT NULL,
    message_type VARCHAR(20) NOT NULL, -- 'user' or 'bot'
    content TEXT NOT NULL,
    intent VARCHAR(100),
    confidence DECIMAL(3, 2),
    entities TEXT, -- JSON string
    response_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_attractions_name ON attractions(name);
CREATE INDEX IF NOT EXISTS idx_attractions_category ON attractions(category);
CREATE INDEX IF NOT EXISTS idx_food_items_name ON food_items(name);
CREATE INDEX IF NOT EXISTS idx_food_items_category ON food_items(category);
CREATE INDEX IF NOT EXISTS idx_transport_options_name ON transport_options(name);
CREATE INDEX IF NOT EXISTS idx_hotels_location ON hotels(location);
CREATE INDEX IF NOT EXISTS idx_hotels_category ON hotels(category);
CREATE INDEX IF NOT EXISTS idx_emergency_contacts_category ON emergency_contacts(category);
CREATE INDEX IF NOT EXISTS idx_cities_name ON cities(name);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_session_id ON chat_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);

-- Create triggers for updated_at timestamps
CREATE TRIGGER IF NOT EXISTS update_attractions_timestamp 
    AFTER UPDATE ON attractions
    BEGIN
        UPDATE attractions SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_food_items_timestamp 
    AFTER UPDATE ON food_items
    BEGIN
        UPDATE food_items SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_transport_options_timestamp 
    AFTER UPDATE ON transport_options
    BEGIN
        UPDATE transport_options SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_hotels_timestamp 
    AFTER UPDATE ON hotels
    BEGIN
        UPDATE hotels SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_emergency_contacts_timestamp 
    AFTER UPDATE ON emergency_contacts
    BEGIN
        UPDATE emergency_contacts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_cities_timestamp 
    AFTER UPDATE ON cities
    BEGIN
        UPDATE cities SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_cultural_info_timestamp 
    AFTER UPDATE ON cultural_info
    BEGIN
        UPDATE cultural_info SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_weather_info_timestamp 
    AFTER UPDATE ON weather_info
    BEGIN
        UPDATE weather_info SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;