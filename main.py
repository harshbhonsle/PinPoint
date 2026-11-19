from fastapi import FastAPI

app = FastAPI(
    title="PinPoint – Pincode Lookup & Delivery Serviceability API",
    description="Auto fill city and state from Indian pincode during checkout"
)

@app.get("/")
def root():
    return{"message":"testing for lookup"}