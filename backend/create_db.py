# create_db.py
from backend.database import engine, Base
from backend.models.models import User, Message

Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")