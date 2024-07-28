"""
Auth module
"""

from fastapi import APIRouter
from starlette.templating import Jinja2Templates

router = APIRouter(tags=["auth"])

templates = Jinja2Templates(directory="templates")

