# Models.py – Defines your database table (tasks).py
# Import the required classes and functions from SQLAlchemy needed to define the table structure.
from sqlalchemy import Column, Integer, String, Text, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from config import engine

# Create a base class for your database models.
Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'  # This is the name of the table in the database.
    
    # Define the columns for the tasks table.
    id = Column(Integer, primary_key=True)                     # Unique ID for each task.
    user_name = Column(String(100), nullable=False)              # The name of the user who created the task.
    task_description = Column(Text, nullable=False)              # The description of the task.
    due_date = Column(Date, nullable=True)                       # The due date of the task (optional).
    status = Column(Enum('pending', 'completed'), default='pending')  # Task status: either pending or completed.

# Create the table in the database if it doesn't already exist.
Base.metadata.create_all(engine)
