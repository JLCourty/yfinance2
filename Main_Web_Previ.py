import streamlit as st
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import JsCode
from streamlit_autorefresh import st_autorefresh
import yfinance as yf


#FONCTION FORMATAGE EN EUROS
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
def Get_tout(x_code_valeur,x_nom_valeur):

    #SI LE TICKER EST CORRECT
    if x_code_valeur:

        #CHERCHER DANS YFINANCE
        x_ticker = yf.Ticker(x_code_valeur)
        data = x_ticker.history(start="2025-01-02")['Close']

        if data.empty:
            st.warning(f"Données absentes pour {x_code_valeur}")
            return

        #EXTRAIRE ET TRAITER LA DATE DES DONNEES DE YFINANCE
        t_date_jour = data.index[-1].strftime("%d/%m/%Y")
        x_label_date = "Aujourd'hui" if x_date_jour == t_date_jour else "Hier"

        #EXTRAIRE LES COURS OUVERTURE ET DE FERMETURE
        vJanvier = data.iloc[0]         # 15 JANVIER
        t_close_jour = data.iloc[-1]
        t_open_jour = data.iloc[-2]
        variation_pct = ((t_close_jour - t_open_jour) / t_open_jour) * 100

        #TRAITER LES VARIATIONS DE 2025
        Janvier_PC =   round(  (t_close_jour - vJanvier) / vJanvier * 100   ,2)  #+"%" AVEC ce format le tri ne fonctionne plus

        #LISTE DES INFOS REELLEMENT AFFICHEES (AVEC LEUR FORMAT)
        liste_donnees.append([
            x_label_date,
            x_nom_valeur,
            #str(Janvier_PC)+"%",
            Janvier_PC,
            format_euro(t_open_jour),format_euro(t_close_jour),round(variation_pct, 2) ])

#CHAINE DES VALEURS FRANCAISES
valeurs = [
           ('FR0000131104','BNP'),
           ('FR0000130809','Soc Générale'),
           ('FR0000133308','Orange'),
           ('US4370761029','US-Home Depot'),
           ('DE000RENK730','Renk Allemand'),
           ('FR0000120404','Accor'),
           ('FR0000120073','Air Liquide'),
           ('NL0000235190','Airbus'),
           ('FR0010220475','Alstom'),
           ('LU1598757687','Arcelor Mittal'),
           ('FR0000120628','Axa'),
           ('FR0000120503','Bouygues'),
           ('FR0000125338','Capgemini'),
           ('FR0000120172','Carrefour'),
           ('FR0000045072','Crédit Agricole'),
           ('FR0000120644','Danone'),
           ('FR0014003TT8','Dassault Systemes'),
           ('FR0010908533','Edenred'),
           ('FR0010208488','Engie'),
           ('FR0000121667','Essilor Luxottica'),
           ('FR0014000MR3','Eurofins Scientific'),
           ('FR0000052292','Hermès'),
           ('FR0000121485','Kering'),
           ('FR0000120321','LOréal'),
           ('FR0010307819','Legrand'),
           ('FR0000121014','LVMH'),
           ('FR001400AJ45','Michelin'),
           ('FR0000120693','Pernod Ricard'),
           ('FR0000130577','Publicis'),
           ('FR0000131906','Renault'),
           ('FR0000073272','Safran'),
           ('FR0000125007','Saint-Gobain'),
           ('FR0000120578','Sanofi'),
           ('FR0000121972','Schneider Electric'),
           ('NL00150001Q9','--Stellantis'),
           ('NL0000226223','ST Microelectronics'),
           ('FR0000051807','Teleperformance'),
           ('FR0000121329','Thales'),
           ('FR0000120271','Total Energies'),
           ('FR001400J770','Unibail-Rodamco'),
           ('FR0000124141','Veolia Environnement'),
           ('FR0000125486','Vinci'),
           ('FR0000127771','Vivendi'),
           ('FR0014004L86','Dassault Aviation'),
           ('FR0012757854','SPIE'),
           ('US02079K3059', 'US-Alphabet Class A'),
        ('US02079K1079','US-Alphabet Class C'),
('US30303M1027','US-Meta Platforms'),
('US67066G1040','US-Nvidia'),
('US88160R1014','US-Tesla'),
('US11135F1012','US-Broadcom'),
('US64110L1061','US-Netflix'),
('US22160K1051','US-Costco'),
('US17275R1023','US-Cisco Systems'),
('US4581401001','US-Intel Corporation'),
('US0079031078','US-Advanced Micro Devices'),
('US0530151036','US-Automatic Data Processing'),
('US7223041028','US-Pinduoduo'),
('US8825081040','US-Texas Instruments'),
('US7475251036','US-Qualcom'),
('US8552441094','US-Starbucks Corporation'),
('US0382221051','US-Applied Materials'),
('US4612021034','US-Intuit Inc'),
('US4523271090','US-Illumina'),
('US75886F1075','US-Regeneron Pharmaceuticals'),
('US09062X1037','US-Biogen Inc'),
('US30161N1019','US-Exelon Corporation'),
('US92532F1003','US-Vertex Pharmaceuticals'),
('US47215P1066','US-JD.com'),
('US2561631068','US-Docusign'),
('US2855121099','US-Electronic Arts'),
('US98138H1014','US-Workda'),
('US00724F1012','US-Adobe Inc'),
('US09857L1089','US-Booking Holdings'),
('US98980L1017','US-Zoom Video') ]

#('US5737741035','Marvell Technolog'),

#LANCEMENT DE LA FONCTION SUR LA CHAINE DES VALEURS
for code, nom in valeurs:
    Get_tout(code,nom)

#TITRES DES COLONNES DU TABLEAU
df = pd.DataFrame(liste_donnees,columns=["Date", "Valeur", "PC_2025","Open", "Close", "PC_Jour"])

#TRI SUR LE PC DU JOUR
df_sorted = df.sort_values(by="PC_Jour", ascending=False).reset_index(drop=True)

nombre_de_lignes = len(df_sorted)
#print("Nombre de lignes :", nombre_de_lignes)

st.markdown(
        f"<p style='margin-top: 0; margin-bottom: 5px; font-size: 36px;'>"
        f"<strong>📊 Prévisionnel &nbsp;&nbsp; "
        f"</p><p style='margin-top: 10px; font-size: 16px;'>"
        f"{nombre_de_lignes} lignes - le {x_date_jour} à {t_heure_actuelle}     - Version 2313</p>",
        unsafe_allow_html=True    )

# 🔹 Mise en forme conditionnelle JS
cell_style_js = JsCode("""
function(params) {
    if (params.value > 0) {
        return { color: 'green', fontWeight: 'bold' };
    } else if (params.value < 0) {
        return { color: 'red', fontWeight: 'bold' };    }
    return null;} """)

#CONFIGURATION DU TABLEAU
gb = GridOptionsBuilder.from_dataframe(df_sorted)

#fonction pour formater les cellules
gb.configure_column("Open", cellStyle=cell_style_js)

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
}
""")
gb.configure_column("PC_2025", cellStyle=cell_style_pc2025)


# Style gras pour la colonne 3 : PC_2025
cell_style_bold = JsCode("function(params) { return { fontWeight: 'bold' }; }")
gb.configure_column("PC_2025", cellStyle=cell_style_pc2025)


#CONSTRUCTION DU TABLEAU
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



