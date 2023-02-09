from marshmallow import Schema, fields
from marshmallow.validate import Range




class ProductSchema(Schema):

    name = fields.Str(required=True, allow_none=False)
    description = fields.Str(required=True, allow_none=False)
    sku = fields.Str(required=True, allow_none=False)
    manufacturer = fields.Str(required=True, allow_none=False)
    quantity = fields.Int(validate=Range(min=0, max=100), required=True, allow_none=False)
