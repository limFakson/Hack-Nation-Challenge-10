from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from helpers.token_generator import decode_access_token


# --- Middleware for Token Validation ---


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        unprotected_paths = ["/login", "/signup", "/docs", "/openapi.json", "details"]
        if any(request.url.path.endswith(path) for path in unprotected_paths):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Not authenticated: Missing or invalid Authorization header"
                },
            )

        token = auth_header.split(" ")[1]

        try:
            payload = decode_access_token(token)
            request.state.user = payload
            
            return await call_next(request)
        except HTTPException as e:
            return JSONResponse(status_code=e, content={"detail": e.detail})

