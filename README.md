# Google Calendar MCP Server

This project integrates `Google Calendar v3 APIs` and creates an `MCP (Model Context Protocol) Server`. It allows MCP clients like **Claude Desktop** to interact with Google Calendar through natural language — powered by a lightweight server that bridges your calendar data with the LLM via MCP.

---

## 🧠 How It Works

This project consists of **2 servers**:

1. **Google OAuth Server**
   - Handles Google OAuth 2.0 authentication
   - Stores and manages access/refresh tokens for the user

2. **MCP Server**
   - Implements the [MCP (Model Context Protocol)](https://modelcontextprotocol.io/introduction) specification
   - Exposes a HTTP service that can be connected to **Claude Desktop** or other MCP-compatible clients
   - Uses stored tokens to interact with the [Google Calendar API v3](https://developers.google.com/calendar/api/v3/reference)

---

## 🚀 Getting Started

### 1. Set Up Google API Credentials

1. Visit the [Google Cloud Console](https://console.cloud.google.com/apis/dashboard)
2. Create a new project (or select an existing one)
3. Navigate to **APIs & Services** and enable the Google Calendar APIs for your project
4. Navigate to **Credentials** and create a new OAuth 2.0 Client
    - Choose *Desktop App* 
    - Create Branding for your application
    - Add your test email IDs in Audience to allow access
5. Download the credentials as `client_secret.json`
6. Place this file in the `Project root directory`

---

### 2. Install Python Dependencies

```bash
poetry install
```

### 3. Launch the OAuth FastAPI server

```bash
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

1. This should open the browser and prompt for OAuth verfication. (If not, you can manually head to http://0.0.0.0:8000/google_oauth/) 
2. After completing the OAuth succefully you should see the success screen.
3. Once done, a `session.json` file would get created with your access token in it.

![OAuth Success Page](/assets/oauth_sucess.png)

### 4. Run the MCP Server

```bash
poetry run python src/server.py
```

> The above command launches a streamable-http MCP server at localhost 8080

### 5. Add configuration for MCP client

- Connect your **Claude Desktop (MCP client)** with the server by adding the following configuration in */Users/{username}/Library/Application Support/Claude/claude_desktop_config.json*

```yaml
{
    "mcpServers": {
        "google-calendar-mcp": {
            "command": "npx",
            "args": [
                "mcp-remote",
                "http://localhost:8080/mcp"
            ]
        }
    }
}
```

### 6. Verify

- If connected successfully, you should be able to see the MCP server in settings.

![MCP client integrations](/assets/mcp_client_integration.png)

## 🧠 Demo

https://github.com/user-attachments/assets/27a8e5ee-8f2f-40c7-bdfc-1caa93767efb

## Project Structure

```
root
│   README.md
│   client_secret.json
│   session.json   
│   pyproject.toml
│
└───src
│   │   main.py - FastAPI Server for OAuth
│   │   settings.py - Basic settings for MCP server
│   │   server.py - MCP Server
│   │
│   └───api
│   │       oauth_callback.py - OAuth Server APIs
│   │
│   └───core
│   │       calendar_client.py - Google Calendar v3 integration
│   │       mcp_tools.py - MCP exposed tools
│   │       oauth_manager.py - Manages OAuth initiation
│   │       session_manager.py - Manages access/refresh token
│   │   
│   └───gcalendar_types - Google Calendar v3 API types
```
