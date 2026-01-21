from fastapi import FastAPI
from backend.simulator import step

app = FastAPI(title="Ambulance Rerouting System")

@app.get("/ambulance")
def get_ambulance():
    return step()

