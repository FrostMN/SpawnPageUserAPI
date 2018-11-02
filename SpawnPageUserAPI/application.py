from flask import Flask, render_template, redirect, url_for, request
from config import ConfigPicker
import os

conf = ConfigPicker(os.environ['ENV'])


app = Flask(__name__)
app.config.from_object(conf)
