from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter(tags=["UI"])

@router.get("/dashboard")
def get_dashboard():
    static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    dashboard_file = os.path.join(static_path, "dashboard.html")
    return FileResponse(dashboard_file)
