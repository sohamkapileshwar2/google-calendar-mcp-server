import json
import os
import secrets
import time
from typing import Dict, Any, Optional
from fastapi import Request, Response
from google.oauth2.credentials import Credentials

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.session_path = "session.json"
        self.cookie_name = "session_id"
        self.cookie_max_age = 30 * 24 * 60 * 60  # 30 days in seconds
        
        # Create session file if it doesn't exist
        if not os.path.exists(self.session_path):
            try:
                with open(self.session_path, 'w') as f:
                    json.dump({}, f, indent=2)
            except Exception as e:
                print(f"Error creating session file: {e}")
        else:
            # Load existing sessions if file exists
            try:
                with open(self.session_path, 'r') as f:
                    self.sessions = json.load(f)
            except json.JSONDecodeError:
                # If file is corrupted, start with empty sessions
                self.sessions = {}
            except Exception as e:
                print(f"Error loading session file: {e}")
                self.sessions = {}

    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        timestamp = int(time.time())
        random_bytes = secrets.token_hex(16)
        return f"{timestamp}-{random_bytes}"

    def get_session_id(self, request: Request) -> Optional[str]:
        """Get session ID from request cookies."""
        return request.cookies.get(self.cookie_name)

    def create_session(self, response: Response) -> str:
        """Create a new session and set the session cookie."""
        session_id = self._generate_session_id()
        response.set_cookie(
            key=self.cookie_name,
            value=session_id,
            max_age=self.cookie_max_age,
            httponly=True,
            secure=True,  # Only send cookie over HTTPS
            samesite='lax'  # Protect against CSRF
        )
        return session_id

    def store_token(self, session_id: str, credentials: Credentials) -> None:
        """
        Store Google credentials in both memory and session.json file.
        
        Args:
            session_id: Unique identifier for the session
            credentials: Google OAuth2 credentials object
        """
        
        # Convert credentials to dictionary
        credentials_dict = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        # Store in memory
        self.sessions = {session_id : credentials_dict}
        
        # Persist to file
        try:
            with open(self.session_path, 'w') as f:
                json.dump(self.sessions, f, indent=2)
        except Exception as e:
            print(f"Error saving session to file: {e}")
            # If file write fails, at least we have it in memory

    def get_credentials(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get stored credentials for a session ID."""
        return self.sessions.get(session_id)

    def delete_session(self, response: Response, session_id: str) -> None:
        """Delete a session and clear the session cookie."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            # Update the file
            try:
                with open(self.session_path, 'w') as f:
                    json.dump(self.sessions, f, indent=2)
            except Exception as e:
                print(f"Error updating session file: {e}")
        
        # Clear the cookie
        response.delete_cookie(self.cookie_name)
        