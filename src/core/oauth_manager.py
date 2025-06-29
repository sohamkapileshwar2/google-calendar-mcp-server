from typing import Dict, Any
import google.oauth2.credentials
import google_auth_oauthlib.flow
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from itsdangerous import URLSafeSerializer

class GoogleOAuthManager:
    def __init__(self, client_secrets_file: str, scopes: list[str], redirect_uri: str, secret_key: str):
        self.client_secrets_file = client_secrets_file
        self.scopes = scopes
        self.redirect_uri = redirect_uri
        self.flow = None
        self.state_serializer = URLSafeSerializer(secret_key)
        self._initialize_flow()
        
    def _initialize_flow(self):
        """Initialize the OAuth flow with client secrets and scopes."""
        self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.client_secrets_file,
            scopes=self.scopes
        )
        self.flow.redirect_uri = self.redirect_uri

    def get_authorization_url(self, state_data: Dict[str, Any]) -> tuple[str, str]:
        """Generate authorization URL for OAuth flow with encrypted state."""
        # Encrypt the state data
        encrypted_state = self.state_serializer.dumps(state_data)
        
        return self.flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent',
            state=encrypted_state
        )

    def handle_oauth_callback(self, request: Request, code: str, state: str) -> tuple[google.oauth2.credentials.Credentials, Dict[str, Any]]:
        """Handle OAuth callback and return credentials and state data."""
        # Decrypt the state
        try:
            state_data = self.state_serializer.loads(state)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid state parameter")
            
        self.flow.fetch_token(code=code)
        credentials = self.flow.credentials

        return credentials, state_data


    def require_auth(self, request: Request, state_data: Dict[str, Any]) -> RedirectResponse:
        """Require authentication, redirecting to OAuth if needed."""

        auth_url, _ = self.get_authorization_url(state_data)
        return RedirectResponse(url=auth_url)