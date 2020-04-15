# robo-advisor/my_test.py

from app.robo_advisor import to_usd, num_there, get_response

def test_to_usd():
    result = to_usd(3.50)
    assert result == "$3.50"

def test_num_there():
    result = num_there("asdfs2")
    assert result == True

def test_get_response():
    result = get_response("tsla", "BCV3KUW4GBOD7DTL")
    assert type(result) is dict and 'Meta Data' in result and 'Time Series (Daily)' in result