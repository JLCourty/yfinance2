import streamlit as st
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import JsCode
from streamlit_autorefresh import st_autorefresh
import yfinance as yf

# Fonction formatage en euros
def format_euro(val):
    return f"{val:,.2f} €".replace(",", " ").replace(".", ",")

# Date et heure actuelles
x_date_jour = datetime.now().strftime("%d/%m/%Y")
t_heure_actuelle = datetime.now().strftime("%H:%M")

# Données USD/EUR
usd_eur_data = yf.Ticker("EURUSD=X")
x_cours_dollar = round(usd_eur_data.history(period="1d")["Close"].iloc[-1], 4)

# Liste de données à remplir
liste_donnees = []

# Fonction principale
def Get_tout(x_code_valeur,x_nom_valeur):
    if x_code_valeur:
        x_ticker = yf.Ticker(x_code_valeur)
        data = x_ticker.history(start="2025-01-02")['Close']

        if data.empty:
            return

        t_date_jour = data.index[-1].strftime("%d/%m/%Y")
        x_label_date = "Aujourd'hui" if x_date_jour == t_date_jour else "Hier"

        vJanvier = data.iloc[0]
        t_close_jour = data.iloc[-1]
        t_open_jour = data.iloc[-2]
        variation_pct = ((t_close_jour - t_open_jour) / t_open_jour) * 100
        Janvier_PC = round((t_close_jour - vJanvier) / vJanvier * 100, 2)

        liste_donnees.append([
            x_label_date,
            x_nom_valeur,
            Janvier_PC,
            format_euro(t_open_jour),
            format_euro(t_close_jour),
            round(variation_pct, 2)
        ])

#CHAINE DES VALEURS FRANCAISES
valeurs = [
('FR0000131104','FR - BNP'),
('FR0000130809','FR - Soc Générale'),
('FR0000133308','FR - Orange'),
('US4370761029','US - Home Depot'),
('DE000RENK730','DE - Renk Allemand'),
('FR0000120404','FR - Accor'),
('FR0000120073','FR - Air Liquide'),
('NL0000235190','FR - Airbus'),
('FR0010220475','FR - Alstom'),
('LU1598757687','EU - Arcelor Mittal'),
('FR0000120628','FR - Axa'),
('FR0000120503','FR - Bouygues'),
('FR0000125338','FR - Capgemini'),
('FR0000120172','FR - Carrefour'),
('FR0000045072','FR - Crédit Agricole'),
('FR0000120644','FR - Danone'),
('FR0014003TT8','FR - Dassault Systemes'),
('FR0014004L86','FR - Dassault Aviation'),
('FR0010908533','FR - Edenred'),
('FR0010208488','FR - Engie'),
('FR0000121667','FR - Essilor Luxottica'),
('FR0014000MR3','FR - Eurofins Scientific'),
('FR0000052292','FR - Hermès'),
('FR0000121485','FR - Kering'),
('FR0000120321','FR - LOréal'),
('FR0010307819','FR - Legrand'),
('FR0000121014','FR - LVMH'),
('FR001400AJ45','FR - Michelin'),
('FR0000120693','FR - Pernod Ricard'),
('FR0000130577','FR - Publicis'),
('FR0000131906','FR - Renault'),
('FR0000073272','FR - Safran'),
('FR0000125007','FR - Saint-Gobain'),
('FR0000120578','FR - Sanofi'),
('FR0000121972','FR - Schneider Electric'),
('NL00150001Q9','FR - Stellantis'),
('NL0000226223','EU - ST Microelectronics'),
('FR0000051807','FR - Teleperformance'),
('FR0000121329','FR - Thales'),
('FR0000120271','FR - Total Energies'),
('FR001400J770','FR - Unibail-Rodamco'),
('FR0000124141','FR - Veolia Environnement'),
('FR0000125486','FR - Vinci'),
('FR0000127771','FR - Vivendi'),
('FR0012757854','FR - SPIE'),
('DE000A1EWWW0','EU - Adidas'),
('NL0012969182','EU - Adyen'),
('NL0011794037','EU - Ahold Delhaize'),
('DE0008404005','EU - Allianz'),
('BE0974293251','EU - Anheuser-Busch InBev'),
('NL0010273215','EU - ASML Holding'),
('DE000BASF111','EU - BASF'),
('DE000BAY0017','EU - Bayer'),
('ES0113211835','EU - BBVA'),
('ES0113900J37','EU - Banco Santander'),
('DE0005190003','EU - BMW'),
('DE0005810055','EU - Deutsche Börse'),
('DE0005552004','EU - Deutsche Post'),
('DE0005557508','EU - Deutsche Telekom'),
('IT0003128367','EU - Enel'),
('IT0003132476','EU - Eni'),
('NL0011585146','EU - Ferrari'),
('IE00BWT6H894','EU - Flutter Entertainment'),
('ES0144580Y14','EU - Iberdrola'),
('ES0148396007','EU - Inditex'),
('DE0006231004','EU - Infineon Technologies'),
('NL0011821202','EU - ING Group'),
('IT0000072618','EU - Intesa Sanpaolo'),
('DE0007100000','EU - Mercedes-Benz Group'),
('DE0008430026','EU - Munich Re'),
('FI0009000681','EU - Nokia'),
('NL0013654783','EU - Prosus'),
('DE0007164600','EU - SAP'),
('DE0007236101','EU - Siemens'),
('IT0005239360','EU - UniCredit'),
('DE0007664039','EU - Volkswagen Group'),
('DE000A1ML7J1','EU - Vonovia'),
('US02079K3059','US - Alphabet Class A'),
('US02079K1079','US - Alphabet Class C'),
('US30303M1027','US - Meta'),
('US67066G1040','US - Nvidia'),
('US88160R1014','US - Tesla'),
('US11135F1012','US - Broadcom'),
('US64110L1061','US - Netflix'),
('US22160K1051','US - Costco'),
('US17275R1023','US - Cisco Systems'),
('US4581401001','US - Intel Corporation'),
('US0079031078','US - Advanced Micro Devices'),
('US0530151036','US - Automatic Data Processing'),
('US7223041028','US - Pinduoduo'),
('US8825081040','US - Texas Instruments'),
('US7475251036','US - Qualcom'),
('US8552441094','US - Starbucks'),
('US0382221051','US - Applied Materials'),
('US4612021034','US - Intuit Inc'),
('US4523271090','US - Illumina'),
('US75886F1075','US - Regeneron Pharma'),
('US09062X1037','US - Biogen Inc'),
('US30161N1019','US - Exelon Corporation'),
('US92532F1003','US - Vertex Pharma'),
('US47215P1066','US - JD.com'),
('US2561631068','US - Docusign'),
('US2855121099','US - Electronic Arts'),
('US98138H1014','US - Workda'),
('US00724F1012','US - Adobe Inc'),
('US09857L1089','US - Booking Holdings'),
('LU0908500753','EU - ETF STOXX Eur 600'),
('FR0007054358','EU - ETF STOXX 50'),
('FR0010315770','US - ETF MSCI'),
('LU1829221024','US - ETF NASDAQ'),
('LU3038520774','EU - ETF Amundi Stoxx Defense'),
('US98980L1017','US - Zoom Video') ]

#('US5737741035','Marvell Technolog'),

for code, nom in valeurs:
    Get_tout(code, nom)

df = pd.DataFrame(liste_donnees, columns=["Date", "Valeur", "PC_2025", "Open", "Close", "PC_Jour"])
df_sorted = df.sort_values(by="PC_Jour", ascending=False).reset_index(drop=True)

nombre_de_lignes = len(df_sorted)

st.markdown(
    f"<p style='margin-top: 0; margin-bottom: 5px; font-size: 36px;'>"
    f"<strong>📊 Prévisionnel &nbsp;&nbsp; "
    f"</p><p style='margin-top: 10px; font-size: 16px;'>"
    f"{nombre_de_lignes} lignes - le {x_date_jour} à {t_heure_actuelle}     - Version 2313</p>",
    unsafe_allow_html=True)

# Style conditionnel JS
cell_style_js = JsCode("""
function(params) {
    if (params.value > 0) {
        return { color: 'green', fontWeight: 'bold' };
    } else if (params.value < 0) {
        return { color: 'red', fontWeight: 'bold' };    }
    return null;
} """)

cell_style_pc2025 = JsCode("""
function(params) {
    let color = 'black';
    if (params.value < 0) {
        color = 'red';
    } else if (params.value > 0) {
        color = 'green';
    }
    return {
        fontWeight: 'bold',
        color: color
    };
} """)

# Configuration du tableau
filtre = st.radio("Filtrer les valeurs par origine :", options=["Toutes", "FR", "EU", "US"], horizontal=True)

if filtre != "Toutes":
    df_filtered = df_sorted[df_sorted["Valeur"].str.startswith(filtre)]
else:
    df_filtered = df_sorted

gb = GridOptionsBuilder.from_dataframe(df_filtered)
gb.configure_column("Open", cellStyle=cell_style_js)
gb.configure_column("PC_2025", cellStyle=cell_style_pc2025)

grid_options = gb.build()

st_autorefresh(interval=180000, key="refresh")

grid_response = AgGrid(
    df_filtered,
    gridOptions=grid_options,
    height=680,
    fit_columns_on_grid_load=True,
    enable_enterprise_modules=False,
    update_mode='SELECTION_CHANGED',
    allow_unsafe_jscode=True,
)

selected = grid_response["selected_rows"]

if isinstance(selected, list) and selected:
    ligne = selected[0]
    st.markdown("### ✅ Ligne sélectionnée")
    st.json(ligne)
