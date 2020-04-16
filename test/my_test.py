# robo-advisor/my_test.py

from app.robo_advisor import to_usd, num_there, get_response, transform_response, write_to_csv
import os, requests

def test_to_usd():
    result = to_usd(3.50)
    assert result == "$3.50"

def test_num_there():
    result = num_there("asdfs2")
    assert result == True

#test that get_response() returns a dictionary containing the following
def test_get_response():
    symbol = "tsla"
    API_KEY = "BCV3KUW4GBOD7DTL"
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    result = get_response(symbol, API_KEY, request_url)
    assert type(result) is dict and 'Meta Data' in result and 'Time Series (Daily)' in result

#test that transform_response returns a list and contains 'open' in the first element
def test_transform_response():
    symbol = "tsla"
    API_KEY = "BCV3KUW4GBOD7DTL"
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    parsed_response = get_response(symbol, API_KEY, request_url)
    result = transform_response(parsed_response)
    assert type(result) is list and 'open' in result[0]

def test_write_to_csv():
    symbol = "tsla"
    API_KEY = "BCV3KUW4GBOD7DTL"
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"

    rows = transform_response(get_response(symbol, API_KEY, request_url))

    csv_file_path = os.path.join("/Users/williameverett/Desktop/Georgetown-University/Spring-2020/OPIM-243/robo-advisor/app/data/prices.csv")

    result = write_to_csv(rows, csv_file_path)
    
    assert result == True