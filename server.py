#!/usr/bin/env python3

from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
import requests

class CustomHandler(SimpleHTTPRequestHandler):

    def version_string(self):
        return "Apache/2.4.18 (Ubuntu)"

    def end_headers(self):
        self.send_header("X-Powered-By", "PHP/5.6.40")
        self.send_header("Home-Sweet-Home", "j6nphmtl6mqayglcd5eir2jglayitbvqd3eprhiw2yyiv66ki2fonuid.onion")
        super().end_headers()

    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            self.path = "/index.html"
            return super().do_GET()
        elif self.path == "/audio/r.mp3":
            return super().do_GET()

        elif self.path  == "/robots.txt":

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            response = requests.get("https://zenquotes.io/api/random")
            if response.status_code == 200:
                data = response.json()
                quote = data[0]['q']
                author = data[0]['a']
                message = f"{quote} - {author}\n"
            else:
                message = "No robots available"
            self.wfile.write(message.encode("utf-8"))

        else:
            self.send_response(418)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"""

            """)

    def list_directory(self, path):
        # Disable directory listing entirely
        self.send_response(418)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"""
        """)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

httpd = ThreadedHTTPServer(("0.0.0.0", 8080), CustomHandler)
print("Serving on port 8080")
httpd.serve_forever()
