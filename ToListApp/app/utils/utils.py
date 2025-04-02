from app.db.engine import session,User
from sqlalchemy.orm import Session
import uuid
import random 

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_superuser(db: Session =next(get_db())):
    superuser = User(id=uuid.uuid4(),username=f"admin{random.randint(1,1000)}",password = "admin")
    db.add(superuser)
    db.commit()
    db.refresh(superuser)
    return superuser