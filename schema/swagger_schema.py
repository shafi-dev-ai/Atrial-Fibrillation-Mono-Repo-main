from marshmallow import Schema, fields

# Swagger Response Schema in UI
class IsAliveResponseSchema(Schema):
    message = fields.Bool(default=True)

class AtrialFibrillationResponseSchema(Schema):
    afib_percent = fields.Str(default='')

class AtrialFibrillationRequestSchema(Schema):
    name = fields.String(default='')
    age = fields.Float(required=True)
    sex = fields.Float(required=True)
    height =  fields.Float(required=True)
    weight =   fields.Float(required=True)
    ritmi = fields.Float(required=True)
    I   =  fields.Float(required=True)
    II   =  fields.Float(required=True)
    III  =  fields.Float(required=True)
    aVF   =  fields.Float(required=True)
    aVR   =  fields.Float(required=True)
    aVL  =  fields.Float(required=True)
    V1   =  fields.Float(required=True)
    V2  =  fields.Float(required=True)
    V3  =  fields.Float(required=True)
    V4   =  fields.Float(required=True)
    V5  =  fields.Float(required=True)
    V6  =  fields.Float(required=True)



class AtrialFibrillationRequestPutSchema(Schema):
    name = fields.String(default='')
    age = fields.Float(required=True)
    sex = fields.Float(required=True)
    height =  fields.Float(required=True)
    weight =   fields.Float(required=True)
    ritmi = fields.Float(required=True)
    I   =  fields.Float(required=True)
    II   =  fields.Float(required=True)
    III  =  fields.Float(required=True)
    aVF   =  fields.Float(required=True)
    aVR   =  fields.Float(required=True)
    aVL  =  fields.Float(required=True)
    V1   =  fields.Float(required=True)
    V2  =  fields.Float(required=True)
    V3  =  fields.Float(required=True)
    V4   =  fields.Float(required=True)
    V5  =  fields.Float(required=True)
    V6  =  fields.Float(required=True)



class AtrialFibrillationResponsePutSchema(Schema):
    is_updated = fields.Bool(default=False)



class AtrialFibrillationDeleteRequestSchema(Schema):
    name = fields.String(default='')
class AtrialFibrillationDeleteResponseSchema(Schema):
    is_deleted = fields.Bool(default=False)
