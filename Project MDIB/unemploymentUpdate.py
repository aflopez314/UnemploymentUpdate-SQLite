import os
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify, make_response
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import pandas as pd
import sqlite3 as sql

UPLOADS = r'S:\Python Projects\Job Search Data Visualization\Project MDIB\static'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOADS'] = UPLOADS

def allowed_file(filename):
   return '.' in filename and \
   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/Login')
def login():
   return render_template('login.html')

@app.route('/')
def home():
   con = sql.connect(r"S:\Python Projects\Job Search Data Visualization\Project MDIB\unemploymentDatabase.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("SELECT * FROM JobsApplied")
   rows = cur.fetchall();
   return render_template('home.html', rows=rows)
   con.close()

@app.route('/updateform')
def update_install():
   con = sql.connect(r"S:\Python Projects\Job Search Data Visualization\Project MDIB\unemploymentDatabase.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("SELECT * FROM JobsApplied")
   rows = cur.fetchall();
   return render_template('updateform.html', rows=rows)
   con.close()

@app.route('/d3Data')
def d3Data():
   def dict_factory(cursor, row):
      d = {}
      for idx, col in enumerate(cursor.description):
         d[col[0]] = row[idx]
      return d
   con = sql.connect(r"S:\Python Projects\Job Search Data Visualization\Project MDIB\unemploymentDatabase.db")
   con.row_factory = dict_factory
   cur = con.cursor()
   cur.execute("SELECT AppDate,COUNT(Site) AS SiteCounts FROM JobsApplied GROUP BY  AppDate ORDER BY AppDate DESC")
   counts = cur.fetchall()
   return jsonify(counts)

@app.route('/webGraphData')
def webGraphData():
   def dict_factory(cursor, row):
      d = {}
      for idx, col in enumerate(cursor.description):
         d[col[0]] = row[idx]
      return d
   con = sql.connect(r"S:\Python Projects\Job Search Data Visualization\Project MDIB\unemploymentDatabase.db")
   con.row_factory = dict_factory
   cur = con.cursor()
   cur.execute("SELECT Position FROM JobsApplied ORDER BY Position DESC")
   positions = cur.fetchall()
   return jsonify(positions)

@app.route('/circleData')
def circleData():
   def dict_factory(cursor, row):
      d = {}
      for idx, col in enumerate(cursor.description):
         d[col[0]] = row[idx]
      return d
   con = sql.connect(r"S:\Python Projects\Job Search Data Visualization\Project MDIB\unemploymentDatabase.db")
   con.row_factory = dict_factory
   cur = con.cursor()
   cur.execute("SELECT Response,COUNT(Response) as ResponseCounts FROM JobsApplied GROUP BY Response")
   response = cur.fetchall()
   return jsonify(response)


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         Site = request.form['Site']
         Position = request.form['Position']
         AppDate = datetime.strptime(request.form['AppDate'],'%Y-%m-%d').strftime('%m/%d/%Y')
         Response = request.form['Response']
         Interview = request.form['Interview']
         with sql.connect(r"S:\Python Projects\Job Search Data Visualization\Project MDIB\unemploymentDatabase.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO JobsApplied (Site,Position,AppDate,Response,Interview) VALUES (?,?,?,?,?)",(Site,Position,AppDate,Response,Interview) )
            con.commit()
            msg = "Record successfully added"
      except:
         msg = "error in insert operation"
         con.rollback()
      finally:
         return render_template("result.html",msg=msg)
         con.close()

@app.route('/deleterec', methods= ['GET', 'POST'])
def deleterec():
   if request.method=='POST':
      try:
         data = request.get_json()
         Site = data.get('Site')
         Position = data.get('Position')
         AppDate =  data.get('AppDate')
         Response =  data.get('Response')
         Interview =  data.get('Interview')
         with sql.connect(r"S:\Python Projects\Job Search Data Visualization\Project MDIB\unemploymentDatabase.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM JobsApplied WHERE Site=? AND Position=?", (Site,Position))
            con.commit()
            msg = "Record successfully deleted"
      except:
         msg = "error in delete operation"
         con.rollback()
      finally:
         return render_template("result.html",msg=msg, data=data, Site=AppDate)
         con.close()

@app.route('/addfile', methods = ['GET', 'POST'])
def addfile():
   if request.method == 'POST':
      if 'file' not in request.files:
         flash('No file found')
         return redirect('updateform.html')
      try:
         file = request.files['file']
         if file.filename == '':
            flash('No file selected')
            return redirect('updateform.html')
         if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOADS'], filename)
            file.save(path)
            msg = "File data successfully added"

            df = pd.read_csv(path)
            chart_data = df.to_dict(orient='Site')
            for item in chart_data:
               Site = item['Site']
               Position = item['Position']
               AppDate = item['AppDate']
               Response = item['Response']
               Interview = item['Interview']
               with sql.connect(r"S:\Python Projects\Job Search Data Visualization\Project MDIB\unemploymentDatabase.db") as con:
                  cur = con.cursor()
                  cur.execute("INSERT INTO JobsApplied (Site,Position,AppDate,Response,Interview) VALUES (?,?,?,?,?)",(Site,Position,AppDate,Response,Interview) )
                  con.commit()
      except:
         msg = "error in upload operation"
         con.rollback()
      finally:
         return render_template("result.html", msg=msg)
         con.close()
   return "'" 

@app.route('/list')
def list():
   con = sql.connect(r"S:\Python Projects\Job Search Data Visualization\Project MDIB\ConstructionProject.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from JobsApplied")
   rows = cur.fetchall();
   return render_template("list.html",rows=rows)

if __name__ == '__main__':
   app.run(debug=True)
