# -*- coding: utf-8 -*-

from . import main
from flask import render_template, request, make_response, send_from_directory
import config


@main.route('/tss-donation', methods=['GET'])
def tss_donation():
    return render_template("tss-donation/tss-donation.html")
