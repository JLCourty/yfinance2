import yfinance as yf
import streamlit as st
import pandas as pd


# Liste globale pour stocker toutes les lignes
liste_donnees = []
x_date_jour="2025-05-14"
x_cours_dollar = 1.131

#DEFINIR UN BEAU TITRE
st.set_page_config(layout="wide")
#st.title("📈 Mon Application Boursière 12:36")

#MA FONCTION GET TOUT
def Get_tout(x_code_valeur, x_nom_valeur, x_date_jour, x_qte, x_currency):
    if x_code_valeur:
        stock = yf.Ticker(x_code_valeur)
        info = stock.info
        t_prix = info.get("currentPrice")
        t_ouverture = info.get("open")

        # Calcul de la variation journalière (%)
        if t_prix is not None and t_ouverture:
            variation_jour = ((t_prix - t_ouverture) / t_ouverture) * 100
        else:
            variation_jour = None  # ou 0 ou "N/A"

        # Ajouter une ligne à la liste globale
        liste_donnees.append([
            x_date_jour,
            x_nom_valeur,
            t_prix,
            variation_jour,         # ✅ Nouvelle colonne ajoutée ici
            x_qte,x_currency   ])
    else:
        st.warning(f"Le ticker n’a pas été trouvé : {x_code_valeur}")


#LANCER LA FONCTION UNIQUE
Get_tout('FR0000120404','ACCOR',          x_date_jour ,214 ,1)
Get_tout('NL0000235190','AIRBUS',         x_date_jour ,95  ,1)
Get_tout('GOOGL'       ,'ALPHABET',       x_date_jour,79  , x_cours_dollar)
Get_tout('US0231351067','AMAZON',         x_date_jour,52  , x_cours_dollar)
Get_tout('NL0010273215','ASML',           x_date_jour ,18  ,1)
Get_tout('US11135F1012','BROADCOM',       x_date_jour,73  , x_cours_dollar)
Get_tout('DE0005810055','DEUTSCHE BORSE', x_date_jour,42  ,1)
Get_tout('FR0000052292','HERMES',         x_date_jour,4   ,1)
Get_tout('ES0144580Y14','IBERDROLA',      x_date_jour,712 ,1)
Get_tout('IT0003856405','LEONARDO',       x_date_jour,142  , 1)
Get_tout('US5949181045','MICROSOFT',      x_date_jour ,48  , x_cours_dollar)
Get_tout('US64110L1061','NETFLIX',        x_date_jour ,10  , x_cours_dollar)
Get_tout('US67066G1040','NVDIA',          x_date_jour,160 , x_cours_dollar)
Get_tout('US6974351057','PALO ALTO',      x_date_jour,56  , x_cours_dollar)
Get_tout('DE0007030009','RHEINMETALL',    x_date_jour, 12000 ,5   ,1)
Get_tout('US79466L3024','SALESFORCE',     x_date_jour ,46  , x_cours_dollar)
Get_tout('FR0000121329','THALES',         x_date_jour, 7000 ,24  ,1)
Get_tout('FR0000120271','TOTAL ENERGIES', x_date_jour,  ,111 ,1)
Get_tout('US92826C8394','VISA',           x_date_jour,40  , x_cours_dollar)
Get_tout('FR0007054358','_ETF STOXX 50',  x_date_jour,1543,1)
Get_tout('FR0010315770','_ ETF MSCI' ,    x_date_jour,305 ,1)      #VALEUR US FOURNIE EN EUROS
Get_tout('LU1829221024','_ ETF NASDAQ',   x_date_jour,130 ,1)      #VALEUR US FOURNIE EN EUROS

# À la fin : convertir en DataFrame et afficher
columns = [ "Date", "Valeur", "Prix actuel", "variation_jour", "Quantité", "Devise"]
df = pd.DataFrame(liste_donnees, columns=columns)
st.table(df)