import streamlit as st
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import JsCode
from streamlit_autorefresh import st_autorefresh
import yfinance as yf
import matplotlib.pyplot as plt

# 🔹 Réserves initiales
t_reserves = 132846

# 🔹 Fonctions utilitaires
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
        progression = (t_prix - t_ouverture) * x_qte
        variation_pct = ((t_prix - t_ouverture) / t_ouverture) * 100

        total_prix = t_prix * x_qte / x_currency
        liste_donnees.append([
            label_date,
            x_nom_valeur,
            round(total_prix),
            round(progression),
            round(variation_pct, 2)
        ])
    else:
        st.warning(f"Le ticker n’a pas été trouvé : {x_code_valeur}")

# 🔹 Portefeuille (code, nom, quantité, devise)
valeurs = [
    ('FR0000120404', 'ACCOR', 214, 1),
    ('NL0000235190', 'AIRBUS', 95, 1),
    ('GOOGL', 'ALPHABET', 79, x_cours_dollar),
    ('US0231351067', 'AMAZON', 52, x_cours_dollar),
    ('NL0010273215', 'ASML', 18, 1),
    ('US11135F1012', 'BROADCOM', 73, x_cours_dollar),
    ('DE0005810055', 'DEUTSCHE BORSE', 42, 1),
    ('FR0000052292', 'HERMES', 4, 1),
    ('ES0144580Y14', 'IBERDROLA', 712, 1),
    ('IT0003856405', 'LEONARDO', 142, 1),
    ('US5949181045', 'MICROSOFT', 48, x_cours_dollar),
    ('US64110L1061', 'NETFLIX', 10, x_cours_dollar),
    ('US67066G1040', 'NVDIA', 160, x_cours_dollar),
    ('US6974351057', 'PALO ALTO', 56, x_cours_dollar),
    ('DE0007030009', 'RHEINMETALL', 5, 1),
    ('US79466L3024', 'SALESFORCE', 46, x_cours_dollar),
    ('FR0000121329', 'THALES', 24, 1),
    ('FR0000120271', 'TOTAL ENERGIES', 111, 1),
    ('US92826C8394', 'VISA', 40, x_cours_dollar),
    ('FR0007054358', 'ETF STOXX 50', 1543, 1),
    ('FR0010315770', 'ETF MSCI', 305, 1),
    ('LU1829221024', 'ETF NASDAQ', 130, 1)
]

# 🔹 Chargement des données
for code, nom, qte, devise in valeurs:
    Get_tout(code, nom, x_date_jour, qte, devise)

# 🔹 DataFrame final
df = pd.DataFrame(
    liste_donnees,
    columns=["Date", "Valeur", "Montant", "Progression", "Variation (%)"]
)
df["Progression"] = df["Progression"].astype(str).str.replace(",", ".").astype(float)
df["Montant"] = df["Montant"].astype(float)

df_sorted = df.sort_values(by="Progression", ascending=False).reset_index(drop=True)

# 🔹 Totaux
total_prix = df["Montant"].sum()
total_prog = df["Progression"].sum()

# 🔹 Affichage des totaux
if total_prog > 0:
    st.markdown(
        f"<p style='margin-top: 0; margin-bottom: 5px; font-size: 20px;'>"
        f"<strong>📊 Total : {format_euro(total_prix + t_reserves)} &nbsp;&nbsp; "
        f"<span style='color: green;'>Gains : +{format_euro(total_prog)}</span></strong>"
        f"</p><p style='margin-top: 10px; font-size: 16px;'>"
        f"Le {x_date_jour} à {t_heure_actuelle}</p>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"<p style='font-size: 20px;'>Total : {format_euro(total_prix + t_reserves)} - "
        f"<span style='color: red;'>Pertes : {format_euro(total_prog)}</span> - "
        f"{x_date_jour} - {t_heure_actuelle}</p>",
        unsafe_allow_html=True
    )

# 🔹 Mise en forme conditionnelle JS
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

# 🔹 Configuration AgGrid
gb = GridOptionsBuilder.from_dataframe(df_sorted)
gb.configure_selection("single", use_checkbox=False)
gb.configure_column("Montant", type=["numericColumn"],
                    valueFormatter="x.toLocaleString('fr-FR', {style: 'currency', currency: 'EUR'})")
gb.configure_column("Progression", cellStyle=cell_style_js)
gb.configure_column("Variation (%)", cellStyle=cell_style_js)
grid_options = gb.build()

# 🔄 Rafraîchissement automatique
st_autorefresh(interval=60000, key="refresh")

# 🔹 Affichage AgGrid
grid_response = AgGrid(
    df_sorted,
    gridOptions=grid_options,
    height=680,
    fit_columns_on_grid_load=True,
    enable_enterprise_modules=False,
    update_mode='SELECTION_CHANGED',
    allow_unsafe_jscode=True,)

#**********************************************

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

# Bouton export CSV (toujours visible)
df_export = df_sorted.drop(columns=["Date"]).sort_values(by="Valeur")
csv = df_export.to_csv(index=False, sep=';').encode('utf-8-sig')
st.download_button(
    label="📥 Télécharger le tableau (.csv)",
    data=csv,
    file_name="portefeuille.csv",
    mime="text/csv"
)

# Affichage ligne sélectionnée + graphe si sélection
selected = grid_response["selected_rows"]
if isinstance(selected, list) and selected:
    ligne = selected[0]
    st.markdown("### ✅ Ligne sélectionnée")
    st.json(ligne)

    nom_valeur = ligne["Valeur"]
    st.write(f"Valeur sélectionnée : '{nom_valeur}'")

    map_nom_ticker = {
        'ACCOR': 'FR0000120404',
        'AIRBUS': 'NL0000235190',
        'ALPHABET': 'GOOGL',
        'AMAZON': 'US0231351067',
        'ASML': 'NL0010273215',
        'BROADCOM': 'US11135F1012',
        'DEUTSCHE BORSE': 'DE0005810055',
        'HERMES': 'FR0000052292',
        'IBERDROLA': 'ES0144580Y14',
        'LEONARDO': 'IT0003856405',
        'MICROSOFT': 'US5949181045',
        'NETFLIX': 'US64110L1061',
        'NVDIA': 'US67066G1040',
        'PALO ALTO': 'US6974351057',
        'RHEINMETALL': 'DE0007030009',
        'SALESFORCE': 'US79466L3024',
        'THALES': 'FR0000121329',
        'TOTAL ENERGIES': 'FR0000120271',
        'VISA': 'US92826C8394',
        'ETF STOXX 50': 'FR0007054358',
        'ETF MSCI': 'FR0010315770',
        'ETF NASDAQ': 'LU1829221024',
    }

    x_ticker = map_nom_ticker.get(nom_valeur)
    if not x_ticker:
        st.warning("⚠️ Historique non disponible pour cette valeur.")
    else:
        data_hist = yf.Ticker(x_ticker).history(start=f"{datetime.now().year}-01-01")
        st.write(f"Données historiques chargées : {len(data_hist)} lignes")
        if not data_hist.empty:
            fig, ax = plt.subplots()
            data_hist["Close"].plot(ax=ax, linewidth=2)
            ax.set_title(f"Historique YTD : {nom_valeur}")
            ax.set_ylabel("Cours (€ ou $)")
            ax.grid(True)
            st.pyplot(fig)
        else:
            st.warning("⚠️ Aucune donnée historique disponible.")