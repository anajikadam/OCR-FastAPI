from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import os

from app.server.routes.ocr import router as ocrRouter

app = FastAPI()

app.include_router(ocrRouter, tags=["ocr"], prefix="/ocr")

# app.mount("/app/server/static", StaticFiles(directory="static"), name="static")
statics = f"{os.getcwd()}/app/server/static/images"
@app.get("/download/{file_name}")
async def main(file_name: str):
    return FileResponse(os.path.join(statics, file_name))
    # return FileResponse(f"{os.getcwd()}/app/server/static/{file_name}")

@app.get("/", tags=["Root"], response_class=HTMLResponse )
async def read_root(request: Request, ):
    templates = Jinja2Templates(directory="app/server/templates")
    return templates.TemplateResponse("index.html", {"request": request,})
 