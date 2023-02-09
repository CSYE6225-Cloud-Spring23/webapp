from marshmallow import Schema, fields
from marshmallow.validate import Range



class CreateUserInputSchema(Schema):
  
    first_name = fields.Str(required=True, allow_none=False)
    last_name = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)
    user_name = fields.Email(required=True, allow_none=False)