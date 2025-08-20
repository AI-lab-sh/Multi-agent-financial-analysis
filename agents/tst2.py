import os 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# project root (one level up from app/)
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../app",".env"))

print(PROJECT_ROOT)