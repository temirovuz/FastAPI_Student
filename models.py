from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
metadata = Base.metadata


# student_subjects = Table("student_course", Base.metadata,
#                        Column("student_id", ForeignKey("students.id"), primary_key=True),
#                        Column("subject_id", ForeignKey("subjects.id"), primary_key=True))
class StudentSubject(Base):
    __tablename__ = 'student_subjects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    subject = relationship("Subject", secondary="student_subjects", back_populates='student')


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    student = relationship("Student", secondary="student_subjects", back_populates='subject')