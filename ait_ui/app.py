from flask import Flask, request, jsonify, send_from_directory, send_file, abort
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
import os

from . import socket_handler
from . import index_gen
flask_app = Flask(__name__)
socketio = SocketIO(flask_app)
socket_handler.socket = socketio
socket_handler.web_server = flask_app
socket_handler.web_request = request
CORS(flask_app)

ui_root = None
dir_routes = {}

@socketio.on('connect')
def handle_from_client(json):
    print('Socket connected')
    if socket_handler.clientHandler is not None:
        socket_handler.clientHandler('myapp', 'connect', 'connect')    


@socketio.on('from_client')
def handle_from_client(json):
    print('Received json: ' + str(json))
    if json['id'] == "myapp":
        if json['value'] == "init":
            socket_handler.send("myapp", ui_root.render(), "init-content")
    if socket_handler.clientHandler is not None:
        socket_handler.clientHandler(json['id'], json['value'], json['event_name'])    

@flask_app.route('/')
def home():
    return index_gen.generate_index()

@flask_app.route('/<path:path>')
def files(path):
    print("Path:",path)  # Ensure the path is correct
    return send_from_directory("static", path)

def add_static_route(route, osDirPath):
    print("Route Path:",osDirPath)  # Ensure the path is correct
    dir_routes[route] = osDirPath

@flask_app.route('/<route>/<path:file_path>')
def custom_files(route, file_path):
    if route not in dir_routes:
        abort(404)    
    return send_from_directory(dir_routes[route], file_path)

def run(ui = None, port=5000, debug=True):
    global ui_root
    if ui is not None:
        ui_root = ui        
    flask_app.run(host="0.0.0.0",port=port, debug=debug)

if __name__ == '__main__':
    run()