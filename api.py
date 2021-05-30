from fastapi import FastAPI
import uvicorn
import main
app = FastAPI()


@app.get("/getInfoById")
async def getInfoById(num: int):
    return main.get_one_user_info(num)


@app.get('/performByExecute')
async def performByExecute():
    return main.execute()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# uvicorn api:app --reload --host 0.0.0.0
