import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import BillingCode, Client, Matter, DB_PATH

# --- DB & ORM setup ---
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)

# --- Zero-Shot Model Initialization ---
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
)

app = FastAPI(title="TimeTracker AI Service")

class PredictRequest(BaseModel):
    window_title: str

class PredictResponse(BaseModel):
    client_id: str | None
    matter_id: str | None
    code_id:   str
    score:     float

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    session = Session()

    # load codes
    codes = session.query(BillingCode).all()
    labels = [c.code for c in codes]
    code_map = {c.code: c.code_id for c in codes}

    # zero-shot
    res = classifier(req.window_title, labels)
    best_label = res["labels"][0]
    score      = res["scores"][0]
    code_id    = code_map[best_label]

    # default client/matter
    client = session.query(Client).first()
    matter = (
        session.query(Matter)
        .filter(Matter.client_id == client.client_id)
        .first()
    ) if client else None

    return PredictResponse(
        client_id= client.client_id if client else None,
        matter_id= matter.matter_id if matter else None,
        code_id=   code_id,
        score=     score
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
