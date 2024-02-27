from pydantic import BaseModel


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    age: int


class SubjectBase(BaseModel):
    name: str


class Student(StudentBase):
    subject: list[int] = []

    class Config:
        orm_mode = True


class SubjectShow(SubjectBase):
    id: int

    class Config:
        orm_mode = True
