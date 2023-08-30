"""Contains setting parameters for Neo4j."""
import os

from dotenv import load_dotenv

load_dotenv()

POPULAR_SRC = os.getenv("POPULAR_SRC")
POPULAR_DST = os.getenv("POPULAR_DST")
