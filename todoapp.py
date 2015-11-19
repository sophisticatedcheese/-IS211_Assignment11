__author__ = 'T.J November 2015'


from flask import Flask, render_template
from flask import request, redirect, flash
import glob
import re
import pickle

class SaveList(object):


    def __init__(self, filename=None):
        self.filename = filename

    def save(self, item_list):
        with open(self.filename, "wb") as save_list:
            pickle.dump(item_list, save_list)
            print 'List saved'

    def load(self):
        with open(self.filename, "rb") as item_list:
            state = pickle.load(item_list)
            print 'List loaded'
            return state

"""Beginning of the app"""

app = Flask(__name__)       # build app
app.secret_key = 'secret'   # so flash() function is operable

TO_DO = []

filename = 'save_list.txt'
save_list = SaveList(filename)

if glob.glob(filename):
    TO_DO = save_list.load()                # overwrites TO_DO with the load list

@app.route('/')
def home():
    return render_template('index.html', to_do=TO_DO)   # passing to_do list into HTML

@app.route('/submit', methods=['POST'])
def submit():
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']
    row_id = len(TO_DO)                     # sets row_id = list[i] to be deleted

    email_pattern = re.compile(r'[a-zA-Z0-9.!*&$#_%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}')

    if email_pattern.match(email):
        TO_DO.append((task, email, priority, row_id))       # match email pattern
        save_list.save(TO_DO)
    else:
        flash('Invalid email address')

    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear():
    TO_DO[:] = []                               # reset list
    save_list.save(TO_DO)
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():

    id = request.form.get('row_id', type=int)   # multi-dict cast as int

    for row in TO_DO:
        if row[3] == id:
            TO_DO.remove(row)

    save_list.save(TO_DO)                       # save the list
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
