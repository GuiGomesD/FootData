import requests
import sqlite3

API_KEY = '9e63fddbcd4560f1d099d51b934606fd'
API_URL = 'https://v3.football.api-sports.io/'

headers = {
    'x-apisports-key': API_KEY
}

def get_match_data(league_id, season):
    url = f'{API_URL}fixtures?league={league_id}&season={season}'
    response = requests.get(url, headers=headers)
    match_data = response.json()
    
    print("Response JSON:", match_data)

    if 'response' in match_data:  #Verifica se a chave 'response' existe
        detailed_matches = []
        for match in match_data['response']:
            #Extrai os dados conforme a estrutura correta
            home_team = match['teams']['home']['name']
            away_team = match['teams']['away']['name']
            score = f"{match['goals']['home']}-{match['goals']['away']}"
            stadium = match['fixture']['venue']['name']
            date = match['fixture']['date']
            referee = match.get('fixture', {}).get('referee', 'N/A')
            yellow_cards = match.get('cards', {}).get('yellow', 0)
            red_cards = match.get('cards', {}).get('red', 0)

            detailed_matches.append({
                'home_team': home_team,
                'away_team': away_team,
                'score': score,
                'stadium': stadium,
                'date': date,
                'referee': referee,
                'yellow_cards': yellow_cards,
                'red_cards': red_cards,
            })

        return detailed_matches
    else:
        print("Nenhum dado de partidas encontrado.")
        return []  #Retorna uma lista vazia se não houver dados

def save_to_database(matches):
    conn = sqlite3.connect('football_data.db')
    c = conn.cursor()

    #Criação da tabela de partidas
    c.execute('''CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY,
        home_team TEXT,
        away_team TEXT,
        score TEXT,
        stadium TEXT,
        date TEXT,
        referee TEXT,
        yellow_cards INTEGER,
        red_cards INTEGER
    )''')

    #Limpar dados antigos para evitar duplicações em execuções futuras
    c.execute("DELETE FROM matches")

    for match in matches:
        home_team = match['home_team']
        away_team = match['away_team']
        score = match['score']
        stadium = match['stadium']
        date = match['date']
        referee = match['referee']
        yellow_cards = match['yellow_cards']
        red_cards = match['red_cards']

        c.execute('''INSERT INTO matches (home_team, away_team, score, stadium, date, referee, yellow_cards, red_cards) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (home_team, away_team, score, stadium, date, referee, yellow_cards, red_cards))

    conn.commit()
    conn.close()

def check_data_in_database():
    conn = sqlite3.connect('football_data.db')
    c = conn.cursor()

    c.execute("SELECT * FROM matches")
    rows = c.fetchall()
    
    for row in rows:
        print(row)  #Isso irá imprimir todas as colunas da tabela

    conn.close()

if __name__ == '__main__':
    league_id = 39  #Premier League, por exemplo
    season = 2022  #Ano da temporada
    match_data = get_match_data(league_id, season)
    
    if match_data:  #Verifica se há dados de partidas
        save_to_database(match_data)
        check_data_in_database()  #Chama a função para verificar os dados
    else:
        print("Nenhum dado de partidas encontrado.")
