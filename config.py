import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ORS_API_KEY")

TWIST_RADIUS_THRESHOLD = 250
WINDOW_DIST_M = 40  # meters
MIN_GROUP_LENGTH_M = 125    #meters
MIN_SCORE_THRESHOLD = 0.015   # temporary, we will tune
LOW_SCORE_THRESHOLD = 30
HIGH_SCORE_THRESHOLD = 200
RHYTHM_MULTIPLIER = 3.0


