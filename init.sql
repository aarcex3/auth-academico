-- Create the students table
CREATE TABLE IF NOT EXISTS students (
    student_code TEXT PRIMARY KEY,
    password TEXT NOT NULL
);

-- Insert a student record
INSERT INTO students (student_code, password) VALUES 
('2.004.995', '$2b$12$sW2hA24/SxcaGS4kE5cGUee5CSDnhoNAJBi.JscYvo4RS0uSMGilC');
