import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import yfinance as yf

#DEFINIR LES RESERVES
t_reserves = 132846

# Rafraîchir automatiquement toutes les 60 secondes
st_autorefresh(interval=60000, key="refresh")

# Fonction de formatage
def format_euro(num_brut):
    num_brut = str("{:,.2f}".format(int(num_brut)).replace(',', ' '))
    num_brut = num_brut.replace('.00', ' ')
    return num_brut + "€"

# Fonction principale d'affichage
def afficher_tableau():
    liste_donnees = []

    # Date et heure actuelles
    date_jour = pd.Timestamp.today()
    x_date_jour = date_jour.strftime("%d/%m/%Y")
    t_heure_actuelle = pd.Timestamp.now(tz='Europe/Paris').strftime('%H:%M')

    # Cours USD
    usd_eur_data = yf.Ticker("EURUSD=X")
    x_cours_dollar = round(usd_eur_data.history(period="1d")["Close"].iloc[-1], 4)

    # Fonction pour chaque ligne
    def Get_tout(x_code_valeur, x_nom_valeur, x_date_jour, x_qte, x_currency):
        if x_code_valeur:
            x_ticker = yf.Ticker(x_code_valeur)
            data = x_ticker.history(start="2025-05-11")['Close']
            t_date_jour = data.index[-1].strftime("%d/%m/%Y")
            t_prix = data.iloc[-1]
            t_ouverture = data.iloc[-2]

            if x_date_jour == t_date_jour:
                label_date = ""
                progression = (t_prix - t_ouverture) * x_qte
            else:
                label_date = "Hier"
                progression = (t_prix - t_ouverture) * x_qte  #0

            total_prix = t_prix * x_qte / x_currency
            liste_donnees.append([label_date, x_nom_valeur, round(total_prix), round(progression)])
        else:
            st.warning(f"Le ticker n’a pas été trouvé : {x_code_valeur}")

    # Appels aux tickers
    Get_tout('FR0000120404','ACCOR',          x_date_jour ,214 ,1)
    Get_tout('NL0000235190','AIRBUS',         x_date_jour ,95  ,1)
    Get_tout('GOOGL',       'ALPHABET',       x_date_jour,79   , x_cours_dollar)
    Get_tout('US0231351067','AMAZON',         x_date_jour,52   , x_cours_dollar)
    Get_tout('NL0010273215','ASML',           x_date_jour ,18  ,1)
    Get_tout('US11135F1012','BROADCOM',       x_date_jour,73   , x_cours_dollar)
    Get_tout('DE0005810055','DEUTSCHE BORSE', x_date_jour,42   ,1)
    Get_tout('FR0000052292','HERMES',         x_date_jour,4    ,1)
    Get_tout('ES0144580Y14','IBERDROLA',      x_date_jour,712  ,1)
    Get_tout('IT0003856405','LEONARDO',       x_date_jour,142  , 1)
    Get_tout('US5949181045','MICROSOFT',      x_date_jour ,48  , x_cours_dollar)
    Get_tout('US64110L1061','NETFLIX',        x_date_jour ,10  , x_cours_dollar)
    Get_tout('US67066G1040','NVDIA',          x_date_jour,160  , x_cours_dollar)
    Get_tout('US6974351057','PALO ALTO',      x_date_jour,56   , x_cours_dollar)
    Get_tout('DE0007030009','RHEINMETALL',    x_date_jour,5    ,1)
    Get_tout('US79466L3024','SALESFORCE',     x_date_jour,46   , x_cours_dollar)
    Get_tout('FR0000121329','THALES',         x_date_jour,24   ,1)
    Get_tout('FR0000120271','TOTAL ENERGIES', x_date_jour,111  ,1)
    Get_tout('US92826C8394','VISA',           x_date_jour,40   , x_cours_dollar)
    Get_tout('FR0007054358','ETF STOXX 50',   x_date_jour,1543 ,1)
    Get_tout('FR0010315770','ETF MSCI' ,      x_date_jour,305  ,1)
    Get_tout('LU1829221024','ETF NASDAQ',     x_date_jour,130  ,1)

    # Création DataFrame
    df = pd.DataFrame(liste_donnees, columns=["Date", "Valeur", "Montant", "Progression"])
    df["Progression"] = df["Progression"].astype(str).str.replace(",", ".").astype(int)
    df_sorted = df.sort_values(by="Progression", ascending=False).reset_index(drop=True)

    #CALCUL DES TOTAUX
    total_prix = df["Montant"].sum()
    total_prog = df["Progression"].sum()

    #AFFICHAGE DES TOTAUX
    if total_prog > 0:
        st.markdown(
            f"<p style='margin-top: 0; margin-bottom: 5px; font-size: 24px;'>"
            f"<strong>Total :</strong>          {format_euro(total_prix + t_reserves)} &nbsp;&nbsp;"
            f"<strong> <span style='color: green;'> Gains : +{format_euro(total_prog)  }   </strong>       "
            f"</p>"
            f"<p style='margin-top: 10px; margin-bottom: 5px; font-size: 16px;'>"
            f"Le {x_date_jour} à {t_heure_actuelle} " f"</p>",
            unsafe_allow_html=True)

    else:
        st.markdown(f"### Total : {format_euro(total_prix + t_reserves)} - <span style='color: red;'>Pertes : {format_euro(total_prog)} - {x_date_jour} - {t_heure_actuelle}")

    # Affichage tableau
    def df_to_html(df):
        html = "<table style='width:100%; border-collapse: collapse;'>"
        html += "<thead><tr>"
        for col in df.columns:
            html += f"<th style='border: 1px solid #ccc; padding: 4px; background-color: #f0f0f0; font-weight: bold;'>{col}</th>"
        html += "</tr></thead><tbody>"
        for _, row in df.iterrows():
            html += "<tr>"
            for col in df.columns:
                val = row[col]
                style = "font-weight: bold;"
                if col in ["Montant", "Progression"]: style += " text-align: right;"
                if col == "Montant":  val = format_euro(val)
                if col == "Progression":
                    style += "color: green;" if val > 0 else "color: red;"
                    val = f"{val:,.2f} €"
                html += f"<td style='border: 1px solid #ccc; padding: 4px; {style}'>{val}</td>"
            html += "</tr>"
        html += "</tbody></table>"
        return html

    st.markdown(df_to_html(df_sorted), unsafe_allow_html=True)

# ⏬ Appel de la fonction principale
afficher_tableau()
