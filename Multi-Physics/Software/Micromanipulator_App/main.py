# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 16:41:34 2023

@author: sabge

main.py is the file that initialises the web app
if it is run in a terminal using python main.py
where the directory has to be set to the current one
"""

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=True, port=8080)
    # app.run(debug=True, threaded=True)
