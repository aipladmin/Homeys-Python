# application.py
from flask import Flask

from app import create_app

application = create_app()

if __name__ == "__main__":
	application.run(port='8000')