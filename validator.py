from marshmallow import Schema, fields

class CreateUserInputSchema(Schema):
   
    first_name = fields.Str(required=True, allow_none=False)
    last_name = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)
    user_name = fields.Str(required=True, allow_none=False)