import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    DIGITALOCEAN_API_TOKEN = os.getenv('DIGITALOCEAN_API_TOKEN')
