from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()


# Middleware untuk menambahkan header `X-Client-IP` ke request
class AddClientIPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Mendapatkan IP address dari request
        client_ip = request.client.host

        # Menyimpan IP ke `request.state` untuk dapat diakses di dalam endpoint atau dependency
        request.state.client_ip = client_ip

        # Memproses request dan mendapatkan response dari endpoint yang dituju
        response = await call_next(request)

        # Menambahkan IP address ke header response
        response.headers["X-Client-IP"] = client_ip

        return response


app.add_middleware(AddClientIPMiddleware)
