from fastapi import APIRouter, HTTPException
from models import Student
from database import get_connection

router = APIRouter()

@router.get("/students")
def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    students = cursor.execute("SELECT * FROM students").fetchall()
    conn.close()
    return {"students": students, "count": len(students)}


@router.get("???") 
def get_students_by_major(major: str):
    conn = get_connection()
    cursor = conn.cursor()
    pass


@router.get("???") 
def get_students_by_gpa(min_gpa: float):
    conn = get_connection()
    cursor = conn.cursor()
    pass


@router.get("???") 
def get_student(student_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    pass


@router.post("/students", status_code=201)
def create_student(student: Student):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)", 
        (student.id, student.name, student.email, student.major, student.gpa, student.enrollment_year)
    )
    conn.commit()
    conn.close()

@router.put("???") 
def update_student(student_id: int, student: Student):
    conn = get_connection()
    cursor = conn.cursor()
    pass


@router.delete("/students/{student_id}") 
def delete_student(student_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        return {"message": "Student deleted successfully"}
    
    except:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    
    finally:
        conn.close()