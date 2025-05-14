import yfinance as yf
from datetime import datetime,time

# Définir le symbole de l'action (ticker)
x_code_valeur = 'FR0000121014'  #LVMH


x_code_valeur = "DE0007030009" # rheinmetal"'IT0003856405' # LEONARDO
#x_code_valeur = "NVDA"
#x_code_valeur = "FR0000120404"   #ACCOR
#x_code_valeur = "US67066G1040" #NVIDIA
#x_code_valeur = "ES0144580Y14"   # "ES0144580Y14" iberdrola

import streamlit as st
#import yfinance as yf

st.title("📈 Application Boursière")

ticker = st.text_input("Entrez un ticker", "AAPL")

if ticker:
    stock = yf.Ticker(ticker)
    info = stock.info
    st.write("Nom complet :", info.get("longName"))
    st.write("Prix actuel :", info.get("currentPrice"))

#x_currency = 1.03

#Gestion des dates et heures *********************
#*************************************************

# LA DATE DU JOUR ET LE PREMIER JOUR DU MOIS
x_date = datetime.today()                       #NON RECOUPEE A 10
debut_mois = x_date.replace(day=1)              #NON RECOUPEE A 10
print("Aujourd’hui", str(x_date )[00:10]   ,"Début de mois"         ,   str(debut_mois )[00:10]   )

# DATES DU JOUR ET DE LA VEILLE
x_date   = str(datetime.now())[00:10]         # RECOUPEE A 10
x_heure  = str(datetime.now())[11:16]         # RECOUPEE A 10
#print("Date",x_date,"Heure",x_heure)

#Extraction d’historique avec Ticker.history EN DEUX LIGNES C EST MIEUX
x_indice = yf.Ticker(x_code_valeur)
x_close = x_indice.history(start=debut_mois)['Close']


""
#Extraction d’historique avec DOWNLOAD ******************
#********************************************************

# Télécharger les données historiques avec la commande DOWNLOAD
data = yf.download(x_code_valeur,start='2025-04-20',end=x_date)   #'2025-01-28')
print("Avec Download",data)

#Sélectionner les colonnes d'intérêt
columns_of_interest = ['Open', 'Close']
ticker_data_filtered = data[columns_of_interest]

#INSERTION DES DONNEES DANS LA TABLE
for row in ticker_data_filtered.itertuples(index=False, name=None):
    open = row[0]   #PAS DU TOUT LA DATE
    close = row[1]
    print("Streamlit",x_code_valeur,open,close)
