# robo-advisor/my_test.py

from app.robo_advisor import to_usd, num_there, get_response, transform_response

def test_to_usd():
    result = to_usd(3.50)
    assert result == "$3.50"

def test_num_there():
    result = num_there("asdfs2")
    assert result == True

#test that get_response() returns a dictionary containing the following
def test_get_response():
    result = get_response("tsla", "BCV3KUW4GBOD7DTL")
    assert type(result) is dict and 'Meta Data' in result and 'Time Series (Daily)' in result

#test that transform_response returns a list and contains 'open' in the first element
def test_transform_response():
    parsed_response = get_response("tsla", "BCV3KUW4GBOD7DTL")
    result = transform_response(parsed_response)
    assert type(result) is list and 'open' in result[0]