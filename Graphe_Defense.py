#OUVRIR LES LIBRAIRIES
import sqlite3
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


#DEFINIR LE NB DE JOURS D'HISTORIQUE
T_nb_jours = 20   # 285 # 13 octobre

#CALCULER LA DATE DE DEBUT
end_date = datetime.now()
start_date = end_date - timedelta(days=T_nb_jours)

#CONNEXION A LA BASE DE DONNEES
conn = sqlite3.connect('ma_base_de_valeurs.db')
cursor = conn.cursor()

#VIDER LA TABLE DES VALEURS
cursor.execute('DELETE FROM Historique')

#FONCTION DE CHARGEMENT DE 3 MOIS D'HISTORIQUE
def load_histo(code_valeur,Nom_Valeur,coef_1000,Off_set):

#   TELECHARGER LES DONNEES d historique POUR CETTE VALEUR
    ticker_data = yf.download(code_valeur, start=start_date, end=end_date)
    ticker_data.reset_index(inplace=True)  # Réinitialise l'index et ajoute "Date" comme colonne

#   Sélectionner les colonnes d'intérêt
    columns_of_interest = ['Date','Open','Close']
    ticker_data_filtered = ticker_data[columns_of_interest]

#   INSERTION DES DONNEES DANS LA TABLE HISTORIQUE
    for row in ticker_data_filtered.itertuples(index=False, name=None):
        date = str(row[0])[00:10]
        close_price = (row[2] - Off_set) / Off_set * 100
        cursor.execute(''' INSERT INTO Historique ( Nom_Valeur,Date,Close) VALUES (?,?,?) ''', (Nom_Valeur, date, round( (close_price) - 0 ,0 )  ))

#VALEURS
#load_histo('FR0000120404',"ACCOR",             1,47.11)     #OFF SET CONTIENT LE COURS AU 1ER JANVIER 2025
#load_histo('NVDA',        "NVIDIA",            1,135.93)
#load_histo('TSLA',        "TSLA - Musk",       1,390.12)
#load_histo('META',        "Meta - Zuckenberg", 1,589.60)
#load_histo('US0231351067',"AMAZON",    1,222.45)
#load_histo('DJT',         "DJT - Trump",       1,31.61)

load_histo('FR0000121329',"THALES",            1,136.6)
load_histo('DE0007030009',"RHEINMETALL",            1,604.6)
load_histo('IT0003856405',"LEONARDO",            1,26.06)
load_histo('FR0014004L86',"DASSAULT AV",            1,195.6)

#ENREGISTRER LES LIGNES IMPORTEES
conn.commit()

# Récupération des données
cursor.execute('SELECT Nom_Valeur, date, close FROM Historique')
rows = cursor.fetchall()

# Fermeture de la connexion
conn.close()

# Transformation des données pour le tracé
data = {}
for nom_valeur, date, close in rows:
    date = datetime.strptime(date, "%Y-%m-%d")  # Conversion en format datetime
    if nom_valeur not in data:
        data[nom_valeur] = {"dates": [], "closes": []}
    data[nom_valeur]["dates"].append(date)
    data[nom_valeur]["closes"].append(close)

# Tracé du graphique
plt.figure(figsize=(12, 6))
for nom_valeur, values in data.items():
    plt.plot(values["dates"], values["closes"], marker='o', label=nom_valeur)

# Formatage du graphique
plt.xlabel("Date")
plt.ylabel("Prix de clôture")
plt.title("Évolution des prix de clôture des actions")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

# Affichage du graphique
plt.show()




