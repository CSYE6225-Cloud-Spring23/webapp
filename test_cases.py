import DbConfig
import security


def test_email():
    response = security.email_validation("abc@gmail.com")
    assert response == True



def Invalid_test_email():
    response = security.email_validation("abc")
    assert response == False