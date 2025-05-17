import streamlit as st
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import JsCode
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import yfinance as yf

#DEFINIR LES RESERVES
t_reserves = 132846

# 📌 Fonctions utilitaires
def format_euro(val):
    return f"{val:,.2f} €".replace(",", " ").replace(".", ",")

# 🔹 Variables supplémentaires
date_jour = pd.Timestamp.today()
x_date_jour = datetime.now().strftime("%d/%m/%Y")
t_heure_actuelle = datetime.now().strftime("%H:%M")

# 🔹 Exemple de données
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
            progression = (t_prix - t_ouverture) * x_qte  # 0

        total_prix = t_prix * x_qte / x_currency
        liste_donnees.append([label_date, x_nom_valeur, round(total_prix), round(progression)])
    else:
        st.warning(f"Le ticker n’a pas été trouvé : {x_code_valeur}")

# Appels aux tickers
Get_tout('FR0000120404', 'ACCOR', x_date_jour, 214, 1)
Get_tout('NL0000235190', 'AIRBUS', x_date_jour, 95, 1)
Get_tout('GOOGL', 'ALPHABET', x_date_jour, 79, x_cours_dollar)
Get_tout('US0231351067', 'AMAZON', x_date_jour, 52, x_cours_dollar)
Get_tout('NL0010273215', 'ASML', x_date_jour, 18, 1)
Get_tout('US11135F1012', 'BROADCOM', x_date_jour, 73, x_cours_dollar)
Get_tout('DE0005810055', 'DEUTSCHE BORSE', x_date_jour, 42, 1)
Get_tout('FR0000052292', 'HERMES', x_date_jour, 4, 1)
Get_tout('ES0144580Y14', 'IBERDROLA', x_date_jour, 712, 1)
Get_tout('IT0003856405', 'LEONARDO', x_date_jour, 142, 1)
Get_tout('US5949181045', 'MICROSOFT', x_date_jour, 48, x_cours_dollar)
Get_tout('US64110L1061', 'NETFLIX', x_date_jour, 10, x_cours_dollar)
Get_tout('US67066G1040', 'NVDIA', x_date_jour, 160, x_cours_dollar)
Get_tout('US6974351057', 'PALO ALTO', x_date_jour, 56, x_cours_dollar)
Get_tout('DE0007030009', 'RHEINMETALL', x_date_jour, 5, 1)
Get_tout('US79466L3024', 'SALESFORCE', x_date_jour, 46, x_cours_dollar)
Get_tout('FR0000121329', 'THALES', x_date_jour, 24, 1)
Get_tout('FR0000120271', 'TOTAL ENERGIES', x_date_jour, 111, 1)
Get_tout('US92826C8394', 'VISA', x_date_jour, 40, x_cours_dollar)
Get_tout('FR0007054358', 'ETF STOXX 50', x_date_jour, 1543, 1)
Get_tout('FR0010315770', 'ETF MSCI', x_date_jour, 305, 1)
Get_tout('LU1829221024', 'ETF NASDAQ', x_date_jour, 130, 1)

# 🔸 Création du DataFrame
df = pd.DataFrame(liste_donnees, columns=["Date", "Valeur", "Montant", "Progression"])
df["Progression"] = df["Progression"].astype(str).str.replace(",", ".").astype(int)
df["Montant"] = df["Montant"].astype(float)
df_sorted = df.sort_values(by="Progression", ascending=False).reset_index(drop=True)

# 🔸 Calcul des totaux
total_prix = df["Montant"].sum()
total_prog = df["Progression"].sum()

# 🔸 Affichage des totaux
if total_prog > 0:
    st.markdown(
        f"<p style='margin-top: 0; margin-bottom: 5px; font-size: 24px;'>"
        f"<strong>Total : {format_euro(total_prix + t_reserves)} &nbsp;&nbsp;"
        f"<span style='color: green;'>Gains : +{format_euro(total_prog)}</span></strong>"
        f"</p><p style='margin-top: 10px; font-size: 16px;'>"
        f"Le {x_date_jour} à {t_heure_actuelle}</p>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"<p style='font-size: 24px;'>Total : {format_euro(total_prix + t_reserves)} - "
        f"<span style='color: red;'>Pertes : {format_euro(total_prog)}</span> - "
        f"{x_date_jour} - {t_heure_actuelle}</p>",
        unsafe_allow_html=True    )

# 🔸 Style JS conditionnel pour la progression
cell_style_js = JsCode("""
function(params) {
    if (params.value > 0) {
        return { color: 'green', fontWeight: 'bold' };
    } else if (params.value < 0) {
        return { color: 'red', fontWeight: 'bold' };
    }
    return null;
}
""")

# 🔸 Configuration du tableau interactif
gb = GridOptionsBuilder.from_dataframe(df_sorted)
gb.configure_selection("single", use_checkbox=False)
gb.configure_column("Montant", type=["numericColumn"], valueFormatter="x.toLocaleString('fr-FR', {style: 'currency', currency: 'EUR'})")
gb.configure_column("Progression", cellStyle=cell_style_js)
grid_options = gb.build()


st_autorefresh(interval=60000, key="refresh")


# 🔸 Affichage AgGrid
st.markdown("## 📊 Tableau interactif")
grid_response = AgGrid(
    df_sorted,
    gridOptions=grid_options,
    height=750,
    fit_columns_on_grid_load=True,
    enable_enterprise_modules=False,
    update_mode='SELECTION_CHANGED',
    allow_unsafe_jscode=True,
)

# 🔸 Affichage de la ligne sélectionnée
selected = grid_response["selected_rows"]
if selected:
    ligne = selected[0]
    st.markdown("### ✅ Ligne sélectionnée")
    st.json(ligne)
