from fastapi import FastAPI,Depends
from . import schemas, models
from . database import engine, sessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog')
def create(request: schemas.blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog



# Add user and user detailes to database
#use password hashing
from passlib.CryptContext(schemas=["bcrypt"], deprecated="auto")

@app.post('/user')
def create_user(request: schemas.User, db: Session=Depends(get_db)):
    hashedPassword=pwd_cxt.hash(request.password)

    new_user=models.User(name=request.name, email=request.email, password=hashedPassword)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user