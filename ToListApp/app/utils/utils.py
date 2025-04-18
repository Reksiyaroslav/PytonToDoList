from app.db.engine import session,User
from sqlalchemy.orm import Session
import uuid
import random 
from sqlalchemy.sql import text

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_superuser(db: Session =next(get_db())):
    db.execute(text("DELETE FROM users WHERE username = 'admin'"))
    db.commit()
    superuser = User(id=uuid.uuid4(),username=f"admin{random.randint(1,1000)}",password = "admin")
    db.add(superuser)
    db.commit()
    db.refresh(superuser)
    return superuser