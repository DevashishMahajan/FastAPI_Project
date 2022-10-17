from fastapi import FastAPI

app=FastAPI()

@app.get('/')
def index():
    return 'heyy'

@app.get('/name')
def name():
    return { 'data' : {'name' : 'Devashish'}}

@app.get('/email')
def email():
    return { 'data' : {'email' : 'devashishmahajan31@gmail.com'}}
  

@app.get('/github')
def email():
    return { 'data' : {'github' : 'https://github.com/DevashishMahajan'}}  


#Request Body
from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    title: str
    body: str
    published: Optional [bool]

@app.post('/blog')
def create_blog(blog:Blog):
    return {'data': f'Blog is created with title as {blog.title}'}