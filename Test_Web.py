import yfinance as yf
from datetime import datetime,time
import streamlit as st


x_date_jour="2025-05-14"
x_cours_dollar = 1.131


# Définir le symbole de l'action (ticker)
#x_code_valeur = "DE0007030009" # rheinmetal"'IT0003856405' # LEONARDO
#x_code_valeur = "NVDA"
#x_code_valeur = "FR0000120404"   #ACCOR
#x_code_valeur = "US67066G1040" #NVIDIA
#x_code_valeur = "ES0144580Y14"   # "ES0144580Y14" iberdrola
#x_code_valeur = 'FR0000121014'  #LVMH

#DEFINIR UN BEAU TITRE
st.title("📈 Mon Application Boursière 12:36")


#def get_tout(p_ticker):
def Get_tout(x_code_valeur, x_nom_valeur, x_date_jour, x_cours_1janv, x_cours_1mai, cours_31dec, mt_31dec, x_qte, x_currency):

    #x_date_jour = "2025-05-14"



    if x_code_valeur:
        stock = yf.Ticker(px_code_valeur)
        info = stock.info
        #t_longname = info.get("longName")
        t_prix = info.get("currentPrice")
        st.write(x_date_jour, x_nom_valeur,t_prix ,  x_cours_1janv, x_cours_1mai, cours_31dec, mt_31dec, x_qte, x_currency)
    else:
        print("Le Ticker ,'a pas été trouvé",ticker)

#LANCER LA FONCTION UNIQUE
Get_tout('FR0000120404','ACCOR',          x_date_jour,47.39  ,43.15  ,55, 12000 ,214 ,1)
Get_tout('NL0000235190','AIRBUS',         x_date_jour,154.78 ,147.14 ,55, 19000 ,95  ,1)
Get_tout('GOOGL'       ,'ALPHABET',       x_date_jour,182.86 ,140.52 ,55, 15000 ,79  , x_cours_dollar)
Get_tout('US0231351067','AMAZON',         x_date_jour,211.93 ,163.19 ,55, 12000 ,52  , x_cours_dollar)
Get_tout('NL0010273215','ASML',           x_date_jour,678.7  ,582.51 ,55, 15000 ,18  ,1)
Get_tout('US11135F1012','BROADCOM',       x_date_jour,223.96 ,170.31 ,55, 18000 ,73  , x_cours_dollar)
Get_tout('DE0005810055','DEUTSCHE BORSE', x_date_jour,223.60 ,283.51 ,55, 14000 ,42  ,1)
Get_tout('FR0000052292','HERMES',         x_date_jour,2409.60,2391.01,55, 12000 ,4   ,1)
Get_tout('ES0144580Y14','IBERDROLA',      x_date_jour,13.58  ,15.87  ,55, 13000 ,712 ,1)
Get_tout('IT0003856405','LEONARDO',       x_date_jour,49.69  ,45.81  ,55, 8000 ,142  , 1)
Get_tout('US5949181045','MICROSOFT',      x_date_jour,407.17 ,349.76 ,55, 25000 ,48  , x_cours_dollar)
Get_tout('US64110L1061','NETFLIX',        x_date_jour,820.01 ,1001.43,55, 12000 ,10  , x_cours_dollar)
Get_tout('US67066G1040','NVDIA',          x_date_jour,133.31 ,96.38  ,55, 22000 ,160 , x_cours_dollar)
Get_tout('US6974351057','PALO ALTO',      x_date_jour,191.02 ,165.41 ,55, 11000 ,56  , x_cours_dollar)
Get_tout('DE0007030009','RHEINMETALL',    x_date_jour,1196.01,1499.01,55, 12000 ,5   ,1)
Get_tout('US79466L3024','SALESFORCE',     x_date_jour,322.96 ,237.00 ,55, 14000 ,46  , x_cours_dollar)
Get_tout('FR0000121329','THALES',         x_date_jour,262.93 ,244.90 ,55, 7000 ,24  ,1)
Get_tout('FR0000120271','TOTAL ENERGIES', x_date_jour,53.37  ,51.16  ,55, 7000  ,111 ,1)
Get_tout('US92826C8394','VISA',           x_date_jour,305.29 ,305.73 ,55, 14000 ,40  , x_cours_dollar)
Get_tout('-',           '_ A ----------', x_date_jour,0      ,150    ,55, 0     ,0   ,1)
Get_tout('FR0007054358','_ETF STOXX 50',  x_date_jour,53.33  ,56.41  ,55, 105000,1543,1)
Get_tout('FR0010315770','_ ETF MSCI' ,    x_date_jour,359.41 ,318.64 ,55, 112000,305 ,1)      #VALEUR US FOURNIE EN EUROS
Get_tout('LU1829221024','_ ETF NASDAQ',   x_date_jour,82.73  ,69.06  ,55, 12000 ,130 ,1)      #VALEUR US FOURNIE EN EUROS