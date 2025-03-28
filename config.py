# config.py – Handles your database connection
# Import function to set up connection to DATABASE
from sqlalchemy import create_engine

# DATABASE_URI tells SQLAlchemy how to connect to your MySQL database.
# Note: The '@' in your password is URL-encoded as %40.
DATABASE_URI = "mysql+pymysql://root:Eunikblog%407@localhost/task_manager"

# Create the engine that will manage the connection to the database.
# The parameter echo=True makes SQLAlchemy print out the SQL it executes, which is useful for debugging.
engine = create_engine(DATABASE_URI, echo=True)
