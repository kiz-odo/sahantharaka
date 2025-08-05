#!/usr/bin/env python3
"""
Database migration script for Sri Lanka Tourism Chatbot
This script creates the database schema and populates it with initial data.
"""

import sqlite3
import os
import json
from datetime import datetime

class DatabaseMigrator:
    def __init__(self, db_path='tourism_chatbot.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to the database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"✅ Connected to database: {self.db_path}")
        except Exception as e:
            print(f"❌ Failed to connect to database: {e}")
            raise

    def disconnect(self):
        """Disconnect from the database"""
        if self.conn:
            self.conn.close()
            print("✅ Disconnected from database")

    def create_schema(self):
        """Create the database schema"""
        try:
            # Read schema file
            schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()

            # Execute schema
            self.cursor.executescript(schema_sql)
            self.conn.commit()
            print("✅ Database schema created successfully")
        except Exception as e:
            print(f"❌ Failed to create schema: {e}")
            raise

    def populate_attractions(self):
        """Populate attractions table with initial data"""
        attractions_data = [
            {
                'name': 'Sigiriya (Lion Rock)',
                'name_sinhala': 'සීගිරිය (සිංහ පාර්ව)',
                'name_tamil': 'சிகிரியா (சிங்க பாறை)',
                'location': 'Central Province, Sri Lanka',
                'description': 'Ancient palace and fortress complex built on a massive rock column. A UNESCO World Heritage site featuring stunning frescoes and the famous Lion\'s Paw entrance.',
                'description_sinhala': 'පුරාණ මාලිගාවක් සහ බලකොටු සංකීර්ණයක් විශාල ගල් තීරුවක් මත ඉදිකර ඇත. අලංකාර චිත්‍ර සහ ප්‍රසිද්ධ සිංහ පාද ඇතුළුව යුනෙස්කෝ ලෝක උරුම අඩවියකි.',
                'description_tamil': 'பெரிய பாறை நெடுவரிசையில் கட்டப்பட்ட பண்டைய அரண்மனை மற்றும் கோட்டை வளாகம். அழகான ஓவியங்கள் மற்றும் பிரபலமான சிங்க பாதம் நுழைவு வாயிலுடன் யுனெஸ்கோ உலக பாரம்பரிய தளம்.',
                'best_time_to_visit': 'December to April (dry season)',
                'entry_fee': 'Approximately $30 USD',
                'how_to_reach': 'Take a bus or train from Colombo to Dambulla, then a tuk-tuk to Sigiriya. About 4-5 hours from Colombo.',
                'latitude': 7.9570,
                'longitude': 80.7603,
                'category': 'Historical Site'
            },
            {
                'name': 'Nuwara Eliya',
                'name_sinhala': 'නුවරඑළිය',
                'name_tamil': 'நுவரெலியா',
                'location': 'Central Province, Sri Lanka',
                'description': 'Known as \'Little England\', this hill country town features tea plantations, cool climate, and colonial architecture.',
                'description_sinhala': '\'කුඩා එංගලන්තය\' ලෙස හඳුන්වන මෙම කඳුකර නගරය තේ වතු, සිසිල් දේශගුණය සහ යටත්විජිත ගෘහ නිර්මාණ ශිල්පය ඇතුළත් වේ.',
                'description_tamil': '\'சிறிய இங்கிலாந்து\' என்று அழைக்கப்படும் இந்த மலை நாட்டு நகரம் தேயிலை தோட்டங்கள், குளிர்ந்த காலநிலை மற்றும் காலனி கட்டிடக்கலை ஆகியவற்றைக் கொண்டுள்ளது.',
                'best_time_to_visit': 'March to May (spring season)',
                'entry_fee': 'Free (attractions may have separate fees)',
                'how_to_reach': 'Take the scenic train from Colombo or Kandy. About 6-7 hours from Colombo by train.',
                'latitude': 6.9497,
                'longitude': 80.7891,
                'category': 'Hill Country'
            },
            {
                'name': 'Galle Fort',
                'name_sinhala': 'ගාල්ල බලකොටුව',
                'name_tamil': 'காலி கோட்டை',
                'location': 'Southern Province, Sri Lanka',
                'description': 'A UNESCO World Heritage site featuring a 16th-century Portuguese fort with Dutch colonial architecture, boutique hotels, and charming streets.',
                'description_sinhala': '16 වන සියවසේ පෘතුගීසි බලකොටුව, ලන්දේසි යටත්විජිත ගෘහ නිර්මාණ ශිල්පය, බූටික් හෝටල් සහ ආකර්ෂණීය වීථි සහිත යුනෙස්කෝ ලෝක උරුම අඩවියකි.',
                'description_tamil': '16 ஆம் நூற்றாண்டின் போர்த்துகீசிய கோட்டை, டச்சு காலனி கட்டிடக்கலை, புட்டிக் ஹோட்டல்கள் மற்றும் கவர்ச்சிகரமான தெருக்களுடன் யுனெஸ்கோ உலக பாரம்பரிய தளம்.',
                'best_time_to_visit': 'November to April',
                'entry_fee': 'Free to enter the fort',
                'how_to_reach': 'Take a train or bus from Colombo. About 2-3 hours from Colombo.',
                'latitude': 6.0535,
                'longitude': 80.2210,
                'category': 'Historical Site'
            },
            {
                'name': 'Yala National Park',
                'name_sinhala': 'යාල ජාතික වනෝද්‍යානය',
                'name_tamil': 'யால தேசிய பூங்கா',
                'location': 'Southern Province, Sri Lanka',
                'description': 'Famous for leopard sightings and diverse wildlife including elephants, crocodiles, and hundreds of bird species.',
                'description_sinhala': 'චිත්තාවරයන් දැකීම සහ අලි, මොස්සන් සහ සිය ගණනක් පක්ෂි විශේෂ ඇතුළු විවිධ වනජීවීන් සඳහා ප්‍රසිද්ධයි.',
                'description_tamil': 'சிறுத்தை பார்வைகள் மற்றும் யானைகள், முதலைகள் மற்றும் நூற்றுக்கணக்கான பறவை இனங்கள் உட்பட பல்வேறு வனவிலங்குகளுக்கு பிரபலமானது.',
                'best_time_to_visit': 'February to July (best for wildlife viewing)',
                'entry_fee': 'Approximately $15 USD for foreigners',
                'how_to_reach': 'Take a bus to Tissamaharama, then arrange a safari jeep. About 6 hours from Colombo.',
                'latitude': 6.3667,
                'longitude': 81.5167,
                'category': 'Wildlife'
            }
        ]

        for attraction in attractions_data:
            self.cursor.execute('''
                INSERT INTO attractions (name, name_sinhala, name_tamil, location, description, 
                                       description_sinhala, description_tamil, best_time_to_visit, 
                                       entry_fee, how_to_reach, latitude, longitude, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                attraction['name'], attraction['name_sinhala'], attraction['name_tamil'],
                attraction['location'], attraction['description'], attraction['description_sinhala'],
                attraction['description_tamil'], attraction['best_time_to_visit'],
                attraction['entry_fee'], attraction['how_to_reach'], attraction['latitude'],
                attraction['longitude'], attraction['category']
            ))

        self.conn.commit()
        print(f"✅ Populated attractions table with {len(attractions_data)} records")

    def populate_food_items(self):
        """Populate food items table with initial data"""
        food_data = [
            {
                'name': 'Rice and Curry',
                'name_sinhala': 'බත් සහ කරවල',
                'name_tamil': 'சாதம் மற்றும் கறி',
                'description': 'The national dish of Sri Lanka, featuring steamed rice served with various curries including vegetables, fish, chicken, or beef.',
                'description_sinhala': 'ශ්‍රී ලංකාවේ ජාතික ආහාරය, විවිධ කරවල සමඟ සේවනය කරන උම්බල බත්.',
                'description_tamil': 'இலங்கையின் தேசிய உணவு, பல்வேறு கறிகளுடன் சேவை செய்யப்படும் வேகவைத்த சாதம்.',
                'ingredients': 'Rice, coconut milk, spices, vegetables, meat or fish',
                'ingredients_sinhala': 'බත්, පොල් කිරි, මසාල, එළවළු, මස් හෝ මාළු',
                'ingredients_tamil': 'சாதம், தேங்காய் பால், மசாலாப் பொருட்கள், காய்கறிகள், இறைச்சி அல்லது மீன்',
                'where_to_find': 'Available in most restaurants and hotels throughout Sri Lanka',
                'price_range': '$2-8 USD',
                'category': 'Main Course',
                'is_vegetarian': False,
                'is_spicy': True
            },
            {
                'name': 'Kottu Roti',
                'name_sinhala': 'කොත්තු රොටි',
                'name_tamil': 'கோத்து ரொட்டி',
                'description': 'A popular street food made by shredding roti bread and mixing it with vegetables, eggs, and meat on a hot griddle.',
                'description_sinhala': 'රොටි බඩ ඉරා එළවළු, බිත්තර සහ මස් සමඟ මිශ්‍ර කර උණුසුම් ග්‍රිඩ්ල් මත සාදන ජනප්‍රිය වීථි ආහාරයකි.',
                'description_tamil': 'ரொட்டியை நறுக்கி காய்கறிகள், முட்டைகள் மற்றும் இறைச்சியுடன் சூடான கிரிடிலில் கலக்கி தயாரிக்கப்படும் பிரபலமான தெரு உணவு.',
                'ingredients': 'Roti bread, vegetables, eggs, chicken or beef, spices',
                'ingredients_sinhala': 'රොටි බඩ, එළවළු, බිත්තර, කුකුල් මස් හෝ ගව මස්, මසාල',
                'ingredients_tamil': 'ரொட்டி, காய்கறிகள், முட்டைகள், கோழி அல்லது மாட்டிறைச்சி, மசாலாப் பொருட்கள்',
                'where_to_find': 'Street food stalls, especially in Colombo and tourist areas',
                'price_range': '$1-3 USD',
                'category': 'Street Food',
                'is_vegetarian': False,
                'is_spicy': True
            },
            {
                'name': 'Hoppers (Appa)',
                'name_sinhala': 'ආප්ප',
                'name_tamil': 'அப்பம்',
                'description': 'Crispy, bowl-shaped pancakes made from rice flour and coconut milk, often served with curry or sambol.',
                'description_sinhala': 'බත් පිටි සහ පොල් කිරි වලින් සාදන ලද පිරිසිදු, භාජන හැඩැති ආප්ප, බොහෝ විට කරවල හෝ සම්බෝල සමඟ සේවනය කරයි.',
                'description_tamil': 'அரிசி மாவு மற்றும் தேங்காய் பாலில் இருந்து தயாரிக்கப்படும் மிருதுவான, கிண்ண வடிவ பன்கேக்குகள், பெரும்பாலும் கறி அல்லது சம்போல் உடன் சேவை செய்யப்படுகின்றன.',
                'ingredients': 'Rice flour, coconut milk, yeast, salt',
                'ingredients_sinhala': 'බත් පිටි, පොල් කිරි, යීස්ට්, ලුණු',
                'ingredients_tamil': 'அரிசி மாவு, தேங்காய் பால், ஈஸ்ட், உப்பு',
                'where_to_find': 'Breakfast at hotels, street food stalls, and traditional restaurants',
                'price_range': '$0.50-2 USD',
                'category': 'Breakfast',
                'is_vegetarian': True,
                'is_spicy': False
            }
        ]

        for food in food_data:
            self.cursor.execute('''
                INSERT INTO food_items (name, name_sinhala, name_tamil, description, description_sinhala,
                                      description_tamil, ingredients, ingredients_sinhala, ingredients_tamil,
                                      where_to_find, price_range, category, is_vegetarian, is_spicy)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                food['name'], food['name_sinhala'], food['name_tamil'], food['description'],
                food['description_sinhala'], food['description_tamil'], food['ingredients'],
                food['ingredients_sinhala'], food['ingredients_tamil'], food['where_to_find'],
                food['price_range'], food['category'], food['is_vegetarian'], food['is_spicy']
            ))

        self.conn.commit()
        print(f"✅ Populated food_items table with {len(food_data)} records")

    def populate_transport_options(self):
        """Populate transport options table with initial data"""
        transport_data = [
            {
                'name': 'Trains',
                'name_sinhala': 'දුම්රිය',
                'name_tamil': 'ரயில்கள்',
                'description': 'Sri Lanka Railways operates an extensive network connecting major cities and towns.',
                'description_sinhala': 'ශ්‍රී ලංකා දුම්රිය සේවය ප්‍රධාන නගර සහ නගර සම්බන්ධ කරන විශාල ජාලයක් ක්‍රියාත්මක කරයි.',
                'description_tamil': 'இலங்கை இரயில்வே முக்கிய நகரங்கள் மற்றும் நகரங்களை இணைக்கும் விரிவான நெட்வொர்க்கை இயக்குகிறது.',
                'cost': 'Very affordable, 2nd class tickets from $1-5 USD',
                'availability': 'Regular services between major cities, book in advance for popular routes',
                'tips': 'Book 1st or 2nd class for comfort, 3rd class can be very crowded',
                'tips_sinhala': 'සුවපහසුව සඳහා 1 වන හෝ 2 වන පන්තිය වෙන් කරන්න, 3 වන පන්තිය ඉතා ගැඹුරු විය හැකිය',
                'tips_tamil': 'சுகாதாரத்திற்காக 1வது அல்லது 2வது வகுப்பு புக்கிங் செய்யுங்கள், 3வது வகுப்பு மிகவும் நெரிசலாக இருக்கலாம்',
                'category': 'Public Transport'
            },
            {
                'name': 'Buses',
                'name_sinhala': 'බස්',
                'name_tamil': 'பேருந்துகள்',
                'description': 'Extensive bus network covering almost every part of the country.',
                'description_sinhala': 'රටේ සෑම කොටසක්ම ආවරණය කරන විශාල බස් ජාලයක්.',
                'description_tamil': 'நாட்டின் கிட்டத்தட்ட ஒவ்வொரு பகுதியையும் உள்ளடக்கிய விரிவான பேருந்து நெட்வொர்க்கு.',
                'cost': 'Very cheap, typically $0.50-2 USD for most routes',
                'availability': 'Frequent services, no advance booking needed',
                'tips': 'Can be crowded and hot, bring water and patience',
                'tips_sinhala': 'ගැඹුරු සහ උණුසුම් විය හැකිය, ජලය සහ ඉවසීම ගෙන එන්න',
                'tips_tamil': 'நெரிசலாகவும் சூடாகவும் இருக்கலாம், தண்ணீர் மற்றும் பொறுமையைக் கொண்டு வாருங்கள்',
                'category': 'Public Transport'
            },
            {
                'name': 'Taxis and Tuk-tuks',
                'name_sinhala': 'ටැක්සි සහ ටුක්-ටුක්',
                'name_tamil': 'டாக்ஸிகள் மற்றும் டுக்கு-டுக்கு',
                'description': 'Convenient for short distances and airport transfers.',
                'description_sinhala': 'කෙටි දුර සහ ගුවන්තොටුපළ මාරුවීම් සඳහා පහසුකම්.',
                'description_tamil': 'குறுகிய தூரங்கள் மற்றும் விமான நிலைய பரிமாற்றங்களுக்கு வசதியானது.',
                'cost': 'Tuk-tuks: $1-5 USD, Taxis: $5-20 USD depending on distance',
                'availability': 'Readily available in cities and tourist areas',
                'tips': 'Always negotiate the fare before getting in, tuk-tuks are cheaper than taxis',
                'tips_sinhala': 'ඇතුළු වීමට පෙර සෑම විටම ගාස්තු සාකච්ඡා කරන්න, ටුක්-ටුක් ටැක්සි වලට වඩා ලාභදායී වේ',
                'tips_tamil': 'உள்ளே செல்வதற்கு முன் எப்போதும் கட்டணத்தை பேரம் பேசுங்கள், டுக்கு-டுக்கு டாக்ஸிகளை விட மலிவானவை',
                'category': 'Private Transport'
            }
        ]

        for transport in transport_data:
            self.cursor.execute('''
                INSERT INTO transport_options (name, name_sinhala, name_tamil, description, description_sinhala,
                                             description_tamil, cost, availability, tips, tips_sinhala, tips_tamil, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                transport['name'], transport['name_sinhala'], transport['name_tamil'], transport['description'],
                transport['description_sinhala'], transport['description_tamil'], transport['cost'],
                transport['availability'], transport['tips'], transport['tips_sinhala'], transport['tips_tamil'],
                transport['category']
            ))

        self.conn.commit()
        print(f"✅ Populated transport_options table with {len(transport_data)} records")

    def populate_emergency_contacts(self):
        """Populate emergency contacts table with initial data"""
        emergency_data = [
            {
                'service_name': 'General Emergency',
                'service_name_sinhala': 'සාමාන්‍ය හදිසි අවස්ථා',
                'service_name_tamil': 'பொதுவான அவசர நிலைமை',
                'contact_number': '119',
                'description': 'General emergency services for police, fire, and medical emergencies',
                'description_sinhala': 'පොලිසිය, ගිනි නිවන සහ වෛද්‍ය හදිසි අවස්ථා සඳහා සාමාන්‍ය හදිසි සේවා',
                'description_tamil': 'காவல்துறை, தீயணைப்பு மற்றும் மருத்துவ அவசர நிலைமைகளுக்கான பொதுவான அவசர சேவைகள்',
                'category': 'Emergency'
            },
            {
                'service_name': 'Ambulance',
                'service_name_sinhala': 'ගිලන් රථ',
                'service_name_tamil': 'ஆம்புலன்ஸ்',
                'contact_number': '110',
                'description': 'Emergency ambulance services',
                'description_sinhala': 'හදිසි ගිලන් රථ සේවා',
                'description_tamil': 'அவசர ஆம்புலன்ஸ் சேவைகள்',
                'category': 'Medical'
            },
            {
                'service_name': 'Fire Services',
                'service_name_sinhala': 'ගිනි නිවන සේවා',
                'service_name_tamil': 'தீயணைப்பு சேவைகள்',
                'contact_number': '111',
                'description': 'Fire and rescue services',
                'description_sinhala': 'ගිනි නිවන සහ ගලවා ගැනීමේ සේවා',
                'description_tamil': 'தீயணைப்பு மற்றும் மீட்பு சேவைகள்',
                'category': 'Fire'
            },
            {
                'service_name': 'Tourist Police',
                'service_name_sinhala': 'සංචාරක පොලිසිය',
                'service_name_tamil': 'சுற்றுலா காவல்துறை',
                'contact_number': '011-242-1052',
                'description': 'Specialized police service for tourists, English speaking officers available',
                'description_sinhala': 'සංචාරකයින් සඳහා විශේෂ පොලිස් සේවා, ඉංග්‍රීසි කතා කරන නිලධාරීන් ලබා ගත හැකිය',
                'description_tamil': 'சுற்றுலா பயணிகளுக்கான சிறப்பு காவல்துறை சேவை, ஆங்கிலம் பேசும் அதிகாரிகள் கிடைக்கின்றனர்',
                'category': 'Tourist Support'
            }
        ]

        for emergency in emergency_data:
            self.cursor.execute('''
                INSERT INTO emergency_contacts (service_name, service_name_sinhala, service_name_tamil,
                                              contact_number, description, description_sinhala, description_tamil, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                emergency['service_name'], emergency['service_name_sinhala'], emergency['service_name_tamil'],
                emergency['contact_number'], emergency['description'], emergency['description_sinhala'],
                emergency['description_tamil'], emergency['category']
            ))

        self.conn.commit()
        print(f"✅ Populated emergency_contacts table with {len(emergency_data)} records")

    def run_migration(self):
        """Run the complete migration process"""
        print("🚀 Starting database migration...")
        
        try:
            self.connect()
            self.create_schema()
            self.populate_attractions()
            self.populate_food_items()
            self.populate_transport_options()
            self.populate_emergency_contacts()
            
            print("✅ Database migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            raise
        finally:
            self.disconnect()

def main():
    """Main function to run the migration"""
    migrator = DatabaseMigrator()
    migrator.run_migration()

if __name__ == "__main__":
    main()