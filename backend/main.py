# main.py
# Backend for the Student Performance Prediction System
# Stage 1: Foundational setup, data models, and mock API endpoint.

# --- 1. Imports ---
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

# --- 2. FastAPI App Initialization ---
# This creates the main application instance.
# The title and version will be visible in the auto-generated API docs.
app = FastAPI(
    title="Student Performance Prediction API",
    description="API to predict student academic risk based on multi-factor analysis.",
    version="1.0.0"
)

# --- 3. Pydantic Data Models ---
# These models define the structure of the data we expect.
# FastAPI uses them to validate incoming and outgoing data.

class RiskLevel(str, Enum):
    """Enumeration for the possible risk levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Student(BaseModel):
    """Represents the raw input data for a single student."""
    student_id: str = Field(..., description="Anonymized unique identifier for the student.")
    cumulative_gpa: float = Field(..., ge=0.0, le=5.0, description="Student's cumulative GPA.")
    attendance_percentage: int = Field(..., ge=0, le=100, description="Student's class attendance percentage.")
    
    # Survey-based features (from our methodology)
    lab_access_rating: int = Field(..., ge=1, le=5, description="Student's rating of lab access (1-5).")
    weekly_coding_hours: int = Field(..., ge=0, description="Hours spent coding outside class per week.")
    commute_impact: int = Field(..., ge=1, le=5, description="Impact of commute on studies (1-5).")

class StudentRiskAssessment(BaseModel):
    """Represents the final output object for a student, including the prediction."""
    student_details: Student
    predicted_risk: RiskLevel
    justification: str = Field(..., description="A brief explanation for the assigned risk level.")


# --- 4. Assumed Data (In-Memory Database) ---
# In a real application, this data would come from a database.
# For Stage 1, we use a hardcoded list to simulate the data source.
# This allows us to develop and test the API endpoint without a database setup.

assumed_student_data: List[Student] = [
    Student(student_id="LASU_CS_001", cumulative_gpa=2.2, attendance_percentage=55, lab_access_rating=2, weekly_coding_hours=2, commute_impact=4),
    Student(student_id="LASU_CS_002", cumulative_gpa=4.1, attendance_percentage=95, lab_access_rating=5, weekly_coding_hours=15, commute_impact=1),
    Student(student_id="LASU_CS_003", cumulative_gpa=3.4, attendance_percentage=80, lab_access_rating=4, weekly_coding_hours=8, commute_impact=2),
    Student(student_id="LASU_CS_004", cumulative_gpa=2.8, attendance_percentage=92, lab_access_rating=3, weekly_coding_hours=5, commute_impact=3),
    Student(student_id="LASU_CS_005", cumulative_gpa=3.9, attendance_percentage=88, lab_access_rating=4, weekly_coding_hours=12, commute_impact=2),
    Student(student_id="LASU_CS_006", cumulative_gpa=1.9, attendance_percentage=45, lab_access_rating=1, weekly_coding_hours=1, commute_impact=5),
]

# --- 5. API Endpoints ---

@app.get("/", tags=["General"])
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Student Performance Prediction API. Visit /docs for documentation."}


@app.get("/api/v1/students/risk-assessment", 
         response_model=List[StudentRiskAssessment],
         tags=["Prediction"])
def get_all_student_risk_assessments():
    """
    Retrieves a list of all students with their predicted academic risk level.
    
    In Stage 1, the prediction is based on a simple heuristic.
    This will be replaced by an ML model in Stage 2.
    """
    assessments = []
    for student in assumed_student_data:
        risk_level = RiskLevel.LOW
        justification = "Student is performing well across key metrics."

        # Simple rule-based logic for prediction (placeholder)
        if student.cumulative_gpa < 2.5 or student.attendance_percentage < 60:
            risk_level = RiskLevel.HIGH
            justification = "Low GPA or poor attendance are strong indicators of high academic risk."
        elif student.cumulative_gpa < 3.5:
            risk_level = RiskLevel.MEDIUM
            justification = "Student's GPA is average. Monitor for potential decline."

        assessment = StudentRiskAssessment(
            student_details=student,
            predicted_risk=risk_level,
            justification=justification
        )
        assessments.append(assessment)
    
    return assessments

# To run this application:
# 1. Install the necessary libraries: pip install fastapi "uvicorn[standard]"
# 2. Save the code as main.py
# 3. In your terminal, run: uvicorn main:app --reload
# 4. Open your browser to http://127.0.0.1:8000/docs
