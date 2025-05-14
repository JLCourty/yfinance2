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
st.title("📈 Mon Application Boursière 11:36")


def get_ticker(p_ticker):
    if p_ticker:
        stock = yf.Ticker(p_ticker)
        info = stock.info
        t_longname = info.get("longName")
        t_prix = info.get("currentPrice")
        st.write("Nom complet :", t_longname,t_prix)

    #st.write("Nom complet :", info.get("longName"))
    #st.write("Prix actuel :", info.get("currentPrice"))
    #print(ticker,t_longname,t_prix)
    else:
        print("Le Ticker ,'a pas été trouvé",ticker)


#SAISIR UNE VALEUR
#ticker = x_code_valeur
get_ticker("FR0000120404")
get_ticker("US67066G1040")
