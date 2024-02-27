from fastapi import HTTPException

from models import Subject, Student, StudentSubject


def _create_student(student, db):
    a = Student(first_name=student.first_name, last_name=student.last_name, age=student.age)
    db.add(a)
    db.commit()
    db.refresh(a)
    for id in student.subject:
        sub = db.query(Subject).filter(Subject.id == id).first()
        ss = StudentSubject(student_id=a.id, subject_id=sub.id)
        db.add(ss)
        db.commit()
        db.refresh(ss)
    return student


def _subject_create(subject, db):
    subject = Subject(name=subject.name)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


def update_student_full_name(student_id, lastname, firstname, age, db):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        student.last_name = lastname
        student.first_name = firstname
        student.age = age
        db.merge(student)
        db.commit()
        return student
    else:
        raise HTTPException(detail='Student not found', status_code=400)


def _delete_student(student_id, db):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
        return {'message': 'Student delete'}
    else:
        raise HTTPException(detail='Student not found', status_code=401)


def _get_student(student_id, db):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        return student
    else:
        raise HTTPException(detail='Student not found', status_code=4001)


def _get_subjects(db):
    subjects = db.query(Subject).filter(Subject.id).all()
    return subjects


def _delete_subject(subject_id, db):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject:
        db.delete(subject)
        db.commit()
        return {'message': 'delete subject'}
    else:
        raise HTTPException(detail='Subject not found', status_code=401)


def _update_subject(subject_id, name, db):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject:
        subject.name = name
        db.commit()
        return subject
    else:
        raise HTTPException(detail='subject not found', status_code=401)


def _subject_add_for_student(student_id, subject_id, db):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject:
        temp = StudentSubject()
        temp.student_id = student_id
        temp.subject_id = subject_id
        db.add(temp)
        db.commit()
        db.refresh(temp)
        return temp
    raise HTTPException(status_code=404, detail="Subject not found")


def all_students_list(db):
    students = db.query(Student).all()
    return students
