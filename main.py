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
    