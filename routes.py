from fastapi import APIRouter, HTTPException
from models import Student
from database import get_connection


router = APIRouter()

@router.get("/students", status_code=200)
def get_all_students():

    with get_connection() as conn:
        cursor = conn.cursor()
        results = cursor.execute("SELECT * FROM students").fetchall()

        return {"students": results, "count": len(results)}


@router.get("/students/by-major", status_code=200)
def get_students_by_major(major: str):

    if len(major) <= 0:
        raise HTTPException(status_code=400, detail=f"GPA must be between 0.0 and 4.0")

    with get_connection() as conn:
        cursor = conn.cursor()

        results = cursor.execute("""
            SELECT * FROM students
            WHERE major = ?""", (major,)).fetchall()

        return {"students": results, "count": len(results), "major": major}


@router.get("/students/by-gpa", status_code=200) 
def get_students_by_gpa(min_gpa: float):

    if min_gpa < 0.0 or min_gpa > 4.0:
        raise HTTPException(status_code=400, detail=f"GPA must be between 0.0 and 4.0")

    with get_connection() as conn:
        cursor = conn.cursor()

        results = cursor.execute("""
            SELECT * FROM students
            WHERE gpa > ?""", (min_gpa,)).fetchall()

        return {"students": results, "count": len(results), "min_gpa": min_gpa}


@router.get("/students/{student_id}", status_code=200) 
def get_student(student_id: int):

    with get_connection() as conn:
        cursor = conn.cursor()
        
        result = cursor.execute("""
            SELECT * FROM students 
            WHERE id = ?""", (student_id,)).fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
        
        return result


@router.post("/students", status_code=201)
def create_student(student: Student):

    with get_connection() as conn:
        cursor = conn.cursor()
        student_info = [student.name, student.email, student.major, student.gpa, student.enrollment_year]

        try:
            cursor.execute("""
                INSERT INTO students (name, email, major, gpa, enrollment_year)
                VALUES (?, ?, ?, ?, ?)
                """, student_info
            )
            id = cursor.lastrowid
            result = cursor.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()

            return result

        except:
            raise HTTPException(status_code=400, detail="Invalid email format")


@router.put("/students/{student_id}", status_code=200) 
def update_student(student_id: int, student: Student):

    with get_connection() as conn:
        cursor = conn.cursor()
        new_student_info = [student.id, student.name, student.email, student.major, student.gpa, student.enrollment_year, student_id]

        cursor.execute("""
            UPDATE students 
            SET (id, name, email, major, gpa, enrollment_year)
            = (?, ?, ?, ?, ?, ?)
            WHERE id = ? 
            """, (new_student_info)
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
        
        return cursor.execute("""
            SELECT *
            FROM students
            WHERE id = ?
            """, (student.id,)).fetchone()


@router.delete("/students/{student_id}", status_code=200) 
def delete_student(student_id: int):
    
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM students 
            WHERE id = ?
            """, (student_id,)
        )
        if cursor.rowcount <= 0:
            raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
        
        return {"message": "Student deleted successfully"}