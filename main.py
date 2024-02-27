import time

from fastapi import FastAPI, Depends, Form, Request
from sqlalchemy.orm import Session

from database import SessionLocal
from middleware import RateLimitingMiddleware, IPMiddleware
from schemes import Student, SubjectShow, SubjectBase, StudentBase
from services import _subject_create, _create_student, _subject_add_for_student, _delete_student, _delete_subject, \
    _update_subject, update_student_full_name, all_students_list

app = FastAPI()

app.add_middleware(RateLimitingMiddleware)
# app.add_middleware(IPMiddleware)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.middleware("http")
async def time_delta(request: Request, call_next):
    print(request.scope)
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    response.headers["X-Process-Time"] = f'Time: {end_time - start_time}'
    return response


@app.get('/')
def read_root():
    return {"message": "Hello World"}


@app.post('/student-create')
def create_student(student: Student, db: Session = Depends(get_db)):
    student = _create_student(student, db)
    return {'student': student}


@app.post('/subject-create', response_model=SubjectShow)
def create_subject(subject: SubjectBase, db: Session = Depends(get_db)):
    ans = _subject_create(subject, db)
    return ans


@app.post("/student/update", response_model=StudentBase)
def update_student(student_id: int,
                   first_name: str = Form(...),
                   last_name: str = Form(...),
                   age: int = Form(...),
                   db: Session = Depends(get_db),
                   ):
    return update_student_full_name(student_id, first_name, last_name, age, db)


@app.post("/subject/update/{subject_id}", response_model=SubjectBase)
def update_subject(subject_id: int, name: str,
                   db: Session = Depends(get_db)):
    return _update_subject(subject_id, name, db)


@app.post('/subject-add/student/{student_id}')
def subject_add_for_student(student_id: int,
                            subject: str,
                            db: Session = Depends(get_db)):
    return _subject_add_for_student(student_id, subject, db)


@app.post("/student/delete/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return _delete_student(student_id, db)


@app.post("/subject/delete/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    return _delete_subject(subject_id, db)


@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = all_students_list(db)
    return students

