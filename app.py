from flask import Flask, render_template
import sqlite3
from datetime import datetime
from dateutil import parser
import os

app = Flask(__name__)

def get_matches_from_db():
    conn = sqlite3.connect('football_data.db')
    c = conn.cursor()
    c.execute("SELECT home_team, away_team, score, stadium, date, referee, yellow_cards, red_cards FROM matches")
    matches = c.fetchall()
    conn.close()
    
    formatted_matches = []
    for match in matches:
        home_team, away_team, score, stadium, date_str, referee, yellow_cards, red_cards = match
        
        # Usando dateutil.parser para analisar a data
        date = parser.isoparse(date_str)  # Analisa a string no formato ISO 8601
        formatted_date = date.strftime('%d/%m/%Y %H:%M')  # Exemplo: 21/10/2022 15:00
        formatted_matches.append((home_team, away_team, score, stadium, formatted_date, referee, yellow_cards, red_cards))
    
    return formatted_matches

@app.route('/')
def index():
    matches = get_matches_from_db()
    print("Dados recebidos:", matches)
    if not matches:
        print("Nenhum dado de partidas encontrado.")
    return render_template('index.html', matches=matches)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Obtém a porta do ambiente ou usa 5000 como padrão
    app.run(host='0.0.0.0', port=port, debug=True)
