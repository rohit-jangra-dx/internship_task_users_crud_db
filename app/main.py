from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import UserAlreadyExistError, UserNotFoundError
from app.routes import router as users_router

app = FastAPI()

app.include_router(users_router)


# exceptions
@app.exception_handler(UserNotFoundError)
def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError,
):
    
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.exception_handler(UserAlreadyExistError)
def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistError,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )


