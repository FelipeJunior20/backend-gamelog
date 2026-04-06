from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import sqlite3
import hashlib
from http import cookies

sessions = {}

class LoginHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.show_login()
        elif self.path == "/dashboard":
            self.show_dashboard()
        elif self.path == "/logout":
            self.logout()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/login":
            self.handle_login()

    def show_login(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open("login.html", "r", encoding="utf-8") as file:
            html = file.read()

        self.wfile.write(html.encode())

    def handle_login(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode()
        data = urllib.parse.parse_qs(body)

        email = data.get("email", [""])[0]
        senha = data.get("senha", [""])[0]

        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=? AND senha=?", 
                       (email, senha_hash))
        user = cursor.fetchone()

        conn.close()

        if user:
            session_id = hashlib.sha256(email.encode()).hexdigest()
            sessions[session_id] = email

            self.send_response(302)
            self.send_header("Location", "/dashboard")
            self.send_header("Set-Cookie", f"session={session_id}")
            self.end_headers()
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Login invalido")

    def get_session(self):
        if "Cookie" in self.headers:
            cookie = cookies.SimpleCookie(self.headers["Cookie"])
            if "session" in cookie:
                session_id = cookie["session"].value
                return sessions.get(session_id)
        return None

    def show_dashboard(self):
        user = self.get_session()

        if user:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"<h1>Bem-vindo {user}</h1><a href='/logout'>Sair</a>".encode())
        else:
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

    def logout(self):
        self.send_response(302)
        self.send_header("Location", "/")
        self.send_header("Set-Cookie", "session=; Max-Age=0")
        self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), LoginHandler)
    print("Servidor rodando em http://localhost:8000")
    server.serve_forever()