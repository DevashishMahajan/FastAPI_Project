from fastapi import FastAPI,Depends
from . import schemas, models
from . database import engine, sessionLocal
from sqlalchemy.orm import Session

#make instance of FastAPI 
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


@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog)
def show (id, response : Response, db: Session= Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id= id).first()

    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"Blog with the id {id} is not available")
            
    return blog


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