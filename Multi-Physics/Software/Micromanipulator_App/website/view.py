# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 14:12:16 2023

@author: sabge
"""

# import relavant packages
import numpy as np
import serial
from serial.tools import list_ports
import os
import time
import cv2
import threading
from flask import Blueprint, url_for, render_template, jsonify, request, Response

import datetime as dt
today = dt.date.today()

view = Blueprint('view', __name__)


@view.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(view.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

basedir = os.path.abspath(os.path.dirname(__file__))

#-----------------------------------------------------------------------------------------------------------------
# gloabal variables
#-----------------------------------------------------------------------------------------------------------------
global path
global folder

# Camera Video
global duration
global fps_video

# Camera Settings
global current_w
global max_w
global min_w
global current_h
global max_h
global min_h
global current_offx
global max_ox
global min_ox
global current_offy
global max_oy
global min_oy
global current_g
global max_g
global min_g
global current_b
global max_b
global min_b
global current_gamma
global max_gamma
global min_gamma
global current_exp
global max_exposure
global min_exposure

# Manual Stepper Motor mode
global rms
global micro
global hold

# dict for connecting
global SN_dict
global ser_dict
global ax_dict

# Axis movement increments
global x_increment
global y_increment
global z_increment
global rot1_increment
global rot2_increment
global stab_increment

# Axis auto (True) or manual (False)
global auto_x
global auto_y
global auto_stab

# Probes Electrode (Astrapi) and Laser
global astrapi_total_time_on
global astrapi_time_on
global astrapi_time_off


#-----------------------------------------------------------------------------------------------------------------
# define path - change according to needs
#-----------------------------------------------------------------------------------------------------------------
path = '/home/sabrina/Documents/Code/Camera'
path = '/media/sabrina/Sabrina/MimosaPudica'

experiment='/MimosaPudica/'



#-----------------------------------------------------------------------------------------------------------------
# define initial variables - change according to needs
#-----------------------------------------------------------------------------------------------------------------
# Manual Stepper Motor mode
rms = 0
micro = 0
hold = 0

# Camera Video
duration = 7200
fps_video = 1

# Axis Connections (Microcontroller serial number)
SN_dict = {'E66138935F908929':'x',
           'E66138935F68C428':'y',
           'E6612483CB40902D':'z',
           'E66138935F9E5E29':'rot',
           'E6612483CB53862A':'rot2',
           'E66138935F409C28':'r',
           'BBF9D3EE5153433347202020FF082A1D': 'laser',
           '1BD0DF345153433347202020FF081C15':'astrapi'}

# Axis movement increments
x_increment = 1000
y_increment = 1000
z_increment = 50000
rot1_increment = 50000
rot2_increment = 1
stab_increment = 10

# Axis auto (True) or manual (False)
auto_x, auto_y, auto_stab = False, False, False

# Probes Electrode (Astrapi) and Laser
astrapi_total_time_on = 60
astrapi_time_on = 5
astrapi_time_off = 10



#----------------------------------------------------------
#Initial Axis parameters; False == not connected; ''==no serial connection
ser_dict = {'x':'',
           'y':'',
           'z':'',
           'rot':'',
           'rot2':'',
           'r':'',
           'laser': '',
           'astrapi':''}
ax_dict = {'x':False,
           'y':False,
           'z':False,
           'rot':False,
           'rot2':False,
           'r':False,
           'laser':False,
           'astrapi':False}


# Creates folder to save images in
def check_path(experiment="/Test/"):
    global folder
    if not os.path.exists(path+experiment+str(today)):
        os.makedirs(path+experiment+str(today))
    folder = experiment+str(today)
    return folder


#----------------------------------------------------------
# home view, what happens when the page is reloaded
@view.route('/')
def index():
    global icam
    global current_w
    global max_w
    global min_w
    global current_h
    global max_h
    global min_h
    global current_offx
    global max_ox
    global min_ox
    global current_offy
    global max_oy
    global min_oy
    global current_g
    global max_g
    global min_g
    global current_b
    global max_b
    global min_b
    global current_gamma
    global max_gamma
    global min_gamma
    global current_exp
    global max_exposure
    global min_exposure
    # init_cam()

    try:
        icam
    except (NameError) or (TimeoutException):
        connect_axes()
        return render_template('index.html',
                                max_w = 0,min_w = 0 , max_h = 0, min_h = 0,
                                max_ox = 0, min_ox = 0 , max_oy = 0, min_oy = 0,
                                max_g = 0,min_g = 0, min_b = 0 , max_b = 0,
                                max_gamma = 0 , min_gamma = 0,
                                max_exposure = 0,min_exposure = 0 , current_w = 0 , current_exp = 0,
                                current_h = 0 , current_g = 0,
                                current_gamma = 0,
                                current_b = 0 , current_offx = 0 , current_offy = 0,
                                x_connect=ax_dict['x'], y_connect=ax_dict['y'], z_connect=ax_dict['z'],
                                rot_connect=ax_dict['rot'], rot2_connect=ax_dict['rot2'], stab_connect=ax_dict['r'],
                                laser_connect=ax_dict['laser'], astrapi_connect=ax_dict['astrapi']
                                )
    try:
        icam.Width.GetValue()
    except:
        current_w  = 0
        max_w = 0
        min_w = 0
        current_h  = 0
        max_h = 0
        min_h = 0
        current_offx  = 0
        max_ox = 0
        min_ox = 0
        current_offy  = 0
        max_oy = 0
        min_oy = 0
        current_g  = 0
        max_g = 0
        min_g = 0
        current_b  = 0
        max_b = 0
        min_b = 0
        current_gamma  = 0
        max_gamma = 0
        min_gamma = 0
        current_exp  = 0
        max_exposure = 0
        min_exposure = 0
        return render_template('index.html',
                                max_w = 0,min_w = 0 , max_h = 0, min_h = 0,
                                max_ox = 0, min_ox = 0 , max_oy = 0, min_oy = 0,
                                max_g = 0,min_g = 0, min_b = 0 , max_b = 0,
                                max_gamma = 0 , min_gamma = 0,
                                max_exposure = 0,min_exposure = 0 , current_w = 0 , current_exp = 0,
                                current_h = 0 , current_g = 0,
                                current_gamma = 0,
                                current_b = 0 , current_offx = 0 , current_offy = 0,
                                x_connect=ax_dict['x'], y_connect=ax_dict['y'], z_connect=ax_dict['z'],
                                rot_connect=ax_dict['rot'], rot2_connect=ax_dict['rot2'], stab_connect=ax_dict['r'],
                                laser_connect=ax_dict['laser'], astrapi_connect=ax_dict['astrapi']
                                )
    
    current_w  = icam.Width.GetValue()
    max_w = icam.Width.GetMax()
    min_w = icam.Width.GetMin()
    current_h  = icam.Height.GetValue()
    max_h = icam.Height.GetMax()
    min_h = icam.Height.GetMin()
    current_offx  = icam.OffsetX.GetValue()
    max_ox = icam.OffsetX.GetMax()
    min_ox = icam.OffsetX.GetMin()
    current_offy  = icam.OffsetY.GetValue()
    max_oy = icam.OffsetY.GetMax()
    min_oy = icam.OffsetY.GetMin()
    current_g  = icam.Gain.GetValue()
    max_g = icam.Gain.GetMax()
    min_g = icam.Gain.GetMin()
    current_b  = icam.BlackLevel.GetValue()
    max_b = icam.BlackLevel.GetMax()
    min_b = icam.BlackLevel.GetMin()
    current_gamma  = icam.Gamma.GetValue()
    max_gamma = round(icam.Gamma.GetMax(), 2)
    min_gamma = icam.Gamma.GetMin()
    current_exp  = icam.ExposureTime.GetValue()
    max_exposure = icam.ExposureTime.GetMax()
    min_exposure = icam.ExposureTime.GetMin()
    # icam.BalanceWhiteAuto.SetValue("Once")

    connect_axes()

    return render_template('index.html',
                            max_w = max_w,min_w = min_w , max_h = max_h, min_h = min_h,
                            max_ox = max_ox, min_ox = min_ox , max_oy = max_oy, min_oy = min_oy,
                            max_g = max_g,min_g = min_g, min_b = min_b , max_b = max_b,
                            max_gamma = max_gamma , min_gamma = min_gamma,
                            max_exposure = max_exposure,min_exposure = min_exposure , current_w = current_w , current_exp = current_exp,
                            current_h = current_h , current_g = current_g,
                            current_gamma = current_gamma,
                            current_b = current_b , current_offx = current_offx , current_offy = current_offy,
                            x_connect=ax_dict['x'], y_connect=ax_dict['y'], z_connect=ax_dict['z'],
                            rot_connect=ax_dict['rot'], rot2_connect=ax_dict['rot2'], stab_connect=ax_dict['r'],
                            laser_connect=ax_dict['laser'], astrapi_connect=ax_dict['astrapi']
                            )
#-----------------------------------------------------------------------------------------------------------------


# check for axis connections and add names
#-----------------------------------------------------------------------------------------------------------------
def connect_axes():
    global SN_dict
    global ser_dict
    global ax_dict

    port = list(list_ports.comports())
    SN_list = [val for val in SN_dict.keys()]

    p_SN_temp = []
    for p in port:
        if p.serial_number in SN_list:
            p_SN_temp.append(p.serial_number)
            ax = SN_dict[p.serial_number]
            if ax_dict[ax] == False:
                ax_dict[ax] = True
                ser_dict[ax] = serial.Serial(p.device, 115200)
    
    for SN in SN_list:
        if not SN in p_SN_temp:
            ax_dict[SN_dict[SN]] = False
            ser_dict[SN_dict[SN]] = ''


@view.route('/_checkconnect/', methods=['POST'])
def checkconnection():
    global ax_dict
    for key, value in ax_dict.items():
        if value == True:
            if type(ser_dict[key]) == str:
                ax_dict[key] = False
    connect_axes()
    return jsonify({'message': render_template('connect.html', 
                                                x_connect=ax_dict['x'], y_connect=ax_dict['y'], z_connect=ax_dict['z'],
                                                rot_connect=ax_dict['rot'], rot2_connect=ax_dict['rot2'], stab_connect=ax_dict['r'],
                                                laser_connect=ax_dict['laser'], astrapi_connect=ax_dict['astrapi']
                                                )})
#-----------------------------------------------------------------------------------------------------------------


# connect to camera (Basler)
#-----------------------------------------------------------------------------------------------------------------
import pypylon.pylon as py
def init_cam():
    global icam
    start_init = time.time()
    try:
        tl_factory = py.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()

        for i in devices:
            try:
                device = tl_factory.CreateDevice(i)
                icam = py.InstantCamera(device)
                device_name = icam.GetDeviceInfo().GetFriendlyName()
                icam.Open()
                print("Using device ", icam.GetDeviceInfo().GetFriendlyName())
                icam.PixelFormat = "BGR8"
                return icam

            except Exception as e:
                print(e)
    finally:
        print("Camera init time: {} ms".format(int(round((time.time() - start_init) * 1000))))


@view.route('/_camera_on/', methods = ['POST', 'GET'])
def camera_on():
    global current_w
    global max_w
    global min_w
    global current_h
    global max_h
    global min_h
    global current_offx
    global max_ox
    global min_ox
    global current_offy
    global max_oy
    global min_oy
    global current_g
    global max_g
    global min_g
    global current_b
    global max_b
    global min_b
    global current_gamma
    global max_gamma
    global min_gamma
    global current_exp
    global max_exposure
    global min_exposure
    init_cam()
    current_w  = icam.Width.GetValue()
    max_w = icam.Width.GetMax()
    min_w = icam.Width.GetMin()
    current_h  = icam.Height.GetValue()
    max_h = icam.Height.GetMax()
    min_h = icam.Height.GetMin()
    
    current_offx  = icam.OffsetX.GetValue()
    max_ox = icam.OffsetX.GetMax()
    min_ox = icam.OffsetX.GetMin()
    
    current_offy  = icam.OffsetY.GetValue()
    max_oy = icam.OffsetY.GetMax()
    min_oy = icam.OffsetY.GetMin()
    current_g  = icam.Gain.GetValue()
    max_g = icam.Gain.GetMax()
    min_g = icam.Gain.GetMin()
    current_b  = icam.BlackLevel.GetValue()
    max_b = icam.BlackLevel.GetMax()
    min_b = icam.BlackLevel.GetMin()
    current_gamma  = icam.Gamma.GetValue()
    max_gamma = round(icam.Gamma.GetMax(), 2)
    min_gamma = icam.Gamma.GetMin()
    current_exp  = icam.ExposureTime.GetValue()
    max_exposure = icam.ExposureTime.GetMax()
    min_exposure = icam.ExposureTime.GetMin()

    print(icam)
    return jsonify({'message_cam': render_template('camera.html',
                                                    max_w = max_w,min_w = min_w , max_h = max_h, min_h = min_h,
                                                    max_ox = max_ox, min_ox = min_ox , max_oy = max_oy, min_oy = min_oy,
                                                    max_g = max_g,min_g = min_g, min_b = min_b , max_b = max_b,
                                                    max_gamma = max_gamma , min_gamma = min_gamma,
                                                    max_exposure = max_exposure,min_exposure = min_exposure , current_w = current_w , current_exp = current_exp,
                                                    current_h = current_h , current_g = current_g,
                                                    current_gamma = current_gamma,
                                                    current_b = current_b , current_offx = current_offx , current_offy = current_offy),
                    'message_set': render_template('camera_settings.html',
                                                    max_w = max_w,min_w = min_w , max_h = max_h, min_h = min_h,
                                                    max_ox = max_ox, min_ox = min_ox , max_oy = max_oy, min_oy = min_oy,
                                                    max_g = max_g,min_g = min_g, min_b = min_b , max_b = max_b,
                                                    max_gamma = max_gamma , min_gamma = min_gamma,
                                                    max_exposure = max_exposure,min_exposure = min_exposure , current_w = current_w , current_exp = current_exp,
                                                    current_h = current_h , current_g = current_g,
                                                    current_gamma = current_gamma,
                                                    current_b = current_b , current_offx = current_offx , current_offy = current_offy)})

@view.route('/_camera_off/', methods = ['POST', 'GET'])
def camera_off():
    global icam
    icam.Close()
    print(icam)
    global current_w
    global max_w
    global min_w
    global current_h
    global max_h
    global min_h
    global current_offx
    global max_ox
    global min_ox
    global current_offy
    global max_oy
    global min_oy
    global current_g
    global max_g
    global min_g
    global current_b
    global max_b
    global min_b
    global current_gamma
    global max_gamma
    global min_gamma
    global current_exp
    global max_exposure
    global min_exposure
    current_w  = 0
    max_w = 0
    min_w = 0
    current_h  = 0
    max_h = 0
    min_h = 0
    current_offx  = 0
    max_ox = 0
    min_ox = 0
    current_offy  = 0
    max_oy = 0
    min_oy = 0
    current_g  = 0
    max_g = 0
    min_g = 0
    current_b  = 0
    max_b = 0
    min_b = 0
    current_gamma  = 0
    max_gamma = 0
    min_gamma = 0
    current_exp  = 0
    max_exposure = 0
    min_exposure = 0
    return jsonify({'message_cam': render_template('camera.html',
                                                    max_w = max_w,min_w = min_w , max_h = max_h, min_h = min_h,
                                                    max_ox = max_ox, min_ox = min_ox , max_oy = max_oy, min_oy = min_oy,
                                                    max_g = max_g,min_g = min_g, min_b = min_b , max_b = max_b,
                                                    max_gamma = max_gamma , min_gamma = min_gamma,
                                                    max_exposure = max_exposure,min_exposure = min_exposure , current_w = current_w , current_exp = current_exp,
                                                    current_h = current_h , current_g = current_g,
                                                    current_gamma = current_gamma,
                                                    current_b = current_b , current_offx = current_offx , current_offy = current_offy),
                    'message_set': render_template('camera_settings.html',
                                                    max_w = max_w,min_w = min_w , max_h = max_h, min_h = min_h,
                                                    max_ox = max_ox, min_ox = min_ox , max_oy = max_oy, min_oy = min_oy,
                                                    max_g = max_g,min_g = min_g, min_b = min_b , max_b = max_b,
                                                    max_gamma = max_gamma , min_gamma = min_gamma,
                                                    max_exposure = max_exposure,min_exposure = min_exposure , current_w = current_w , current_exp = current_exp,
                                                    current_h = current_h , current_g = current_g,
                                                    current_gamma = current_gamma,
                                                    current_b = current_b , current_offx = current_offx , current_offy = current_offy)})


def gen():
    global icam
    global image
    try: 
        icam
    except NameError:
        image = np.zeros((350, 500, 3), dtype = np.uint8)
        ret, jpeg = cv2.imencode('.jpg', image) 
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type:image/jpeg\r\n'
            b'Content-Length: ' + f"{len(frame)}".encode() + b'\r\n'
            b'\r\n' + frame + b'\r\n')
    else:
        while True:
            image_grab = icam.GrabOne(1000)
            image_raw = image_grab.Array
            image = cv2.resize(image_raw, (0,0), fx=0.8366, fy=1, interpolation=cv2.INTER_LINEAR)
            ret, jpeg = cv2.imencode('.jpg', image)
            cv2.setMouseCallback(".jpg", on_mouse_click_coordinates)

            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type:image/jpeg\r\n'
                b'Content-Length: ' + f"{len(frame)}".encode() + b'\r\n'
                b'\r\n' + frame + b'\r\n')
        

@view.route('/take_image', methods=['GET', 'POST'])
def take_image():
    global image
    global path
    global folder
    img = image.copy()
    folder = check_path(experiment)
    cv2.imwrite(os.path.join(path+folder , str(today)+'_'+str(dt.datetime.now().hour)+'-'+str(dt.datetime.now().minute)+'-'+str(dt.datetime.now().second)+'.png'),img)
    resp = {"success": True}
    return jsonify(resp)


def video_thread(converter=py.ImageFormatConverter()):
    global image
    global duration
    global fps_video

    img = image.copy()
    folder = check_path(experiment)
    s_path = path+folder
    frame_width = len(img[0])
    frame_height = len(img)

    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter(os.path.join(s_path , str(today)+'_'+str(dt.datetime.now().hour)+'-'+str(dt.datetime.now().minute)+'-'+str(dt.datetime.now().second)+'_video_'+'o'.join(str(fps_video).split('.'))+'fps.avi'),cv2.VideoWriter_fourcc('M','J','P','G'), 1, (frame_width,frame_height))

    j = dt.datetime.now()
    print('Start Video Capture at {}'.format(j))

    count_min = 0
    count = 0
    while (dt.datetime.now()-j).seconds <= duration:
        old_n = np.round(float(str(dt.datetime.now()-j).split(':')[-1]), 2)
        if old_n+count_min*60 == np.round(count*(1/fps_video), 2):
            if old_n == 60.0:
                print('now')
                count_min += 1
            print(old_n, old_n+count_min*60, count, count*(1/fps_video))
            img_v = image.copy()
            img_v = np.array(img_v)
            img_v = cv2.resize(img_v, dsize=(frame_width,frame_height))
            # Write the frame into the file 'output.avi'
            out.write(img_v)
            count += 1
            print(count)
    print('End Video Capture after {} s at {}'.format((dt.datetime.now()-j).seconds, dt.datetime.now()))
    cv2.destroyAllWindows()


@view.route('/take_video', methods=['GET', 'POST'])
def take_video():
    global icam
    global video_th
    video_th = threading.Thread(target=video_thread, daemon=True)
    video_th.start()
    resp = {"success": True}
    return jsonify(resp)


@view.route('/video_time', methods=['GET', 'POST'])
def video_time():
    global duration
    if request.method == 'POST':
        r = int(request.form.get('text_video_time'))
        duration = r
    return render_template('index.html')


@view.route('/video_fps', methods=['GET', 'POST'])
def video_fps():
    global fps_video
    if request.method == 'POST':
        r = float(request.form.get('text_video_fps'))
        fps_video = r
    return render_template('index.html')


@view.route('/exposure', methods=['GET', 'POST'])
def exposure():
    global current_exp
    if request.method == 'POST':
        r = int(request.form.get('text_exposure'))
        if min_exposure<=r<=max_exposure:
            icam.ExposureTime.SetValue(r)
            current_exp = icam.ExposureTime.Value
    return jsonify({'message_cam': render_template('camera.html',
                                                    max_w = max_w,min_w = min_w , max_h = max_h, min_h = min_h,
                                                    max_ox = max_ox, min_ox = min_ox , max_oy = max_oy, min_oy = min_oy,
                                                    max_g = max_g,min_g = min_g, min_b = min_b , max_b = max_b,
                                                    max_gamma = max_gamma , min_gamma = min_gamma,
                                                    max_exposure = max_exposure,min_exposure = min_exposure , current_w = current_w , current_exp = current_exp,
                                                    current_h = current_h , current_g = current_g,
                                                    current_gamma = current_gamma,
                                                    current_b = current_b , current_offx = current_offx , current_offy = current_offy),
                    'message_set': render_template('camera_settings.html',
                                                    max_w = max_w,min_w = min_w , max_h = max_h, min_h = min_h,
                                                    max_ox = max_ox, min_ox = min_ox , max_oy = max_oy, min_oy = min_oy,
                                                    max_g = max_g,min_g = min_g, min_b = min_b , max_b = max_b,
                                                    max_gamma = max_gamma , min_gamma = min_gamma,
                                                    max_exposure = max_exposure,min_exposure = min_exposure , current_w = current_w , current_exp = current_exp,
                                                    current_h = current_h , current_g = current_g,
                                                    current_gamma = current_gamma,
                                                    current_b = current_b , current_offx = current_offx , current_offy = current_offy)})

    
@view.route('/blacklevel', methods=['GET', 'POST'])
def blacklevel():
    global current_b
    if request.method == 'POST':
        r = int(request.form.get('text_blacklevel'))
        if min_b<=r<=max_b:
            icam.BlackLevel.SetValue(r)
            current_b = icam.BlackLevel.Value
    return jsonify({'message_cam': render_template('camera.html',
                                                    max_w = max_w,min_w = min_w , max_h = max_h, min_h = min_h,
                                                    max_ox = max_ox, min_ox = min_ox , max_oy = max_oy, min_oy = min_oy,
                                                    max_g = max_g,min_g = min_g, min_b = min_b , max_b = max_b,
                                                    max_gamma = max_gamma , min_gamma = min_gamma,
                                                    max_exposure = max_exposure,min_exposure = min_exposure , current_w = current_w , current_exp = current_exp,
                                                    current_h = current_h , current_g = current_g,
                                                    current_gamma = current_gamma,
                                                    current_b = current_b , current_offx = current_offx , current_offy = current_offy),
                    'message_set': render_template('camera_settings.html',
                                                    max_w = max_w,min_w = min_w , max_h = max_h, min_h = min_h,
                                                    max_ox = max_ox, min_ox = min_ox , max_oy = max_oy, min_oy = min_oy,
                                                    max_g = max_g,min_g = min_g, min_b = min_b , max_b = max_b,
                                                    max_gamma = max_gamma , min_gamma = min_gamma,
                                                    max_exposure = max_exposure,min_exposure = min_exposure , current_w = current_w , current_exp = current_exp,
                                                    current_h = current_h , current_g = current_g,
                                                    current_gamma = current_gamma,
                                                    current_b = current_b , current_offx = current_offx , current_offy = current_offy)})

    
@view.route('/gamma', methods=['GET', 'POST'])
def gamma():
    global current_gamma
    if request.method == 'POST':
        r = int(request.form.get('text_gamma'))
        if min_gamma<=r<=max_gamma:
            icam.Gamma.SetValue(r)
            current_gamma = icam.Gamma.Value
    return jsonify({'message_cam': render_template('camera.html',
                                                    max_w = max_w,min_w = min_w , max_h = max_h, min_h = min_h,
                                                    max_ox = max_ox, min_ox = min_ox , max_oy = max_oy, min_oy = min_oy,
                                                    max_g = max_g,min_g = min_g, min_b = min_b , max_b = max_b,
                                                    max_gamma = max_gamma , min_gamma = min_gamma,
                                                    max_exposure = max_exposure,min_exposure = min_exposure , current_w = current_w , current_exp = current_exp,
                                                    current_h = current_h , current_g = current_g,
                                                    current_gamma = current_gamma,
                                                    current_b = current_b , current_offx = current_offx , current_offy = current_offy),
                    'message_set': render_template('camera_settings.html',
                                                    max_w = max_w,min_w = min_w , max_h = max_h, min_h = min_h,
                                                    max_ox = max_ox, min_ox = min_ox , max_oy = max_oy, min_oy = min_oy,
                                                    max_g = max_g,min_g = min_g, min_b = min_b , max_b = max_b,
                                                    max_gamma = max_gamma , min_gamma = min_gamma,
                                                    max_exposure = max_exposure,min_exposure = min_exposure , current_w = current_w , current_exp = current_exp,
                                                    current_h = current_h , current_g = current_g,
                                                    current_gamma = current_gamma,
                                                    current_b = current_b , current_offx = current_offx , current_offy = current_offy)})



@view.route('/gain', methods=['GET', 'POST'])
def gain():
    global current_g
    if request.method == 'POST':
        r = int(request.form.get('text_gain'))
        if min_g<=r<=max_g:
            icam.Gain.SetValue(r)
            current_g = icam.Gain.Value
    return jsonify({'message_cam': render_template('camera.html',
                                                    max_w = max_w,min_w = min_w , max_h = max_h, min_h = min_h,
                                                    max_ox = max_ox, min_ox = min_ox , max_oy = max_oy, min_oy = min_oy,
                                                    max_g = max_g,min_g = min_g, min_b = min_b , max_b = max_b,
                                                    max_gamma = max_gamma , min_gamma = min_gamma,
                                                    max_exposure = max_exposure,min_exposure = min_exposure , current_w = current_w , current_exp = current_exp,
                                                    current_h = current_h , current_g = current_g,
                                                    current_gamma = current_gamma,
                                                    current_b = current_b , current_offx = current_offx , current_offy = current_offy),
                    'message_set': render_template('camera_settings.html',
                                                    max_w = max_w,min_w = min_w , max_h = max_h, min_h = min_h,
                                                    max_ox = max_ox, min_ox = min_ox , max_oy = max_oy, min_oy = min_oy,
                                                    max_g = max_g,min_g = min_g, min_b = min_b , max_b = max_b,
                                                    max_gamma = max_gamma , min_gamma = min_gamma,
                                                    max_exposure = max_exposure,min_exposure = min_exposure , current_w = current_w , current_exp = current_exp,
                                                    current_h = current_h , current_g = current_g,
                                                    current_gamma = current_gamma,
                                                    current_b = current_b , current_offx = current_offx , current_offy = current_offy)})


@view.route('/video')
def video():
    global frame_c
    global icam
    # """Video streaming route. Put this in the src attribute of an img tag."""
    frame_c = gen()
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@view.route('/click-coordinates', methods=['POST'])
def handle_click():
    data = request.get_json()
    print("Received click at:", data['x'], data['y'])
    # Process coordinates as needed
    return jsonify({"status": "success", "x": data['x'], "y": data['y']})

#-----------------------------------------------------------------------------------------------------------------


# Add movement for axes
#-----------------------------------------------------------------------------------------------------------------

# Function that sets parameters for movement and sends all information to necessary stage - in manual mode
def move(axis_name, steps=100, dir=0, micro=0, rms=0, hold=0, home=False):
    global notconnected
    global movenotpossible
    axis = ser_dict[axis_name]
    if ax_dict[axis_name] == False:
        notconnected = True
    elif type(axis) == str:
        movenotpossible = True
    else:
        if home:
            axis.write(str.encode('h'))
        else:
            if micro != 0:
                axis.write(str.encode('m'+str(micro)))
            if rms != 0:
                axis.write(str.encode('r'+str(rms)))
            # if delayTime != 0:
            #     axis.write(str.encode('t'+str(delayTime)))
            axis.write(str.encode('d'+str(dir)))
            axis.write(str.encode('e'+str(hold)))
            axis.write(str.encode('x'+str(steps)))


# switch between manual and auto mode
def go_auto_mode(axis_name, go_auto=True):
    axis = ser_dict[axis_name]
    time.sleep(2)
    if go_auto:
        axis.write(str.encode('a2'))
        return True
    else:
        axis.write(str.encode('a0'))
        return False


# Function that sets parameters for movement and sends all information to necessary stage, - in auto mode
def move_with_pos(axis_name, steps=100, home=False):
    axis = ser_dict[axis_name]
    if ax_dict[axis_name] == False:
        notconnected = True
    elif type(axis) == str:
        movenotpossible = True
    else:
        if home:
            axis.write(str.encode('h'))
        else:
            axis.write(str.encode('x'+str(steps)))


# X-axis buttons
@view.route('/_left/', methods = ['POST', 'GET'])
def left():
    global auto_x
    axis_name = 'x'
    if auto_x:
        steps = x_increment
        move_with_pos(axis_name, steps)
    else:
        dir = 0
        steps = x_increment
        micro = 16 # make it dependent on the stepsize
        rms = 850 # make it dependent on the stepsize
        hold = 1
        move(axis_name, steps, dir, micro, rms, hold)
    resp = {"success": True}
    return jsonify(resp)


@view.route('/_right/', methods = ['POST', 'GET'])
def right():
    global auto_x
    axis_name = 'x'
    if auto_x:
        steps = -x_increment
        move_with_pos(axis_name, steps)
    else:
        dir = 1
        steps = x_increment
        micro = 16 # make it dependent on the stepsize
        rms = 850 # make it dependent on the stepsize
        hold = 1
        move(axis_name, steps, dir, micro, rms, hold)
    resp = {"success": True}
    return jsonify(resp)


# Y-axis buttons
@view.route('/_up/', methods = ['POST', 'GET'])
def up():
    global auto_y
    axis_name = 'y'
    if auto_y:
        steps = y_increment
        print('pos y')
        move_with_pos(axis_name, steps)
    else:
        dir = 0
        steps = y_increment
        micro = 16 # make it dependent on the stepsize
        rms = 850 # make it dependent on the stepsize
        hold = 1
        print('steps y')
        move(axis_name, steps, dir, micro, rms, hold)
    resp = {"success": True}
    return jsonify(resp)


@view.route('/_down/', methods = ['POST', 'GET'])
def down():
    global auto_y
    axis_name = 'y'
    if auto_y:
        print('pos y')
        steps = -y_increment
        move_with_pos(axis_name, steps)
    else:
        dir = 1
        steps = y_increment
        micro = 16 # make it dependent on the stepsize
        rms = 850 # make it dependent on the stepsize
        hold = 1
        print('steps y')
        move(axis_name, steps, dir, micro, rms, hold)
    resp = {"success": True}
    return jsonify(resp)


# Z-axis buttons
@view.route('/_Zup/', methods = ['POST', 'GET'])
def Zup():
    axis_name = 'z'
    dir = 1
    steps = z_increment
    micro = 1 # make it dependent on the stepsize
    rms = 850 # make it dependent on the stepsize
    hold = 1
    move(axis_name, steps, dir, micro, rms, hold)
    resp = {"success": True}
    return jsonify(resp)


@view.route('/_Zdown/', methods = ['POST', 'GET'])
def Zdown():
    axis_name = 'z'
    dir = 0
    steps = z_increment
    micro = 1 # make it dependent on the stepsize
    rms = 850 # make it dependent on the stepsize
    hold = 1
    move(axis_name, steps, dir, micro, rms, hold)
    resp = {"success": True}
    return jsonify(resp)


# Rot1 buttons
@view.route('/_rot_clock/', methods = ['POST', 'GET'])
def rot_clock():
    axis_name = 'rot'
    dir = 0
    steps = rot1_increment
    micro = 1 # make it dependent on the stepsize
    rms = 850 # make it dependent on the stepsize
    hold = 1
    move(axis_name, steps, dir, micro, rms, hold)
    resp = {"success": True}
    return jsonify(resp)


@view.route('/_rot_anticlock/', methods = ['POST', 'GET'])
def rot_anticlock():
    axis_name = 'rot'
    dir = 1
    steps = rot1_increment
    micro = 1 # make it dependent on the stepsize
    rms = 850 # make it dependent on the stepsize
    hold = 1
    move(axis_name, steps, dir, micro, rms, hold)
    resp = {"success": True}
    return jsonify(resp)


# Rot2 buttons
@view.route('/_Z_rot_clock/', methods = ['POST', 'GET'])
def Z_rot_clock():
    axis_name = 'rot2'
    dir = 0
    steps = rot2_increment
    micro = 32
    rms = 500
    hold = 1
    move(axis_name, steps, dir, micro, rms, hold)
    resp = {"success": True}
    return jsonify(resp)

@view.route('/_Z_rot_anticlock/', methods = ['POST', 'GET'])
def Z_rot_anticlock():
    axis_name = 'rot2'
    dir = 1
    steps = rot2_increment
    micro = 32
    rms = 500
    hold = 1
    move(axis_name, steps, dir, micro, rms, hold)
    resp = {"success": True}
    return jsonify(resp)


# R-axis buttons
@view.route('/_stab_out/', methods = ['POST', 'GET'])
def stab_out():
    global auto_stab
    axis_name = 'r'
    if auto_stab:
        steps = -stab_increment
        move_with_pos(axis_name, steps)
    else:
        dir = 1
        steps = stab_increment
        micro = 16 # make it dependent on the stepsize
        rms = 850 # make it dependent on the stepsize
        hold = 1
        move(axis_name, steps, dir, micro, rms, hold)
    resp = {"success": True}
    return jsonify(resp)


@view.route('/_stab_in/', methods = ['POST', 'GET'])
def stab_in():
    global auto_stab
    axis_name = 'r'
    if auto_stab:
        steps = stab_increment
        move_with_pos(axis_name, steps)
    else:
        dir = 0
        steps = stab_increment
        micro = 16 # make it dependent on the stepsize
        rms = 850 # make it dependent on the stepsize
        hold = 1
        move(axis_name, steps, dir, micro, rms, hold)
    resp = {"success": True}
    return jsonify(resp)


#-----------------------------------------------------------------------------------------------------------------


# Change manual/automatic mode of axis
#-----------------------------------------------------------------------------------------------------------------
@view.route('/manual_x/', methods=['GET', 'POST'])
def manual_x_f():
    global auto_x
    axis_name = 'x'
    auto_x = go_auto_mode(axis_name, go_auto=False)
    resp = {"success": True}
    return jsonify(resp)

@view.route('/automatic_x/', methods=['GET', 'POST'])
def automatic_x_f():
    global auto_x
    axis_name = 'x'
    auto_x = go_auto_mode(axis_name, go_auto=True)
    resp = {"success": True}
    return jsonify(resp)

@view.route('/manual_y/', methods=['GET', 'POST'])
def manual_y_f():
    global auto_y
    axis_name = 'y'
    auto_y = go_auto_mode(axis_name, go_auto=False)
    resp = {"success": True}
    return jsonify(resp)

@view.route('/automatic_y/', methods=['GET', 'POST'])
def automatic_y_f():
    global auto_y
    axis_name = 'y'
    auto_y = go_auto_mode(axis_name, go_auto=True)
    resp = {"success": True}
    return jsonify(resp)

@view.route('/manual_stab/', methods=['GET', 'POST'])
def manual_stab_f():
    global auto_stab
    axis_name = 'r'
    auto_stab = go_auto_mode(axis_name, go_auto=False)
    resp = {"success": True}
    return jsonify(resp)

@view.route('/automatic_stab/', methods=['GET', 'POST'])
def automatic_stab_f():
    global auto_stab
    axis_name = 'r'
    auto_stab = go_auto_mode(axis_name, go_auto=True)
    resp = {"success": True}
    return jsonify(resp)



# Change stepsize of movement
#-----------------------------------------------------------------------------------------------------------------
@view.route('/x_increment', methods=['GET', 'POST'])
def x_increment_f():
    global x_increment
    if request.method == 'POST':
        r = float(request.form.get('text_x_increment'))
        x_increment = r
    return render_template('index.html')

@view.route('/y_increment', methods=['GET', 'POST'])
def y_increment_f():
    global y_increment
    if request.method == 'POST':
        r = float(request.form.get('text_y_increment'))
        y_increment = r
    return render_template('index.html')

@view.route('/z_increment', methods=['GET', 'POST'])
def z_increment_f():
    global z_increment
    if request.method == 'POST':
        r = float(request.form.get('text_z_increment'))
        z_increment = r
    return render_template('index.html')

@view.route('/rot1_increment', methods=['GET', 'POST'])
def rot1_increment_f():
    global rot1_increment
    if request.method == 'POST':
        r = float(request.form.get('text_rot1_increment'))
        rot1_increment = r
    return render_template('index.html')

@view.route('/rot2_increment', methods=['GET', 'POST'])
def rot2_increment_f():
    global rot2_increment
    if request.method == 'POST':
        r = float(request.form.get('text_rot2_increment'))
        rot2_increment = r
    return render_template('index.html')

@view.route('/stab_increment', methods=['GET', 'POST'])
def stab_increment_f():
    # 3.000 steps in 1/16 steps in total
    global stab_increment
    if request.method == 'POST':
        r = float(request.form.get('text_stab_increment'))
        stab_increment = r
    return render_template('index.html')



#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
# Probes
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------

@view.route('/astrapi_on/', methods = ['POST', 'GET'])
def astrapi_on():
    axis = ser_dict['astrapi']
    axis.write(str.encode('t'+str(astrapi_time_on)))
    axis.write(str.encode('o'+str(astrapi_time_off)))
    axis.write(str.encode('a'+str(astrapi_total_time_on)))
    time.sleep(2)
    axis.write(str.encode('s'))
    return render_template('index.html')

@view.route('/astrapi_off/', methods = ['POST', 'GET'])
def astrapi_off():
    axis = ser_dict['astrapi']
    axis.write(str.encode('q'))
    return render_template('index.html')


@view.route('/astrapi_total_time_on', methods=['GET', 'POST'])
def astrapi_total_time_on_f():
    global astrapi_total_time_on
    if request.method == 'POST':
        r = float(request.form.get('text_astrapi_total_time_on'))
        astrapi_total_time_on = r
    return render_template('index.html')

@view.route('/astrapi_time_on', methods=['GET', 'POST'])
def astrapi_time_on_f():
    global astrapi_time_on
    if request.method == 'POST':
        r = float(request.form.get('text_astrapi_time_on'))
        astrapi_time_on = r
    return render_template('index.html')

@view.route('/astrapi_time_off', methods=['GET', 'POST'])
def astrapi_time_off_f():
    global astrapi_time_off
    if request.method == 'POST':
        r = float(request.form.get('text_astrapi_time_off'))
        astrapi_time_off = r
    return render_template('index.html')



@view.route('/laser_on/', methods = ['POST', 'GET'])
def laser_on():
    axis = ser_dict['laser']
    axis.write(str.encode('s'))
    return render_template('index.html')

@view.route('/laser_off/', methods = ['POST', 'GET'])
def laser_off():
    axis = ser_dict['laser']
    axis.write(str.encode('q'))
    return render_template('index.html')

@view.route('/laser_total_time_on', methods=['GET', 'POST'])
def laser_total_time_on_f():
    global laser_total_time_on
    axis = ser_dict['laser']
    if request.method == 'POST':
        r = float(request.form.get('text_laser_total_time_on'))
        laser_total_time_on = r
        axis.write(str.encode('a'+str(laser_total_time_on)))
    return render_template('index.html')

@view.route('/laser_time_on', methods=['GET', 'POST'])
def laser_time_on_f():
    global laser_time_on
    axis = ser_dict['laser']
    if request.method == 'POST':
        r = float(request.form.get('text_laser_time_on'))
        laser_time_on = r
        axis.write(str.encode('t'+str(laser_time_on)))
    return render_template('index.html')

@view.route('/laser_time_off', methods=['GET', 'POST'])
def laser_time_off_f():
    global laser_time_off
    axis = ser_dict['laser']
    if request.method == 'POST':
        r = float(request.form.get('text_laser_time_off'))
        laser_time_off = r
        axis.write(str.encode('o'+str(laser_time_off)))
    return render_template('index.html')

#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------


# get coordinates on click
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
def on_mouse_click_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked at: {x}, {y}")
        