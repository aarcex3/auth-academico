from sqlalchemy import Column, String  # type: ignore
from database import Base


# Example student model for the database
class Student(Base):
    __tablename__ = "students"
    student_code = Column(String, primary_key=True, index=True)
    password = Column(String)
