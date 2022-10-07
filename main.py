from fastapi import FastAPI

app=FastAPI()

@app.get('/')
def index():
    return 'heyy'

@app.get('/name')
def name():
    return { 'data' : {'name' : 'Devashish'}}
    