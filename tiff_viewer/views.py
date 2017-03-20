"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from tiff_viewer import app

import os, os.path, tempfile
from PIL import Image
from shutil import copyfile


os.chdir('E:\\IMAGES\\')
images_path = os.getcwd()
temp_files_path = 'C:\\tiff_viewer\\tiff_viewer\\static\\temp\\'
files = []

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'lite1.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/s/<string:filename>', methods=['GET', 'POST'])
def open_file(filename):
    """Renders tif file"""
    if request.method == 'GET':

        if filename[-4:] == '.tif' or filename[-4:] == '.tiff':
            _file = filename
        else:
            _file = filename + '.tif'

        if os.path.isfile(_file):
            im = Image.open(_file)
            im._open
            files = []
            new_files = []
            for i in range(im.n_frames):
                try:
                    im = Image.open(_file)
                    im.seek(i)
                    temp_h = tempfile.mkstemp()[1]
                    im.save(temp_h + _file.split('\\')[-1][:-4] + '_' + str(i), 'jpeg', quality=300)                 
                    copyfile(temp_h + _file.split('\\')[-1][:-4] + '_' + str(i), temp_files_path + _file.split('\\')[-1][:-4] + '_' + str(i) + '.jpg')
                    files.append(temp_files_path + _file.split('\\')[-1][:-4] + '_' + str(i) + '.jpg')
                except EOFError:
                    break

        for f in files:
            new_files.append(f.replace('\\', '/'))

        return render_template(
                'scan.html', 
                title='TIFF Viewer',
                year=datetime.now().year,
                pdf = new_files
        )
    else:
        return render_template(
                'scan.html',
                title='TIFF Viewer',
                year=datetime.now().year,
                message=''
        )


@app.route('/lite1')
def lite():
    return render_template('lite1.html')


@app.route('/lite2', methods = ['POST', 'GET'])
def lite2():
    if request.method == 'POST':
        if request.form['tag'][-4:] == '.tif' or request.form['tag'][-5:] == '.tiff':
            _file = request.form['tag']
        else:
            _file = request.form['tag'] + '.tif'

        if os.path.isfile(_file):
            im = Image.open(_file)
            im._open
            files = []
            new_files = []
            for i in range(im.n_frames):
                try:
                    im = Image.open(_file)
                    im.seek(i)
                    temp_h = tempfile.mkstemp()[1]
                    im.save(temp_h + _file.split('\\')[-1][:-4] + '_' + str(i), 'jpeg', quality=300)                 
                    copyfile(temp_h + _file.split('\\')[-1][:-4] + '_' + str(i), temp_files_path + _file.split('\\')[-1][:-4] + '_' + str(i) + '.jpg')
                    files.append(temp_files_path + _file.split('\\')[-1][:-4] + '_' + str(i) + '.jpg')
                except EOFError:
                    break

        for f in files:
            new_files.append(f.replace('\\', '/'))

        return render_template(
                'lite2.html', 
                title='TIFF Viewer',
                year=datetime.now().year,
                pdf = new_files
        )
    else:
        return render_template(
                'lite1.html',
                title='TIFF Viewer',
                year=datetime.now().year,
                message='No image found.'
        )

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST', 'GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
