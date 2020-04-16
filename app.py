import sqlite3
import os
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, length
from wtforms import TextAreaField

app = Flask(__name__)
app.debug = False
app.secret_key = 'svsdfvsdfvbadb  sfgsgsrg'

aktualni_adresar = os.path.abspath(os.path.dirname(__file__))
databaze = (os.path.join(aktualni_adresar, 'poznamky.db'))

class PoznamkaForm(FlaskForm):
    poznamka = TextAreaField("Poznámka", validators=[DataRequired(), length(max=250)])

@app.route('/formular', methods=['GET', 'POST'])
def formular():
    form = PoznamkaForm()
    poznamka_text = form.poznamka.data     
    if form.validate_on_submit():
        conn = sqlite3.connect(databaze)
        c = conn.cursor()
        c.execute("INSERT INTO poznamky(poznamka) VALUES (?)", (poznamka_text,))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('formular.html', form=form)

@app.route('/')
def vypis():
    conn = sqlite3.connect(databaze)
    c = conn.cursor()
    c.execute("SELECT rowid, poznamka, vlozeno, dulezitost FROM poznamky ORDER BY vlozeno DESC")
    vypis_poznamek = c.fetchall()
    conn.close()
    return render_template('vypis.html', vypis_poznamek=vypis_poznamek)

@app.route('/smaz/<int:poznamka_id>')
def smaz_poznamku(poznamka_id):
    conn = sqlite3.connect(databaze)
    c = conn.cursor()
    c.execute("DELETE FROM poznamky WHERE rowid=?", (poznamka_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/uprav/<int:poznamka_id>', methods=['GET', 'POST'])
def uprav_poznamku(poznamka_id):      
    conn = sqlite3.connect(databaze)
    c = conn.cursor()    
    c.execute("SELECT poznamka, vlozeno, dulezitost FROM poznamky WHERE rowid=?", (poznamka_id,))    
    poznamka_tuple = c.fetchone()
    conn.close()    
    form = PoznamkaForm(poznamka=poznamka_tuple[0])
    poznamka_text = form.poznamka.data
    if form.validate_on_submit():
        conn = sqlite3.connect(databaze)
        c = conn.cursor()        
        c.execute("UPDATE poznamky SET poznamka=? WHERE rowid=?", (poznamka_text, poznamka_id,))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('formular.html', form=form)

if __name__ == '__main__':
    app.run()