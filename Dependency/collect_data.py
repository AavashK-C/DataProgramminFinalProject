from pymongo import MongoClient
from forex_python.converter import CurrencyRates
from datetime import datetime, timedelta

# Connect to the MongoDB database
client = MongoClient("mongodb+srv://Aavash:Aavash123@cluster0.8ejpscx.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database("currency_data")
collection = db.currency_rates

# Create an instance of CurrencyRates
c = CurrencyRates()

# Define the currency pairs
currency_pairs = [("USD", "EUR"), ("USD", "GBP"), ("USD", "CAD")]  # Example currency pairs

# Fetch currency rates for the previous 30 days and save them in MongoDB
for i in range(30):
    target_date = datetime.now().date() - timedelta(days=i + 1)  # Get the date for the previous day
    for pair in currency_pairs:
        rate = c.get_rate(pair[0], pair[1], target_date)
        data = {
            "Date": target_date.isoformat(),
            "FromCurrency": pair[0],
            "ToCurrency": pair[1],
            "ExchangeRate": rate
        }
        collection.insert_one(data)