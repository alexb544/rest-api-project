from fastapi import APIRouter, HTTPException
from models import Student
from database import get_connection

router = APIRouter()

@router.get("/students")
def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    results = cursor.execute("SELECT * FROM students").fetchall()
    conn.close()
    return {"students": results, "count": len(results)}


@router.get("/students/by-major", status_code=200) 
def get_students_by_major(major: str):
    conn = get_connection()
    cursor = conn.cursor()
    results = cursor.execute("""
        SELECT *
        FROM students
        WHERE major = ?""", (major,)
    ).fetchall()

    return {"students": results, "count": len(results), "major": major}


@router.get("/students/by-gpa", status_code=200) 
def get_students_by_gpa(min_gpa: float):
    conn = get_connection()
    cursor = conn.cursor()

    results = cursor.execute("""
        SELECT *
        FROM students
        WHERE gpa > ?""", (min_gpa,)
    ).fetchall()

    conn.close()
    return {"students": results, "count": len(results), "min_gpa": min_gpa}


@router.get("/students/{student_id}", status_code=200) 
def get_student(student_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    result = cursor.execute("""
        SELECT * 
        FROM students 
        WHERE id = ?""", (student_id,)
    ).fetchone()   
    conn.close()

    if result is None:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    else:
        return result

@router.post("/students", status_code=201)
def create_student(student: Student):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO students
        (id, name, email, major, gpa, enrollment_year) 
    VALUES 
        (?, ?, ?, ?, ?, ?)""", 
        (student.id, student.name, student.email, student.major, student.gpa, student.enrollment_year)
    )   
    conn.commit() 
    conn.close()


@router.put("/students/{student_id}", status_code=200) 
def update_student(student_id: int, student: Student):
    conn = get_connection()
    cursor = conn.cursor()

    result = cursor.execute("""
        UPDATE students 
        SET student = ?
        WHERE id = ?""", (student, student_id,)
    )
    conn.commit()
    

    conn.close()

    if result is None:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    else:
        return result


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