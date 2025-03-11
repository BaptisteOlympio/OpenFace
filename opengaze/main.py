from fastapi import FastAPI
import subprocess
import pandas as pd
import time

app = FastAPI()

CSV_FILE = "/tmp/openface/output.csv"
PROCESS = None  # To track the FeatureExtraction process

def start_feature_extraction():
    """Start OpenFace gaze tracking."""
    global PROCESS
    if PROCESS is None:
        PROCESS = subprocess.Popen(
            ["FeatureExtraction", "-gaze", "-device", "0", "-of", CSV_FILE],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

@app.get("/start-gazing")
async def start_gazing():
    """Start the gaze tracking process."""
    start_feature_extraction()
    return {"message": "Gaze tracking started"}

@app.get("/get-gaze")
async def get_gaze():
    """Retrieve the latest gaze data from the CSV."""
    try:
        # Read the CSV and get the last row
        df = pd.read_csv(CSV_FILE)
        if not df.empty:
            # Extract the last row and return it as JSON
            last_row = df.iloc[-1].to_json()
            # return {"gaze_data": last_row}
            # TODO un problème si on a plusieurs personnes dans le champs de vision
            return last_row
        else:
            return {"error": "CSV is empty or gaze data is not yet available."}
    except Exception as e:
        return {"error": f"Error reading CSV: {e}"}

