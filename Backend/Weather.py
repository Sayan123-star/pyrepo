from flask import Flask, request, jsonify
import requests
import sqlite3
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Create SQLite database
conn = sqlite3.connect('weather.db')
c = conn.cursor()

# Create table to store weather data
c.execute('''CREATE TABLE IF NOT EXISTS weather (
             id INTEGER PRIMARY KEY,
             city TEXT,
             temperature REAL,
             humidity REAL,
             timestamp TIMESTAMP
             )''')
conn.commit()

# API key for weather API
API_KEY = 'a8019aa87cdd438aadefe6b899e34fde'

# Function to fetch weather data from API
def get_weather(city):
    url = f'https://api.weatherbit.io/v2.0/history/daily??city={city}&country=IN&start_date=2024-05-01&end_date=2024-05-02&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    print(data)
    return data['main']['temp']


# Endpoint to add a city
@app.route('/add_city', methods=['POST'])
def add_city():
    city = request.json['city']
    temperature, humidity = get_weather(city)
    timestamp = datetime.now()
    c.execute("INSERT INTO weather (city, temperature, humidity, timestamp) VALUES (?, ?, ?, ?)",
              (city, temperature, humidity, timestamp))
    conn.commit()
    return jsonify({'message': 'City added successfully'}), 200


# Endpoint to delete a city
@app.route('/delete_city/<int:city_id>', methods=['DELETE'])
def delete_city(city_id):
    c.execute("DELETE FROM weather WHERE id=?", (city_id,))
    conn.commit()
    return jsonify({'message': 'City deleted successfully'}), 200


# Endpoint to fetch all cities
@app.route('/cities', methods=['GET'])
def get_cities():
    c.execute("SELECT * FROM weather")
    cities = c.fetchall()
    cities_list = [{'id': city[0], 'name': city[1], 'temperature': city[2], 'humidity': city[3]} for city in cities]
    return jsonify(cities_list), 200


if __name__ == '__main__':
    app.run(debug=True)
