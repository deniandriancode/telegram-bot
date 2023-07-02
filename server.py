import http.server
import socketserver
import threading
from bot import main as bot

def bot_thread():
    bot()

thread_child = threading.Thread(target=bot_thread)
thread_child.start()

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

thread_child.join()
