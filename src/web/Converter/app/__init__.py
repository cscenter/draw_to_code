import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'app/static'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mom`s spagetti'
app.config['CSRF_ENABLED'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes