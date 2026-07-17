import uvicorn
import os
import sys

# Ensure the root directory is in python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="127.0.0.1", port=5000, reload=True)