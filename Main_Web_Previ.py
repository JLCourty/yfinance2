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
def Get_tout(x_code_valeur,x_nom_valeur,Janvier,Janvier2,x_date_jour):

    if x_code_valeur:
        x_ticker = yf.Ticker(x_code_valeur)
        data = x_ticker.history(start="2025-05-11")['Close']
        if data.empty:
            st.warning(f"Données absentes pour {x_code_valeur}")
            return

        t_date_jour = data.index[-1].strftime("%d/%m/%Y")

        #COURS OUVERTURE ET DE FERMETURE
        t_close = data.iloc[-1]
        t_open = data.iloc[-2]

        label_date = "Aujourd'hui" if x_date_jour == t_date_jour else "Hier"

        if not label_date != "Hier":
            variation_pct = ((t_close - t_open) / t_open) * 100
        else:
            variation_pct = ((t_close - t_open) / t_open) * 100


        Janvier_PC =   str(round(  (t_close-Janvier) / Janvier * 100   ,2))+"%"


        #LISTE DES INFOS REELLEMENT AFFICHEES
        liste_donnees.append([
            label_date,
            x_nom_valeur,
            format_euro(Janvier),
            Janvier_PC,
            format_euro(t_open),
            format_euro(t_close),
            round(variation_pct, 2) ])
    else:
        st.warning(f"Le ticker n’a pas été trouvé : {x_code_valeur}")

#CHAINE DES VALEURS
valeurs = [
    ('FR0000131104', 'BNP'              ,  59.25, 222, 333 ),
    ('FR0000130809', 'SOCIETE GENERALE' ,  27.08,1, 1),
    ('FR0000133308', 'ORANGE'           ,   9.7,1,1),
    ('US4370761029','HOME DEPOT'        , 388.46,1,1),
    ('DE000RENK730','RENK ALLEMAND',  100,1, 1)       #NON ACQUISE QTE=0




]

#Get_tout('TSLA'        ,'TESLA',          x_date_jour,350.01 ,248.00 ,360, 1 ,0 , x_cours_dollar)    #NON ACQUISE QTE=0
#Get_tout('FR0014004L86','DASSAULT AV',    x_date_jour,350.01 ,317.00 ,400, 1 ,0 , 1)       #NON ACQUISE QTE=0Get_tout('FR0000062671','EXAIL TECHNOLOGIES',x_date_jour,350.01 ,50.00  ,60,  1 ,0 , 1)       #NON ACQUISE QTE=0

#Get_tout('US8835561023','THERMO FISCHER', x_date_jour,502.54 ,378.00 ,55,  1 ,0 , x_cours_dollar)    #NON ACQUISE QTE=0
#Get_tout('FR0000121014','LVMH',           x_date_jour,635.50 ,488    ,720, 1 ,0 , 1)       #NON ACQUISE QTE=0
#Get_tout('DE0007236101','SIEMENS',        x_date_jour,238.01 ,255    ,300, 1 ,0 ,1)        #NON ACQUISE QTE=0
#Get_tout('6758.T'      ,'SONY',           x_date_jour,238.01 ,255    ,300, 1 ,0 ,1)        #NON ACQUISE QTE=0
#Get_tout('DE0006452007','NEMETSCHEK',     x_date_jour,03.60  ,116.70 ,55,  1 ,0 ,1)        #NON ACQUISE QTE=0
#Get_tout('US8716071076','SYNOPSYS',       x_date_jour,472.47 ,405.00,55,  1 ,0 , x_cours_dollar)    #NON ACQUISE QTE=0
#Get_tout('GB0002634046','BAE SYSTEMS',    x_date_jour,350.01 ,1742.00,400, 1 ,0 , 1)       #NON ACQUISE QTE=0
#Get_tout('FR001400Q0V2','EXOSENS SA',     x_date_jour,350.01 ,36.00  ,42,  1 ,0 , 1)       #NON ACQUISE QTE=0
#Get_tout('FR0000133308','ORANGE',         x_date_jour,350.01 ,36.00  ,42,  1 ,0 , 1)       #NON ACQUISE QTE=0
#Get_tout('FR0000125486','VINCI',          x_date_jour,350.01 ,36.00  ,42,  1 ,0 , 1)       #NON ACQUISE QTE=0




#LANCEMENT DE LA FONCTION SUR LA CHAINE DES VALEURS
for code, nom, Janvier,Janvier2, devise in valeurs:
    Get_tout(code, nom,  Janvier,Janvier2,x_date_jour)

#TITRES DES COLONNES DU TABLEAU
df = pd.DataFrame(    liste_donnees,    columns=["Date", "Valeur", "Janvier","Janvier2","Open", "Close", "Variation Jour"])

#TRI
df_sorted = df.sort_values(by="Variation Jour", ascending=False).reset_index(drop=True)

st.markdown(
        f"<p style='margin-top: 0; margin-bottom: 5px; font-size: 36px;'>"
        f"<strong>📊 Prévisionnel &nbsp;&nbsp; "
        f"</p><p style='margin-top: 10px; font-size: 16px;'>"
        f"Le {x_date_jour} à {t_heure_actuelle}</p>",
        unsafe_allow_html=True    )

# 🔹 Mise en forme conditionnelle JS
cell_style_js = JsCode("""
function(params) {
    if (params.value > 0) {
        return { color: 'green', fontWeight: 'bold' };
    } else if (params.value < 0) {
        return { color: 'red', fontWeight: 'bold' };
    }
    return null;
} """)

#CONFIGURATION DU TABLEAU
gb = GridOptionsBuilder.from_dataframe(df_sorted)


#gb.configure_selection("single", use_checkbox=False)

#UTILE ????????
gb.configure_column("Open", cellStyle=cell_style_js)

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



