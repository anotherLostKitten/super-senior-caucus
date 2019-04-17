from urllib import request, parse
import json
import sqlite3
from os import urandom
from random import randint

from flask import Flask, render_template, request, flash, redirect, url_for, make_response, Request

app = Flask(__name__)

app.secret_key = urandom(32)

@app.route("/")
def home():
    return render_template("men.html", cand = [{"name":"uddin"},{"name":"peters"},{"name":"mcbarron"}],capitalize = capitalize)
@app.route("/vote/<men>")
def vote(men):
    ip = request.remote_addr
    if not vore(ip,men):
        flash("Vote updated.")
    return redirect("/results")
@app.route("/results")
def respag():
    if has_vore(request.remote_addr):
        return render_template("res.html",stats=vore_count(),capitalize = capitalize)
    else:
        return redirect("/")
def vore(ip,cand):
    db=sqlite3.connect("votes.db")
    squul=db.cursor()
    b = True
    if squul.execute("SELECT * FROM votes WHERE ip = ?",(ip,)).fetchone()==None:
        squul.execute("INSERT INTO votes VALUES (?, ?);",(ip,cand))
    else:
        squul.execute("UPDATE votes SET vote = ? WHERE ip = ?;",(cand,ip))
        b = False
    db.commit()
    db.close()
    return b
def has_vore(ip):
    db=sqlite3.connect("votes.db")
    squul=db.cursor()
    b = squul.execute("SELECT * FROM votes WHERE ip = ?",(ip,)).fetchone()!=None
    db.close()
    return b
def vore_count():
    db=sqlite3.connect("votes.db")
    squul=db.cursor()
    vts = squul.execute("SELECT vote FROM votes;").fetchall()
    db.close()
    vd = {}
    for i in vts:
        if i[0] in vd:
            vd[i[0]]+=1
        else:
            vd[i[0]]=1
    vd=sorted([(k,vd[k])for k in list(vd)],key=lambda d:d[1])
    return vd
def reset():
    db=sqlite3.connect("votes.db")
    squul=db.cursor()
    squul.execute("DROP TABLE IF EXISTS votes;")
    squul.execute("CREATE TABLE votes (ip TEXT, vote TEXT);")
def capitalize(move):
    '''capitalized series of words seperated by either hyphens or spaces'''
    seperate = move.split(" ")
    result = ""
    for move in seperate:
        result += move.capitalize() + " "
    seperate = result[:-1].split("-")
    result = ""
    for move in seperate:
        result += move[0].upper() + move[1:] + " " 
    return result[:-1]
if __name__ == "__main__":
    reset()
    app.debug = True
    app.run()
