import yfinance as yf
from datetime import datetime,time
import streamlit as st

# Définir le symbole de l'action (ticker)
x_code_valeur = "DE0007030009" # rheinmetal"'IT0003856405' # LEONARDO
#x_code_valeur = "NVDA"
#x_code_valeur = "FR0000120404"   #ACCOR
#x_code_valeur = "US67066G1040" #NVIDIA
#x_code_valeur = "ES0144580Y14"   # "ES0144580Y14" iberdrola
#x_code_valeur = 'FR0000121014'  #LVMH

#DEFINIR UN BEAU TITRE
st.title("📈 Mon Application Boursière 11:11")

#SAISIR UNE VALEUR
#ticker = st.text_input("Entrez un ticker", "AAPL")
ticker = x_code_valeur

if ticker:
    stock = yf.Ticker(ticker)
    info = stock.info
    st.write("Nom complet :", info.get("longName"))
    st.write("Prix actuel :", info.get("currentPrice"))
else:
    print("Le Ticher ,'a pas été trouvé",ticker)

#Extraction d’historique avec Ticker.history EN DEUX LIGNES C EST MIEUX
x_indice = yf.Ticker(x_code_valeur)
x_close = x_indice.history(start="2025-05-01")['Close']

print("mon xclose",x_close)


