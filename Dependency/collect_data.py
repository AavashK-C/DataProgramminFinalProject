from pymongo import MongoClient
from forex_python.converter import CurrencyRates
from datetime import datetime

# Connect to the MongoDB database
client = MongoClient("mongodb+srv://Aavash:Aavash123@cluster0.8ejpscx.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database("currency_data")
collection = db.currency_rates

# Create an instance of CurrencyRates
c = CurrencyRates()

# Define the currency pairs
currency_pairs = [("USD", "EUR"), ("USD", "GBP"), ("USD", "CAD")]  # Example currency pairs

# Fetch currency rates and save them in MongoDB with today's date
for pair in currency_pairs:
    rate = c.get_rate(pair[0], pair[1])
    today_date = datetime.now().date().isoformat()
    data = {
        "Date": today_date,
        "FromCurrency": pair[0],
        "ToCurrency": pair[1],
        "ExchangeRate": rate
    }
    collection.insert_one(data)
