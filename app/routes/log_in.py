from fastapi import APIRouter


router = APIRouter()


# space holder login route for future integration
@router.get("/login")
def login():
    return {"message": "Coming soon!"}
