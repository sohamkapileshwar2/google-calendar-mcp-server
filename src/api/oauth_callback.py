from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from src.core.oauth_manager import GoogleOAuthManager
from src.core.session_manager import SessionManager

router = APIRouter(prefix="/google_oauth", tags=["oauth"])

# Initialize the Google OAuth manager
scopes = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/calendar.settings.readonly'
]

google_oauth_manager = GoogleOAuthManager(
    client_secrets_file="client_secret.json",
    scopes=scopes,
    redirect_uri='http://localhost:8000/google_oauth/oauth2callback',
    secret_key="RANDOM_KEY_FOR_STATE_ENCRYPTION@42SAFAS14"
)

@router.get("/")
async def oauth2(request: Request):
    """Initiate Google OAuth2"""
    return google_oauth_manager.require_auth(request=request, state_data={})

@router.get("/oauth2callback")
async def oauth2callback(request: Request, state: str, code: str):
    """Handle OAuth2 callback."""
    credentials, state_data = google_oauth_manager.handle_oauth_callback(request, code, state)

    session_manager = SessionManager()
    session_id = session_manager._generate_session_id()
    session_manager.store_token(session_id, credentials)
    
    return RedirectResponse(url="/google_oauth/success")

@router.get("/success", response_class=HTMLResponse)
async def oauth2(request: Request):
    """OAuth Success"""

    return """
    <html>
        <head>
            <title>Success</title>
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
            <h1>Google OAuth2 Successful. Run the MCP Server.</h1>
        </body>
    </html>
    """