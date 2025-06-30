from fastapi import FastAPI, HTTPException
import requests
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

BASE_URL = "https://data.etabus.gov.hk/v1/transport/kmb"

# Data models for response serialization
class EtaEntry(BaseModel):
    dest_en: str
    eta: Optional[str]

# API endpoint to fetch ETA info from KMB API and return simplified JSON
@app.get("/eta/{stop_id}/{route}/{service_type}", response_model=List[EtaEntry])
def get_eta(stop_id: str, route: str, service_type: str):
    url = f"{BASE_URL}/eta/{stop_id}/{route}/{service_type}"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Failed to fetch ETA from KMB API")
    data = resp.json().get("data", [])
    return [{"dest_en": entry["dest_en"], "eta": entry.get("eta")} for entry in data]

