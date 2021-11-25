from fastapi import FastAPI, File, UploadFile

from fastapi.responses import HTMLResponse

from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

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
# from app.server.models.ocr import (
#     ErrorResponseModel,
#     ResponseModel,
#     StudentSchema,
#     UpdateStudentModel,
# )

router = APIRouter()


@router.get("/")
async def ocr():
    # students = await retrieve_students()
    # if students:
    #     return ResponseModel(students, "Students data retrieved successfully")
    # return ResponseModel(students, "Empty list returned")
    return {"Hello": "World"}

@router.post("/get_file/")
async def get_file(file: UploadFile = File(...)):
    print(file.file) # temp file save
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
    os.remove(file_name)
    text = text[17:]
    return {"info": file.filename,
            "Text":text}


@router.get("/get_image/")
async def get_image():
    content = """
    <body>
   <form action="/ocr/get_file/" enctype="multipart/form-data" method="post">
    <input name="file" type="file">
    <input type="submit">
    </form>
    </body>
        """
    return HTMLResponse(content=content)



# @router.post("/files1/")
# async def create_files(files: List[bytes] = File(...)):
#     return {"file_sizes": [len(file) for file in files]}


# @router.post("/files/")

# async def create_files(files: List[bytes] = File(...)):

#     return {"file_sizes": [len(file) for file in files]}


# @router.post("/uploadfiles/")

# async def create_upload_files(files: List[UploadFile] = File(...)):

#     return {"filenames": [file.filename for file in files]}


# @router.get("/aa/")
# async def main():
#     content = """
#     <body>
#     <form action="/files/" enctype="multipart/form-data" method="post">
#     <input name="files" type="file" multiple>
#     <input type="submit">
#     </form>
#     <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
#     <input name="files" type="file" multiple>
#     <input type="submit">
#     </form>
#     </body>
#     """
#     return HTMLResponse(content=content)


# @router.post("/", response_description="Student data added into the database")
# async def add_student_data(student: StudentSchema = Body(...)):
#     student = jsonable_encoder(student)
#     new_student = await add_student(student)
#     return ResponseModel(new_student, "Student added successfully.")


# @router.get("/", response_description="Students retrieved")
# async def get_students():
#     students = await retrieve_students()
#     if students:
#         return ResponseModel(students, "Students data retrieved successfully")
#     return ResponseModel(students, "Empty list returned")


# @router.get("/{id}", response_description="Student data retrieved")
# async def get_student_data(id):
#     student = await retrieve_student(id)
#     if student:
#         return ResponseModel(student, "Student data retrieved successfully")
#     return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")


# @router.put("/{id}")
# async def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
#     req = {k: v for k, v in req.dict().items() if v is not None}
#     updated_student = await update_student(id, req)
#     if updated_student:
#         return ResponseModel(
#             "Student with ID: {} name update is successful".format(id),
#             "Student name updated successfully",
#         )
#     return ErrorResponseModel(
#         "An error occurred",
#         404,
#         "There was an error updating the student data.",
#     )


# @router.delete("/{id}", response_description="Student data deleted from the database")
# async def delete_student_data(id: str):
#     deleted_student = await delete_student(id)
#     if deleted_student:
#         return ResponseModel(
#             "Student with ID: {} removed".format(id), "Student deleted successfully"
#         )
#     return ErrorResponseModel(
#         "An error occurred", 404, "Student with id {0} doesn't exist".format(id)
#     )