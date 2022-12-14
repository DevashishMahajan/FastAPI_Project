#pip install -r requirements.txt

from fastapi import FastAPI,Depends,status,Response,HTTPException
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

#make instance of FastAPI 
app = FastAPI()

models.Base.metadata.create_all(engine)

# Connect to database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Post a blog and add it into database
@app.post('/blog')
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

"""
@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog)
def show (id, response : Response, db: Session= Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id= id).first()

    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"Blog with the id {id} is not available")
            
    return blog
"""

# Get all blogs details
@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs= db.query(models.Blog).all()
    return blogs


# Add user and user detailes to database
#use password hashing
#from passlib. import CryptContext
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
@app.post('/user')
def create_user(request: schemas.User, db: Session=Depends(get_db)):
    hashedPassword=pwd_cxt.hash(request.password)

    new_user=models.User(name=request.name, email=request.email, password=hashedPassword)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user