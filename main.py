
from fastapi import FastAPI

from exceptions import (
    pincode_not_found_handler,
    invalid_pincode,
    PinCodeNotFoundError,
    InvalidPinCodeError
)

from models import (
    LocationResponse,
    BulkRequest,
    BulkResponse
)

from data import pincode_db


app = FastAPI(
    title="PinPoint – Pincode Lookup & Delivery Serviceability API",
    description="Auto fill city and state from Indian pincode during checkout"
)


# Register exception handlers
app.add_exception_handler(
    PinCodeNotFoundError,
    pincode_not_found_handler
)

app.add_exception_handler(
    InvalidPinCodeError,
    invalid_pincode
)


@app.get("/")
def root():
    return {"message": "Testing for lookup"}


# Bulk lookup API (keep before dynamic route)
@app.post("/pincode/bulk", response_model=BulkResponse)
def bulk_lookup(request: BulkRequest):

    results = []
    missing = []

    for code in request.pincodes:

        if len(code) != 6 or not code.isdigit():
            missing.append(code)

        elif code in pincode_db:
            results.append(pincode_db[code])

        else:
            missing.append(code)

    return BulkResponse(
        found=len(results),
        not_found=len(missing),
        results=results,
        missing=missing
    )


# Single pincode lookup API
@app.get("/pincode/{code}", response_model=LocationResponse)
def lookup_pincode(code: str):

    if len(code) != 6 or not code.isdigit():
        raise InvalidPinCodeError(
            code,
            "Must be exactly 6 digits"
        )

    if code not in pincode_db:
        raise PinCodeNotFoundError(code)

    return pincode_db[code]
