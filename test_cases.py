import DbConfig
import validator


def test_email():
    response = validator.email_validation("abc@gmail.com")
    assert response == True



def Invalid_test_email():
    response = validator.email_validation("abc")
    assert response == False