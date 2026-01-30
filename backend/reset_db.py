from backend.app.database import engine, Base
from backend.app.models import models

def reset_database():
    print("Resetting database tables...")
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("Tables dropped.")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Tables created with new schema.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reset_database()
