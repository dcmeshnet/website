#!/usr/bin/env python3

import cgi
import sqlite3
import urllib.parse
import requests
import json


def application(environ, start_response):
    post_env = environ.copy()
    post_env["QUERY_STRING"] = ''
    form = cgi.FieldStorage(
        fp=environ['wsgi.input'], environ=post_env, keep_blank_values=True)

    conn = sqlite3.connect('/data/nodes.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS nodes (
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT, 
        address TEXT NOT NULL,
        lat REAL NOT NULL,
        long REAL NOT NULL,
        roof_access INTEGER NOT NULL,
        connected INTEGER NOT NULL
    )''')
    encoded_address = urllib.parse.quote_plus(
        form["address"].value.encode('UTF-8'))

    geocode = requests.get(
        f"https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address={encoded_address}&benchmark=2020&format=json")

    location_result= geocode.json()
    if not location_result["result"]["addressMatches"]:
        start_response('200 OK', [('Content-Type', 'text/json')])
        return ['{ "error": "Address Error"}'.encode('UTF-8')]
    else:
        lat = location_result["result"]["addressMatches"][0]["coordinates"]["y"]
        long = location_result["result"]["addressMatches"][0]["coordinates"]["x"]
    roof = 0
    if form.getvalue("roof") == "roof_access":
        roof = 1

    new_node = (form["name"].value, form["email"].value, form["phone"].value,
                form["address"].value, lat, long, roof, 0)

    c.execute('INSERT INTO nodes (name, email, phone, address, lat, long, roof_access, connected) VALUES (?,?,?,?,?,?,?,?)', new_node)

    conn.commit()

    start_response('200 OK', [('Content-Type', 'text/html')])
    return None
