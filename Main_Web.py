import yfinance as yf
import streamlit as st
import pandas as pd


#DEFINIR UNE LISTE
liste_donnees = []

# Date du jour
date_jour = pd.Timestamp.today()
x_date_jour = date_jour.strftime("%d/%m/%Y")

#CREER LES TICKERS DES COURS DU DOLLAR  PLNTAGE MARDI
usd_eur_data = yf.Ticker("EURUSD=X")
x_cours_dollar = round(usd_eur_data.history(period="1d")["Close"].iloc[-1],4)

#FONCTION DE FORMATAGE UN MONTANT EN EUROS SANS DECIMALES
def format_euro(num_brut):
    num_brut = str("{:,.2f}".format(int(num_brut)).replace(',',' '))
    num_brut = num_brut.replace('.00',' ')
    return num_brut + "€"

#FONCTION DE FORMATAGE UN MONTANT EN POURCENTAGE
def format_pc(t_P1,t_P2):
    return str(    round((t_P1-t_P2)/t_P2*100,2 )  ) + " %"

#MA FONCTION GET TOUT
def Get_tout(x_code_valeur, x_nom_valeur, x_date_jour, x_qte, x_currency):

    if x_code_valeur:

        x_ticker = yf.Ticker(x_code_valeur)
        data = x_ticker.history(start="2025-05-11")['Close']

        #EXTRAIRE LES DONNEES DU TICKER
        t_date_jour = data.index[-1]
        t_prix = data.iloc[-1]
        t_ouverture = data.iloc[-2]

        if x_date_jour == t_date_jour:
            x_date_jour = "OK"
            Progression = (t_prix - t_ouverture) * x_qte
        else:
            x_date_jour = "Hier"
            Progression = 0

        total_prix = t_prix * x_qte / x_currency

        #AJOUTER UNE LIGNE A LA LISTE
        liste_donnees.append([  x_date_jour , x_nom_valeur, round(total_prix) , round(Progression)  ])   #

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
Get_tout('DE0007030009','RHEINMETALL',    x_date_jour,5   ,1)
Get_tout('US79466L3024','SALESFORCE',     x_date_jour,46  , x_cours_dollar)
Get_tout('FR0000121329','THALES',         x_date_jour,24  ,1)
Get_tout('FR0000120271','TOTAL ENERGIES', x_date_jour,111 ,1)
Get_tout('US92826C8394','VISA',           x_date_jour,40  , x_cours_dollar)
Get_tout('FR0007054358','ETF STOXX 50',   x_date_jour,1543,1)
Get_tout('FR0010315770','ETF MSCI' ,      x_date_jour,305 ,1)
Get_tout('LU1829221024','ETF NASDAQ',     x_date_jour,130 ,1)

#DEFINIR LES TITRES DES COLONNES
columns = ["Date", "Valeur", "Montant", "Progression"]

#CREE LE TABLEAU AVEC LIGNES ET COLONNES CHARGEES PRECEDEMMENT
df = pd.DataFrame(liste_donnees, columns=columns)

#A SUPPRIMER
df["Progression"] = df["Progression"].astype(str).str.replace(",", ".").astype(int)
df["Progression"] = df["Progression"].astype(str).str.replace(",", ".").astype(int)

#TRIER LE TABLEAU SUR LA PROGRESSION
df_sorted = df.sort_values(by="Progression", ascending=False).reset_index(drop=True)

#CALCULER LES TOTAUX
total_prix = df["Montant"].sum()
total_prog = df["Progression"].sum()


st.markdown(
    f"<p style='margin-top: 0; margin-bottom: 5px; font-size: 24px;'><strong>Total :</strong> {format_euro(total_prix + 131619)} &nbsp;&nbsp; <strong>Gains :</strong> {format_euro(total_prog)}</p>",
    unsafe_allow_html=True
)

#AFFICHER LES TOTAUX
#if total_prog > 0:
#    st.markdown("### Total : " + format_euro(total_prix + 131619) + " Gains : " + format_euro(total_prog))   #+"   -"+x_date_jour+"-"
#else:
#    st.markdown("### Total : " + format_euro(total_prix + 131619) + " Pertes : " + format_euro(total_prog)+"   -"+x_date_jour)

#CREATION DU TABLEAU HTML
def df_to_html(df):

    #FORMATAGE GENERAL DU TABLEAU
    html = "<table style='width:100%; border-collapse: collapse;'>"

    #ECRITURE DES ENTETES
    html += "<thead><tr>"
    for col in df.columns:
        html += f"<th style='border: 1px solid #ccc; padding: 4px; background-color: #f0f0f0; font-weight: bold;'>{col}</th>"
    html += "</tr></thead><tbody>"

    #ECRITURE DES LIGNES
    for _, row in df.iterrows():

        html += "<tr>"

        for col in df.columns:
            val = row[col]
            style = "font-weight: bold;"

            #ALIGNER LES VALEURS NUMERIQUES A DROITE
            if col in ["Montant", "Progression"]: style += " text-align: right;"

            #AFFICHER EN COULEUR CONDITIONNELLE
            if col == "Progression": style += "color: green;" if val >= 0 else "color: red;"

            # FORMATTER LE MONTANT
            if col == "Montant":
                val = format_euro(val)

            # FORMATTER LA PROGRESSION
            if col == "Progression":
                val = f"{val:,.2f} %"

            html += f"<td style='border: 1px solid #ccc; padding: 4px; {style}'>{val}</td>"
        html += "</tr>"

#   FIN DE LA FOCTION HTML
    html += "</tbody></table>"
    return html

# Affichage HTML
st.markdown(df_to_html(df_sorted), unsafe_allow_html=True)
