#!/usr/bin/env python3

import cgi
import sqlite3
import json


def application(environ, start_response):
    conn = sqlite3.connect('/data/nodes.db')
    conn.row_factory = sqlite3.Row

    conn.execute('''CREATE TABLE IF NOT EXISTS nodes (
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT, 
        address TEXT NOT NULL,
        lat REAL NOT NULL,
        long REAL NOT NULL,
        roof_access INTEGER NOT NULL,
        connected INTEGER NOT NULL
    )''')

    cur = conn.cursor()
    cur.execute('SELECT rowid, lat, long, connected FROM nodes')

    nodes = cur.fetchall()

    if nodes:
        content = json.dumps([tuple(row) for row in nodes])
    else:
        content = None
    start_response('200 OK', [('Content-Type', 'application/json')])
    return [content.encode('UTF-8')]
