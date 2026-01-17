from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import mysql.connector
import shutil
import os

# 1. Initialize the app
app = FastAPI()

# Ensure the upload directory exists on your HP Pavilion
UPLOAD_DIR = "app/static/uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Mount static files for images and JS
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure Jinja2 to look in the templates folder
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Renamed to read_dashboard to avoid duplicate function name error
@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("admindashboard.html", {"request": request})

@app.post("/submit-complaint")
async def handle_form(
    full_name: str = Form(...),
    roll_number: str = Form(...),
    issue_description: str = Form(...),
    file: UploadFile = File(None) # Optional image
):
    # --- 1. Handle File Upload Logic ---
    filename = None
    if file and file.filename:
        # Create a path to save the file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        # Save the file to the disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        filename = file.filename # Store just the name for the DB

    # --- 2. Database Logic ---
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="manthan04",
            database="lab_complaint_system"
        )
        cursor = db.cursor()
        
        # Updated SQL to include the image filename
        sql = "INSERT INTO lab_complaints (full_name, roll_number, issue_description, image_filename) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (full_name, roll_number, issue_description, filename))
        
        db.commit() # Crucial: This saves the data to MySQL
        
        cursor.close()
        db.close()
        
        return {"message": "Complaint and image submitted successfully!", "file_saved": filename}
    
    except mysql.connector.Error as err:
        return {"error": str(err)}