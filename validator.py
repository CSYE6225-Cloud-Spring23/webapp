from marshmallow import Schema, fields
import re

class CreateUserInputSchema(Schema):
   
    first_name = fields.Str(required=True, allow_none=False)
    last_name = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)
    user_name = fields.Str(required=True, allow_none=False)



    def email_validation(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if re.match(regex, email):
            return True
        return False