from fastapi import FastAPI, File, UploadFile, Request

from fastapi.responses import HTMLResponse

from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from typing import List
import os
import time
from app.server.models.app1 import Drive_OCR


# from app.server.database import (
#     add_student,
#     delete_student,
#     retrieve_student,
#     retrieve_students,
#     update_student,
# )
from app.server.models.ocr import (
    ErrorResponseModel,
    ResponseModel,
)

router = APIRouter()


@router.get("/")
async def ocr():
    return {"Data": "Hello World"}

@router.post("/getText/")
async def get_Text(file: UploadFile = File(...)):
    # print(file.file) # temp file save
    f = file.filename.replace(" ", "-")
    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H%M', t)
    fileName = timestamp + '_' + f
    file_name = fileName
    # file_name = "app/server/static/images/"+fileName
    with open(file_name,'wb+') as f:
        f.write(file.file.read())
        f.close()
    ob = Drive_OCR(file_name)
    text = ob.main()
    text = text[17:]
    os.remove(file_name)
    if len(text)<1:
        return ErrorResponseModel("An error occurred",
                404,
                "No text found in given Image", )
    return ResponseModel(text, "OCR Extract Data successfully.")


@router.post("/get_file/")
async def get_file(file: UploadFile = File(...)):
    # print(file.file) # temp file save
    f = file.filename.replace(" ", "-")
    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H%M', t)
    fileName = timestamp + '_' + f
    file_name = fileName
    # file_name = "app/server/static/images/"+fileName
    with open(file_name,'wb+') as f:
        f.write(file.file.read())
        f.close()
    ob = Drive_OCR(file_name)
    text = ob.main()
    text = text[17:]
    os.remove(file_name)
    if len(text)<1:
        return ErrorResponseModel("An error occurred",
                404,
                "No text found in given Image", )
    d = {"File Name": file_name, "Extracted Text":text}
    return ResponseModel(d, "OCR Extract Data successfully.")


@router.get("/get_image/",response_class=HTMLResponse )
async def get_image(request: Request, ):
    templates = Jinja2Templates(directory="app/server/templates")
    return templates.TemplateResponse("index1.html", {"request": request,})


#     content = """
#     <body>
#    <form action="/ocr/get_file/" enctype="multipart/form-data" method="post">
#     <input name="file" type="file">
#     <input type="submit">
#     </form>
#     </body>
#         """
#     return HTMLResponse(content=content)
