from marshmallow import Schema, fields
from marshmallow.validate import Range
from marshmallow import validate 




class ProductSchema(Schema):

    not_null = validate.Length(min=1, error= "Field cannot be blank")
    name = fields.Str(required=True, allow_none=False, validate=not_null)
    description = fields.Str(required=True, allow_none=False, validate=not_null)
    sku = fields.Str(required=True, allow_none=False, validate=not_null)
    manufacturer = fields.Str(required=True, allow_none=False, validate=not_null)
    quantity = fields.Int(validate=Range(min=0, max=100), required=True, allow_none=False, strict=True)
    
