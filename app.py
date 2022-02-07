from flask import Flask
import db


cur = db.start_db()
if cur!=None:
	q= "begin;"+open("create_table.sql", "r").read()+"commit;"
	cur.execute(q) 
	print("table created\n")


app = Flask(__name__)




@app.route('/')
def index():
    return 'Index Page!!!'