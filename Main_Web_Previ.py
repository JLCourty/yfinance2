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
        #t_op en_jour = data.iloc[-2]

        # Vérification que data a au moins 2 lignes
        if len(data) >= 2:
            t_open_jour = data.iloc[-2]
        else:
            print("❌ Pas assez de données disponibles pour "+x_nom_valeur)
            t_open_jour = t_close_jour

        #VARIATION DU JOUR
        variation_pct = ((t_close_jour - t_open_jour) / t_open_jour) * 100

        #TRAITER LES VARIATIONS DE 2025
        Janvier_PC =   round(  (t_close_jour - vJanvier) / vJanvier * 100   ,2)  #+"%" AVEC ce format le tri ne fonctionne plus

        #LISTE DES INFOS REELLEMENT AFFICHEES (AVEC LEUR FORMAT)
        liste_donnees.append([
            x_label_date,x_nom_valeur,Janvier_PC,round(variation_pct, 2) ]) # format_euro(t_open_jour),format_euro(t_close_jour),

#CHAINE DES VALEURS FRANCAISES
valeurs = [
('FR0000052292','HERMES'),
('DE000RENK730','RENK ALLEMAND'),
('FR0014003TT8','DASSAULT SYSTEMS'),
('US45168D1046','IDEXX'),
('US8716071076','SYNOPSYS'),
('US68389X1054','ORACLE'),
('FR0010307819','LEGRAND'),
('FR0012757854','SPIE'),
('LU1829221024','ETF NASDAQ'),
#()'FR0000131104','FR - BNP'),
#('FR0000130809','FR - Soc Générale'),
#('FR0000120404','FR - Accor'),
#('FR0000120073','FR - Air Liquide'),
#('NL0000235190','FR - Airbus'),
#('FR0010220475','FR - Alstom'),
#('LU1598757687','FR - Arcelor Mittal'),
#('FR0000120628','FR - Axa'),
#('FR0000120503','FR - Bouygues'),
#('FR0000125338','FR - Capgemini'),
#('FR0000120172','FR - Carrefour'),
#('FR0000045072','FR - Crédit Agricole'),
#('FR0000120644','FR - Danone'),
#('FR0014004L86','FR - Dassault Aviation'),
#('FR0010908533','FR - Edenred'),
#('FR0010208488','FR - Engie'),
#('FR0000121667','FR - Essilor Luxottica'),
#('FR0014000MR3','FR - Eurofins Scientific'),
#('FR0000121485','FR - Kering'),
#('FR0000120321','FR - LOréal'),
#('FR001400AJ45','FR - Michelin'),
#('FR0000120693','FR - Pernod Ricard'),
#('FR0000130577','FR - Publicis'),
('FR0000131906','FR - Renault'),
#('FR0000073272','FR - Safran'),
#('FR0000125007','FR - Saint-Gobain'),
#('FR0000120578','FR - Sanofi'),
#('FR0000121972','FR - Schneider Electric'),
('NL00150001Q9','FR - Stellantis'),
#('NL0000226223','FR - ST Microelectronics'),
#('FR0000051807','FR - Teleperformance'),
#('FR001400J770','FR - Unibail-Rodamco'),
#('FR0000124141','FR - Veolia Environnement'),
#('FR0000125486','FR - Vinci'),
#('FR0000127771','FR - Vivendi'),
#('DE000A1EWWW0','EU - Adidas'),
('NL0012969182','Novo Nordisk'),
#('NL0011794037','EU - Ahold Delhaize'),
#('DE0008404005','EU - Allianz'),
#('BE0974293251','EU - Anheuser-Busch InBev'),
#('NL0010273215','EU - ASML Holding'),
#('DE000BASF111','EU - BASF'),
#('DE000BAY0017','EU - Bayer'),
#('ES0113211835','EU - BBVA'),
#('ES0113900J37','EU - Banco Santander'),
#('DE0005190003','EU - BMW'),
#('DE0005810055','EU - Deutsche Börse'),
#('DE0005552004','EU - Deutsche Post'),
#('DE0005557508','EU - Deutsche Telekom'),
#('IT0003128367','EU - Enel'),
#('IT0003132476','EU - Eni'),
#('NL0011585146','EU - Ferrari'),
#('IE00BWT6H894','EU - Flutter Entertainment'),
#('ES0144580Y14','EU - Iberdrola'),
#('ES0148396007','EU - Inditex'),
#('DE0006231004','EU - Infineon Technologies'),
#('NL0011821202','EU - ING Group'),
#('IT0000072618','EU - Intesa Sanpaolo'),
#('DE0007100000','EU - Mercedes-Benz Group'),
#('DE0008430026','EU - Munich Re'),
#('FI0009000681','EU - Nokia'),
#('NL0013654783','EU - Prosus'),
#('DE0007236101','EU - Siemens'),
#('IT0005239360','EU - UniCredit'),
#('DE0007664039','EU - Volkswagen Group'),
#('DE000A1ML7J1','EU - Vonovia'),

#('US02079K3059','US - Alphabet Class A'),
#('US02079K1079','US - Alphabet Class C'),
#('US30303M1027','US - Meta Platforms'),
#('US67066G1040','US - Nvidia'),
('US88160R1014','US - Tesla'),
#('US11135F1012','US - Broadcom'),
#('US64110L1061','US - Netflix'),
#('US22160K1051','US - Costco'),
#('US17275R1023','US - Cisco Systems'),
#('US4581401001','US - Intel Corporation'),
#('US0079031078','US - Advanced Micro Devices'),
#('US0530151036','US - Automatic Data Processing'),
#('US7223041028','US - Pinduoduo'),
#('US8825081040','US - Texas Instruments'),
#('US7475251036','US - Qualcom'),
#('US8552441094','US - Starbucks'),
#('US0382221051','US - Applied Materials'),
#('US4370761029','FR - US-Home Depot'),
#('US4612021034','US - Intuit Inc'),
#('US4523271090','US - Illumina'),
#('US75886F1075','US - Regeneron Pharma'),
#('US09062X1037','US - Biogen Inc'),
#('US30161N1019','US - Exelon Corporation'),
#('US92532F1003','US - Vertex Pharma'),
#('US47215P1066','US - JD.com'),
#('US2561631068','US - Docusign'),
#('US2855121099','US - Electronic Arts'),
#('US98138H1014','US - Workda'),
#('US00724F1012','US - Adobe Inc'),
#('US09857L1089','US - Booking Holdings'),
#('LU0908500753','ETF STOXX Eur 600'),
('DE0007164600','SAP')]

#LANCEMENT DE LA FONCTION SUR LA CHAINE DES VALEURS
for code, nom in valeurs:
    Get_tout(code,nom)

#TITRES DES COLONNES DU TABLEAU
df = pd.DataFrame(liste_donnees,columns=["Date","Valeur","PC_2025", "PC_Jour"])     #"Op en", "Close",

#TRI SUR LE PC DU JOUR
df_sorted = df.sort_values(by="PC_Jour", ascending=False).reset_index(drop=True)

#ENTETE
st.markdown(
        f"<p style='margin-top: 0; margin-bottom: 5px; font-size: 36px;'>"
        f"<strong>📊 Prévisionnel &nbsp;&nbsp; ",        unsafe_allow_html=True    )



#CONFIGURATION DU TABLEAU
gb = GridOptionsBuilder.from_dataframe(df_sorted)

#fonction pour formater les cellules
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
    };}""")
gb.configure_column("PC_2025", cellStyle=cell_style_pc2025)

# Style gras pour la colonne 3 : PC_2025
cell_style_bold = JsCode("function(params) { return { fontWeight: 'bold' }; }")

#APPLIQUER LA CONFIG A 3 COLONNES
gb.configure_column("PC_2025", cellStyle=cell_style_pc2025)
#gb.configure_column("Op en",    cellStyle=cell_style_pc2025)
gb.configure_column("PC_Jour", cellStyle=cell_style_pc2025)

#CONSTRUCTION DU TABLEAU
grid_options = gb.build()

# 🔄 Rafraîchissement automatique
st_autorefresh(interval=180000, key="refresh")  # 3 MINUTES

#AFFICHER AVEC AGRID
grid_response = AgGrid(
    df_sorted,
    gridOptions=grid_options,
    height=680,
    fit_columns_on_grid_load=True,
    enable_enterprise_modules=False,
    update_mode='SELECTION_CHANGED',
    allow_unsafe_jscode=True,)

#MESSAGE ????
selected = grid_response["selected_rows"]
if isinstance(selected, list) and selected:
    ligne = selected[0]
    st.markdown("### ✅ Ligne sélectionnée")
    st.json(ligne)

    if "Valeur" in ligne:
        nom_valeur = ligne["Valeur"]

        # Rechercher dans la liste des valeurs
        trouve = False
        for code, nom, qte, devise in valeurs:
            if nom == nom_valeur:
                trouve = True
                ticker = yf.Ticker(code)
                historique = ticker.history(start="2025-01-02")["Close"]

                if historique.empty:
                    st.warning(f"Aucune donnée trouvée pour {code}")
                    break

                # Conversion en euros
                historique_eur = historique / devise * qte
                historique_eur.name = "Montant (€)"

                st.markdown(f"### 📈 Évolution de **{nom_valeur}** en € depuis le 2 janvier 2025")
                st.line_chart(historique_eur)
                break

        if not trouve:
            st.warning(f"Aucune correspondance trouvée pour : {nom_valeur}")
    else:
        st.warning("Champ 'Valeur' non trouvé dans la ligne sélectionnée.")
