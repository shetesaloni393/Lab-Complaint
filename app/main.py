from fastapi import FastAPI, Request, HTTPException, Depends, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

# 1. Initialize the app
app = FastAPI()

# Mount static files for images and JS
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure Jinja2 to look in the templates folder
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # This serves your landing page as the home page
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_root(request: Request):
    # This serves your landing page as the home page
    return templates.TemplateResponse("admindashboard.html", {"request": request})
