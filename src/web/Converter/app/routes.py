
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import render_template
from app.forms import CircleNumberForm, EditTextForm
from pdf2image import convert_from_path, convert_from_bytes
import numpy as np
from PIL import Image
from app import app
import sys
# sys.path.insert(0, "..\\..\\..\\..\\")
sys.path.insert(0, "C:\\Users\\Matvey Bezlepkin\\Documents\\GitProjects\\draw_to_code\\src")
# print(sys.path)
from Detecting_all import main
from helper import to_pdf
# src/Detecting_all.py
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['bmp', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

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
    return render_template("converter_page_1.html", image_name_1=filename, form=form)

@app.route('/converting/<filename>/<circle_num>', methods= ['GET', 'POST'])
def converting(filename, circle_num):
    if request.method == 'GET':
        tech_string = main(file_path="app/static/" + filename, count_circles=circle_num)
        images = convert_from_path('output.pdf')
        with open('params.txt', 'r') as fin:
            counter = int(fin.read())
        image_2_name = 'output_pic' + str(counter) + '.png'
        counter += 1
        with open('params.txt', 'w') as fout:
            fout.write(str(counter))
        images[0].save(os.path.join(app.config['UPLOAD_FOLDER'], image_2_name))
        return render_template('converter_page_2.html', image_name_1=filename, circle_num=circle_num, str=tech_string, image_name_2=image_2_name)
    elif request.method == 'POST':
        form = request.form
        new_tech_string=form['tex_code']
        to_pdf('output', new_tech_string, '')
        images=convert_from_path('output.pdf')
        with open('params.txt', 'r') as fin:
            counter = int(fin.read())
        image_2_name = 'output_pic' + str(counter) + '.png'
        counter += 1
        with open('params.txt', 'w') as fout:
            fout.write(str(counter))
        images[0].save(os.path.join(app.config['UPLOAD_FOLDER'], image_2_name))
        return render_template('converter_page_2.html', image_name_1=filename, circle_num=circle_num, str=new_tech_string,image_name_2=image_2_name)