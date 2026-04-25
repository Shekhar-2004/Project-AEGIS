from backend.db.session import engine
from backend.db.base import Base
from backend.db.incident import Incident

Base.metadata.create_all(bind=engine)

print("Tables created successfully")