# robo-advisor/my_test.py

from app.robo_advisor import to_usd, num_there

def test_to_usd():
    result = to_usd(3.50)
    assert result == "$3.50"

def test_num_there():
    result = num_there("asdfs2")
    assert result == True