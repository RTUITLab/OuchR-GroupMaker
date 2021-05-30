from fastapi import FastAPI, File, UploadFile
import uvicorn
import main
app = FastAPI()


@app.get("/")
async def root():

    return main.execute()


@app.post("/getInter")
async def getInter(str: str = str(...)):
    return str


@app.get("/getInfoById")
async def getInfoById(num: int):
    return main.get_one_user_info(num)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# uvicorn api:app --reload --host 0.0.0.0
