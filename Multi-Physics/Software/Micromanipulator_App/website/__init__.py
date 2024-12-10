# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 14:12:16 2023

@author: sabge

file that makes the folder it is in a python directory,
meaning the folder and anything defined in this file can be imported
"""

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hsfcnksiee hdcbapownwal'

    from .view import view
    
    app.register_blueprint(view, url_prefix='/')
    
    return app