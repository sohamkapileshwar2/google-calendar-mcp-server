from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import webbrowser

from src.api.oauth_callback import router as oauth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 👇 Put your startup logic here
    print("🔐 Opening browser for OAuth login:")
    webbrowser.open("http://localhost:8000/google_oauth/")

    yield

    # 👇 (Optional) Put shutdown/cleanup logic here
    print("🛑 Server shutting down")

app = FastAPI(
    title="Google OAuth Server for MCP",
    description="Google OAuth Server",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(oauth_router)

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Google OAuth Server</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #f5f5f5;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to Google OAuth Proxy Server. Go to /google_oauth</h1>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return {"status": "OK"}

