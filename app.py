from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="booking.db",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)