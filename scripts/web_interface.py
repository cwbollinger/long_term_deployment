#! /usr/bin/env python
import os
import BaseHTTPServer
import SimpleHTTPServer
server_address = ("", 8080)

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if self.path == '/log_data/':
            return os.environ['HOME'] + '/bags'
        else:
            return SimpleHTTPServer.SimpleHTTPRequestHandler.translate_path(self, path)

os.chdir(os.environ['HOME'] + '/ros2djs')
httpd = BaseHTTPServer.HTTPServer(server_address, MyRequestHandler)
httpd.serve_forever()
