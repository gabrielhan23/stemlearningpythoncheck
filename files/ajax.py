from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
import uuid, json

from files.setup import *
from files.databases import *
from files.forms import *
from files.functions import *

@app.route('/test', methods=['POST'])
def test():
  print("test")