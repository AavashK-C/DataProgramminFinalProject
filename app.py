from flask import Flask, render_template,request
from pymongo import MongoClient
import pandas as pd
import json
import plotly
import plotly.express as px
import schedule
import subprocess
import time
from datetime import datetime
from flask import Flask, render_template, request
from forex_python.converter import CurrencyRates


app = Flask(__name__)

c = CurrencyRates()
def run_subprocess():
    
    subprocess.run(['python', 'Dependency/collect_data.py'])
    print("Subprocess executed at scheduled time.")

# Schedule the subprocess to run at 10 AM every day
schedule.every().day.at("10:00").do(run_subprocess)

# Function to continuously check the schedule and run the subprocess
def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)

# MongoDB connection
client = MongoClient("mongodb+srv://Aavash:Aavash123@cluster0.8ejpscx.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database("currency_data")
collection = db.currency_rates


@app.route('/')
def dashboard():
    cursor = collection.find()

    # Convert MongoDB cursor to a DataFrame
    df = pd.DataFrame(list(cursor))

    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Plotting trend lines for each currency pair using Plotly Express
    fig_line = px.line(df, x='Date', y='ExchangeRate', color='ToCurrency',
                  labels={'ExchangeRate': 'Exchange Rate', 'Date': 'Date'})

    # Convert the plotly figure to HTML
    plot_html = fig_line.to_html(full_html=False)

    # Create a box plot using Plotly Express
    fig = px.box(df, x='ToCurrency', y='ExchangeRate', color='ToCurrency',
             labels={'ExchangeRate': 'Exchange Rate', 'ToCurrency': 'To Currency'},
             title='Currency Exchange Rate Box Plot')


    # Convert the plotly figure to HTML
    plot_html_box = fig.to_html(full_html=False)

    # Create a scatter plot using Plotly Express
    fig_scatter = px.scatter(df, x='ToCurrency', y='ExchangeRate', color='FromCurrency',
                 labels={'ExchangeRate': 'Exchange Rate', 'ToCurrency': 'To Currency', 'FromCurrency': 'From Currency'},
                 title='Currency Exchange Rate Scatter Plot')
    
    plot_scatter = fig_scatter.to_html(full_html=False)

    return render_template('dashboard.html', plot_html=plot_html,plot_html_box= plot_html_box,plot_scatter=plot_scatter)

# Route to fetch currency rates and render a table in HTML
@app.route('/table')
def show_currency_rates():
    # Fetch data from MongoDB
    currency_data = collection.find()

    # Pass data to the HTML template
    return render_template('currency_table.html', currency_data=currency_data)

@app.route('/compare')
def compare_currency_rates():
    currency_data = list(collection.find())  # Convert MongoDB cursor to a list

    # Create a DataFrame from the MongoDB data
    df = pd.DataFrame(currency_data)

    # Create a bar chart using Plotly Express
    fig = px.bar(df, x='ToCurrency', y='ExchangeRate', color='FromCurrency', barmode='group',
                 labels={'ToCurrency': 'To Currency', 'ExchangeRate': 'Exchange Rate', 'FromCurrency': 'From Currency'},
                 title='Currency Exchange Rates')

    # Convert the Plotly figure to HTML and pass it to the template
    chart_div = fig.to_html(full_html=False)

    return render_template('compare_chart.html', chart_div=chart_div)

@app.route('/converter')
def converter():
    return render_template('calculate.html')

@app.route('/convert', methods=['POST'])
def convert():
    from_currency = request.form['from_currency']
    to_currency = request.form['to_currency']
    amount = float(request.form['amount'])

    # Perform currency conversion using forex_python
    converted_amount = c.convert(from_currency, to_currency, amount)

    result = f"{amount} {from_currency} is equal to {round(converted_amount)} of {to_currency}"
    
    return render_template('popup.html',result=result)


import threading
thread = threading.Thread(target=schedule_checker)
thread.start()


if __name__ == '__main__':
    app.run(debug=True)



