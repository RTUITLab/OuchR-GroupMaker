from fastapi import FastAPI, File, UploadFile
import uvicorn
app = FastAPI()

@app.get("/")
async def root():

    return "Test ter"

@app.post("/getInter")
async def getInter(str: str = str(...)):
    return str

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# uvicorn api:app --reload --host 0.0.0.0