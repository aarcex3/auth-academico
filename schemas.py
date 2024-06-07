from pydantic import BaseModel


# Example student schema for requests and responses
class Student(BaseModel):
    student_code: str
    password: str
