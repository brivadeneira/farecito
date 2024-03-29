"""Contains setting parameters for Pipelines."""
import os

from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_DB = os.getenv("NEO4J_DB")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
AURA_INSTANCENAME = os.getenv("AURA_INSTANCENAME")

REGION = os.getenv("REGION")

TRIP_MIN_DISCOUNT = os.getenv("TRIP_MIN_DISCOUNT")
SENT_TRIPS_FILE = os.getenv("SENT_TRIPS_FILE")
SCRAP_DAYS = os.getenv("SCRAP_DAYS")
