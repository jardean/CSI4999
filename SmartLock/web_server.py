import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for
#from authenticator import auth
from flask_login import login_user, logout_user, login_required, current_user
from . import db
import SmartLock.database as database
from gpiozero import LED
from time import sleep

led = LED(17)

home = Blueprint('home', __name__)

#This Route is the index page (landing page) -Adrian
@home.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')
   
#This routes is the dashboard page -Adrian
@home.route('/dashboard')
@login_required
def dashboard():
    #displays details of user in dashboard
    details = current_user.username
    return render_template('dashboard.html', info = details)

#This routes is the dashboard post page to handle post commands inside the dashboard web page -Adrian
@home.route('/dashboard', methods=['POST'])
@login_required
def post_dashboard():
    #if the log out button is clicked 
    if 'logout' in request.form:
        return redirect(url_for('auth.logout'))
    if 'confirm' in request.form:

        pas = request.form.get('rpi_password')
        pas_c = request.form.get('rpi_confirm_password')

        if pas == pas_c:
            print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('pass confirm'))
            return redirect(url_for('auth.rpi_config', pas=pas))
        else:
            print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('pass not confirmed'))
            return dashboard()


#This route is the keypad page
@home.route("/keypad")
@login_required
def keypad():
    #TODO: Update to the proper keypad.html file
    return render_template('pinpad_test.html') 

#This route is the keypad landing page for post commands
@home.route("/keypad", methods=['POST'])
@login_required
def post_keypad():
    #Jared
    #if keypad enter button is pressed
    if 'submitpin' in request.form:
        #TODO error detection for keypad inputs to be entered here
        print('IN SUBMIT')
        #scrape input from the pin textbox
        pin = request.form.get('userpin')

        rpi = database.query_rpi()

        #if no input is detected
        if rpi == None:
            return redirect(url_for('home.keypad'))
        else:
            #authenticate entered pin with the pin code in the db
            if rpi.pin_Code == current_user.pin_Code:
                #open door
                led.on()
                #TODO interface code between rpi and door lock
                sleep(5)
                led.off()
                return redirect(url_for('home.keypad'))
            else:
                return redirect(url_for('home.keypad'))
    else:
        return redirect(url_for('home.keypad'))

