
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import render_template
from app.forms import CircleNumberForm
from app import app
import sys
# sys.path.insert(0, "..\\..\\..\\..\\")
sys.path.insert(0, "C:\\Users\\Matvey Bezlepkin\\Documents\\GitProjects\\draw_to_code\\src")
# print(sys.path)
from Detecting_all import main
# src/Detecting_all.py
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['bmp', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/uploaded/<filename>', methods= ['GET', 'POST'])
def uploaded_file(filename):
    app.config.from_object('config')
    form = CircleNumberForm()
    if form.validate_on_submit():
        circle_num = int(form.openid.data)
        return redirect(url_for('converting', filename=filename, circle_num=circle_num))
    return render_template("converter_page_1.html", image_name=filename, form=form)

@app.route('/converting/<filename>/<circle_num>', methods= ['GET', 'POST'])
def converting(filename, circle_num):
    tech_string = main(file_path="app/static/" + filename, count_circles=circle_num)
    return render_template('converter_page_2.html', image_name=filename, circle_num=circle_num, tech_string=tech_string)