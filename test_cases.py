from validator import email_validation
#


def test_email():
    response = email_validation("abc@gmail.com")
    assert response == True



def Invalid_test_email():
    response = email_validation("abc")
    assert response == False