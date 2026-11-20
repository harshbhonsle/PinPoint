from pydantic import BaseModel, field_validator

class PinCodeRequest(BaseModel):
    pincode:str

    #pincode must be 6 digits
    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls,value):
        if len(value)!=6 or not value.isdigit():
            raise ValueError("Pincode must be exactly 6 digits")
        return value

class LocationResponse(BaseModel):
    pincode:str
    city:str
    state:str
    district:str

class BulkRequest(BaseModel):
    pincodes:list[str]

    @field_validator("pincodes")
    @classmethod
    def validate_pincodes(cls,values):
        if len(values)==0: 
            raise ValueError("Atleast one pincode should be provided")
        if len(values)>20:
            raise ValueError("Maximum 20 pincode values allowed per request")
        for code in values: 
            if len(code)!=6 or not code.isdigit():
                raise ValueError("Each Pincode value should be exactly 6 digit")
        return values

class BulkResponse(BaseModel):
    status:str="Success"
    found:int
    not_found:int
    results: list[LocationResponse]
    missing: list[str]
