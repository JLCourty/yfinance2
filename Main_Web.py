import streamlit as st
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import JsCode
from streamlit_autorefresh import st_autorefresh
import yfinance as yf

# 🔹 Réserves initiales
t_reserves = 52635 + 43652

#FORMAT NUMERIQUE EN EUROS
def format_euro(val):
    return f"{val:,.2f} €".replace(",", " ").replace(".", ",")

# 🔹 Date et heure actuelles
date_jour = pd.Timestamp.today()
x_date_jour = datetime.now().strftime("%d/%m/%Y")
t_heure_actuelle = datetime.now().strftime("%H:%M")

# 🔹 Données USD/EUR
usd_eur_data = yf.Ticker("EURUSD=X")
x_cours_dollar = round(usd_eur_data.history(period="1d")["Close"].iloc[-1], 4)

# 🔹 Liste de données à remplir
liste_donnees = []

# 🔹 Fonction principale
def Get_tout(x_code_valeur, x_nom_valeur, x_date_jour, x_qte, x_currency):

    if x_code_valeur:
        x_ticker = yf.Ticker(x_code_valeur)
        data = x_ticker.history(start="2025-05-11")['Close']
        if data.empty:
            st.warning(f"Données absentes pour {x_code_valeur}")
            return

        t_date_jour = data.index[-1].strftime("%d/%m/%Y")
        t_prix = data.iloc[-1]
        t_ouverture = data.iloc[-2]

        label_date = "" if x_date_jour == t_date_jour else "Hier"

        if not label_date != "Hier":
            progression = (t_prix - t_ouverture) * x_qte
            variation_pct = ((t_prix - t_ouverture) / t_ouverture) * 100
        else:
            progression = (t_prix - t_ouverture) * x_qte
            variation_pct = ((t_prix - t_ouverture) / t_ouverture) * 100

        total_prix = t_prix * x_qte / x_currency

        #CHARGER LE TABLEAU AVEC LES COLONNES TELLES QU'ELLES SERONT AFFICHEES
        liste_donnees.append([label_date,x_nom_valeur,round(total_prix,2), round(progression,2), round(variation_pct,2)   ])

# 🔹 Portefeuille (code, nom, quantité, devise)
valeurs = [
    ('FR0000120404', 'ACCOR', 214, 1),
    ('NL0000235190', 'AIRBUS', 95, 1),
    ('GOOGL',        'ALPHABET', 79, x_cours_dollar),
    ('US0231351067', 'AMAZON', 52, x_cours_dollar),
    ('NL0010273215', 'ASML', 18, 1),
    ('NL0010273215', 'ASML (2)', 3, 1),
    ('FR0000131104', 'BNP (2)',  28   ,1) ,  # JUIN 2025
    ('US11135F1012', 'BROADCOM', 73, x_cours_dollar),
    ('FR0000121667', 'ESSILOR LUXOTICA'        ,34 ,1)  ,
    ('DE0005810055', 'DEUTSCHE BORSE', 42, 1),
    ('FR0000052292', 'HERMES', 4, 1),
    ('ES0144580Y14', 'IBERDROLA', 712, 1),
    ('IT0003856405', 'LEONARDO', 142, 1),
    ('US5949181045', 'MICROSOFT', 48, x_cours_dollar),
    ('US64110L1061', 'NETFLIX', 10, x_cours_dollar),
    ('US67066G1040', 'NVDIA', 160, x_cours_dollar),
    ('US6974351057', 'PALO ALTO', 56, x_cours_dollar),
    ('DE0007030009', 'RHEINMETALL', 10, 1),
    ('US79466L3024', 'SALESFORCE', 46, x_cours_dollar),
    ('DE0007164600', 'SAP '   ,34 ,1)  ,
    ('DE0007164600', 'SAP (2)', 8, 1),
    ('FR0000121329', 'THALES', 24, 1),
    ('FR0000120271', 'TOTAL ENERGIES', 111, 1),
    ('US92826C8394', 'VISA',            40, x_cours_dollar),
    ('FR0007054358', 'ETF STOXX 50', 1543, 1),
    ('FR0010315770', 'ETF MSCI', 305, 1),
    ('LU1829221024', 'ETF NASDAQ', 130, 1) ]

#CHARGEMENT DES DONNES
for code, nom, qte, devise in valeurs:
    Get_tout(code, nom, x_date_jour, qte, devise)

#CALCULS DIVERS
df = pd.DataFrame(    liste_donnees,    columns=["Date", "Valeur", "Montant", "Progression",  "Variation"])


df["Progression"] = df["Progression"].astype(str).str.replace(",", ".").astype(float)
df["Montant"] = df["Montant"].astype(float)

#TRI
df_sorted = df.sort_values(by="Progression", ascending=False).reset_index(drop=True)   # EN EUROS
df_sorted = df.sort_values(by="Variation", ascending=False).reset_index(drop=True)    # EN PC


#TOTALISER LES 2 INFOS
total_prix = df["Montant"].sum()
total_prog = df[df["Date"] != "Hier"]["Progression"].sum()

#AFFICHER LE TITRE DES GAINS
if total_prog > 0:
    st.markdown(
        f"<div style='margin: 0; padding: 0;'>"
        f"<p style='margin: 0; font-size: 20px;'>"
        f"<strong>📊 Total : {format_euro(total_prix + t_reserves)} &nbsp;&nbsp; "
        f"<span style='color: green;'>- Gains : +{format_euro(total_prog)}</span>"
        f"</p>"
        f"<p style='margin: 0; font-size: 16px;'>"
        f"Le {x_date_jour} à {t_heure_actuelle}</p>"
        f"</div>",
        unsafe_allow_html=True    )







#TITRES DES PERTES
else:

    st.markdown(
        f"<p style='margin-top: 0; margin-bottom: 5px; font-size: 36px;'>"
        f"<strong><span style='color: blue;'>📊 Total : {format_euro(total_prix + t_reserves)} &nbsp;"
        f"<strong><span style='color: red;'>- Pertes : {format_euro(total_prog)} &nbsp; "
        f"</p><p style='margin-top: 10px; font-size: 16px;'>"
        f"Le {x_date_jour} à {t_heure_actuelle}</p>",
        unsafe_allow_html=True)


#COULEUR DES RUBRIQUES NUMERIQUES DANS LA LISTE
cell_style_js = JsCode("""
function(params) {
    if (params.data && params.data.Date === "Hier") {
        return { color: 'Orange', fontWeight: 'bold' };    }
    if (params.value > 0) {
        return { color: 'green', fontWeight: 'bold' };
    } else if (params.value < 0) {
        return { color: 'red', fontWeight: 'bold' };    }
    return null;} """)

# 🔹 Configuration AgGrid
gb = GridOptionsBuilder.from_dataframe(df_sorted)
gb.configure_selection("single", use_checkbox=False)
gb.configure_column("Montant", type=["numericColumn"],valueFormatter="x.toLocaleString('fr-FR', {style: 'currency', currency: 'EUR'})")
gb.configure_column("Progression", cellStyle=cell_style_js)
gb.configure_column("Variation (%)", cellStyle=cell_style_js)
grid_options = gb.build()

# 🔄 Rafraîchissement automatique
st_autorefresh(interval=60000, key="refresh")

# 🔢 Calcul dynamique de la hauteur : 35 pixels par ligne environ + marge
hauteur_ligne = 33
marge =20
hauteur_totale = len(df_sorted) * hauteur_ligne  + marge

grid_response = AgGrid(
    df_sorted,
    gridOptions=grid_options,
    height=hauteur_totale,
    fit_columns_on_grid_load=True,
    enable_enterprise_modules=False,
    update_mode='SELECTION_CHANGED',
    allow_unsafe_jscode=True,)

# 🔹 Affichage ligne sélectionnée
selected = grid_response["selected_rows"]
if isinstance(selected, list) and selected:
    ligne = selected[0]
    st.markdown("### ✅ Ligne sélectionnée")
    st.json(ligne)

# 🔹 Préparer le DataFrame pour export : trié par Valeur, sans la colonne Date
df_export = df_sorted.drop(columns=["Date"]).sort_values(by="Valeur")

# 📤 Téléchargement CSV
csv = df_export.to_csv(index=False, sep=';').encode('utf-8-sig')
st.download_button(
    label="📥 Télécharger le tableau (.csv)",
    data=csv,
    file_name="portefeuille.csv",
    mime="text/csv")