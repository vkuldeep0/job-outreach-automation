import os

import psycopg
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app.models import Application
from app.schemas import ApplicationCreate, ApplicationUpdate


app = FastAPI(title="Job Outreach Automation")


Base.metadata.create_all(bind=engine)


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def get_db_connection():
	return psycopg.connect(
		host=os.getenv("DB_HOST"),
		port=os.getenv("DB_PORT"),
		user=os.getenv("DB_USER"),
		dbname=os.getenv("DB_NAME"),
		password=os.getenv("DB_PASSWORD"),
	)


@app.get("/")
def root():
	return {"message": "Job Outreach Automation API is running"}

@app.get("/health")
def health():
	return {"status": "healthy"}


@app.get("/db-health")
def db_health():
	with get_db_connection() as connection:
		with connection.cursor() as cursor:
			cursor.execute("SELECT 1")
			result = cursor.fetchone()

	return {"database": "connected", "result": result[0]}


@app.post("/applications", status_code=201)
def create_application(
	application: ApplicationCreate,
	db: Session = Depends(get_db),
):
	new_application = Application(
		company=application.company,
		job_title=application.job_title,
		job_url=application.job_url,
		application_date=application.application_date,
		status=application.status,
	)

	db.add(new_application)
	db.commit()
	db.refresh(new_application)

	return new_application

@app.get("/applications")
def get_applications(db: Session = Depends(get_db)):
	applications = db.query(Application).all()
	return applications



@app.put("/applications/{application_id}")
def update_application(
    application_id: int,
    application: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    existing_application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if existing_application is None:
        raise HTTPException(
		status_code=404,
		detail="Application not found"
	)

    existing_application.status = application.status

    db.commit()
    db.refresh(existing_application)

    return existing_application
