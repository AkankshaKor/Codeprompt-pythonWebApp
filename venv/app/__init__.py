from flask import Flask, render_template,request
from config import Config
import sqlite3 as db
import matplotlib.pyplot as plt
import matplotlib
import plotly.plotly as py
import plotly.graph_objs as go

from pylab import figure, axes, pie, title, show
matplotlib.use('Agg')
import numpy as np

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    user = {'username': 'Miguel'}
    return  render_template('index.html',user=user,title='Home')


@app.route('/handle_data', methods=['POST'])
def handle_data():
    con = db.connect('itemdatabase.db', timeout=100000000000000)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS cars (FirstName char(50) NOT NULL,email char(50) NOT NULL,phoneno bigint,cartype char(50) NOT NULL,milage int,monthly_income int,fraction_of_maintain int,working_hours_or_days int)");

    list_cars = []
    list_cars.append(request.form['firstname'])
    list_cars.append(request.form['email'])
    list_cars.append(request.form['phone'])
    list_cars.append(request.form['Car'])
    list_cars.append(request.form['milage'])
    list_cars.append(request.form['income'])
    list_cars.append(request.form['maintenance'])
    list_cars.append(request.form['engagement'])
    cur.execute('INSERT INTO cars VALUES (?,?,?,?,?,?,?,?)', list_cars)
    con.commit()
    con = db.connect('itemdatabase.db', timeout=2000000000000)
    cur = con.cursor()
    x = []
    y = []
    for row in cur.execute('SELECT working_hours_or_days  FROM  cars'):
        print(row)
        x.append(row[0])

    for row in cur.execute('SELECT monthly_income FROM  cars'):
        print(row)
        y.append(row[0])

    print(request.form['option'])

    if( request.form['option'] == '0'):
        plt.xlabel("Working Hours")
        plt.ylabel("Monthly income")
        plt.title("Line Graph")
        plt.plot(x,y)
        plt.savefig("../Static/data.png")

        plt.clf()
       # plt.show()

    elif(request.form['option'] == '1'):
        plt.xlabel("Working Hours")
        plt.ylabel("Monthly income")
        plt.title("Scatter Graph")
        plt.scatter(x,y)
        plt.show()

    else:
        plt.hist(x,bins=6)
        plt.xlabel("Working hours")
        plt.ylabel("Number of people")
        plt.title("Histogram for working hours")
        plt.show()
    return render_template('output.html')

    #print(cur.fetchall())





if __name__ == '__main__':
    app.run(debug=True)

