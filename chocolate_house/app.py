from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

def create_tables():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS SeasonalFlavors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flavor_name TEXT NOT NULL,
            description TEXT,
            available_until DATE
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient_name TEXT NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flavor_name TEXT NOT NULL,
            customer_name TEXT,
            allergy_info TEXT
        )
    ''')

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('chocolate_house.db')
    conn.row_factory = sqlite3.Row 
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flavors', methods=['GET', 'POST'])
def view_flavors():
    conn = get_db_connection()
    if request.method == 'POST':
        flavor_name = request.form['flavor_name']
        description = request.form['description']
        available_until = request.form['available_until']
        
        conn.execute('INSERT INTO SeasonalFlavors (flavor_name, description, available_until) VALUES (?, ?, ?)',
                     (flavor_name, description, available_until))
        conn.commit()
        return redirect(url_for('view_flavors'))
    
    flavors = conn.execute('SELECT * FROM SeasonalFlavors').fetchall()
    conn.close()
    return render_template('flavors.html', flavors=flavors)

@app.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    conn = get_db_connection()
    if request.method == 'POST':
        ingredient_name = request.form['ingredient_name']
        stock = request.form['stock']
        conn.execute('INSERT INTO Ingredients (ingredient_name, stock) VALUES (?, ?)', 
                     (ingredient_name, stock))
        conn.commit()
    
    ingredients = conn.execute('SELECT * FROM Ingredients').fetchall()
    conn.close()
    return render_template('ingredients.html', ingredients=ingredients)

@app.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    conn = get_db_connection()
    if request.method == 'POST':
        flavor_name = request.form['flavor_name']
        customer_name = request.form['customer_name']
        allergy_info = request.form['allergy_info']
        conn.execute('INSERT INTO Suggestions (flavor_name, customer_name, allergy_info) VALUES (?, ?, ?)', 
                     (flavor_name, customer_name, allergy_info))
        conn.commit()
    
    suggestions = conn.execute('SELECT * FROM Suggestions').fetchall()
    conn.close()
    return render_template('suggestions.html', suggestions=suggestions)

if __name__ == '__main__':
    create_tables()  # Ensure tables are created before running the app
    app.run(debug=True)
