from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/convert")
async def convert_image(file: UploadFile = File(...)):
    pass
