from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

import uvicorn
import json
from src.util import read_json_list , write_json_list, delete_by_id
from src.calculate import calculate_statistic


app = FastAPI()


@app.get("/api/projects")
def projects():
    with open('data/projects.json',encoding='utf-8') as json_file:
        return json.load(json_file)

@app.get("/api/schedule")
def schedule():
    return read_json_list('./data/schedule.jsonl')

@app.get("/api/calculation")
def calculation():
    data = read_json_list('./data/schedule.jsonl')
    return calculate_statistic(data)

@app.put("/api/update")
async def update(request: Request):
    timeSpent = await request.json()
    
    data = read_json_list('./data/schedule.jsonl')
    delete_by_id(data,timeSpent['id'])
    data.append(timeSpent);
    write_json_list('data/schedule.jsonl',data)
    return timeSpent['id']


@app.get("/api/startstop")
async def set_startstop():
    with open('data/startstop.json',encoding='utf-8') as f:
        return json.load(f)

@app.put("/api/startstop")
async def set_startstop(request: Request):
    startstop = await request.json()
    with open("data/startstop.json", "w",encoding='utf-8') as f:
        json.dump(startstop, f)
    

@app.get("/api/delete/{id}")
def update(id: str):
    data = read_json_list('data/schedule.jsonl')
    delete_by_id(data,id)
    write_json_list('data/schedule.jsonl',data)
    


@app.get("/health")
def health():
    return {"Status": "UP"}

app.mount("/", StaticFiles(directory="htdocs",html = True))


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
