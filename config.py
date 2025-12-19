import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATASET_PATH = "data/india_hospital_dataset.csv"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
