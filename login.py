from fastapi import FastAPI, Form, Response, Cookie, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

# Simple mock database
USER_DB = {"admin": "secret123"}

# 1. The HTML Login Form
LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; margin-top: 100px; }
        form { border: 1px solid #ccc; padding: 20px; border-radius: 5px; width: 300px; }
        .input-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input { width: 100%; padding: 8px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }
        .error { color: red; margin-bottom: 15px; }
    </style>
</head>
<body>
    <form action="/login" method="post">
        <h2>Login</h2>
        {error_msg}
        <div class="input-group">
            <label>Username</label>
            <input type="text" name="username" required>
        </div>
        <div class="input-group">
            <label>Password</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit">Sign In</button>
    </form>
</body>
</html>
"""

# 2. Render Login Page (GET)
@app.get("/login", response_class=HTMLResponse)
async def get_login(error: bool = False):
    error_msg = '<div class="error">Invalid username or password</div>' if error else ''
    return LOGIN_HTML.format(error_msg=error_msg)

# 3. Handle Form Submission (POST)
@app.post("/login")
async def post_login(response: Response, username: str = Form(...), password: str = Form(...)):
    # Check credentials
    if username in USER_DB and USER_DB[username] == password:
        # Set a basic session cookie and redirect to dashboard
        response = HTMLResponse(content="<h2>Login successful! Welcome to your dashboard.</h2>", status_code=200)
        response.set_cookie(key="session_user", value=username)
        return response
    
    # If invalid, redirect back to login with error parameter
    return HTMLResponse(content=LOGIN_HTML.format(error_msg='<div class="error">Invalid credentials</div>'), status_code=401)

# 4. A Protected Route
@app.get("/dashboard")
async def dashboard(session_user: str | None = Cookie(None)):
    if not session_user:
        raise HTTPException(status_code=401, detail="Not logged in")
    return {"message": f"Hello {session_user}, welcome to your private dashboard!"}
