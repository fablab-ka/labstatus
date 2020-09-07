from bottle import Bottle, route, run, template, static_file, request, error, hook, get, post, server_names
import os.path
import uuid
import bottle
import datetime
import logging
logging.basicConfig(level=logging.INFO, filename="log/log.txt", filemode="a+",
                    format='%(asctime)s - %(message)s')

@route('/static/<type>/<filename>')
def serve_css(type, filename):
    return static_file(filename, root=type+'/')

lab_open = False

def get_secret():
    file = "log/secret.txt"
    if not os.path.isfile(file):
        with open(file, "w") as f:
            f.write((str)(uuid.uuid4()))
            f.flush()
    with open(file, "r") as f:
        return f.readline()


@get('/set_status/<status>/<secret>')
def set_status(status, secret):
    if secret != get_secret():
        print("wrong secret")
        return "wrong secret"

    global lab_open
    if status == "open":
        print("lab opened")
        lab_open = True
    if status == "closed":
        print("lab closed")
        lab_open = False
    return "ok"

@get('/')
def main():
    lab_status = "geschlossen"
    if lab_open:
        lab_status = "offen"
    return template("main.tpl", lab_status=lab_status)

@get('/get_status')
def get_status():
    if lab_open:
        return "open"
    else:
        return "closed"

logging.info("Starting Service")
run(host='0.0.0.0', port=10127)
logging.info("Finishing Service")