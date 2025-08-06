import streamlit as st
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import JsCode
from streamlit_autorefresh import st_autorefresh
import yfinance as yf

#CALCULER LA RESERVE
t_reserves = 92300  + 31774+ 2050
x_version = "- Version du 2307-2025"

#FORMAT NUMERIQUE EN EURO
def format_euro(num_brut):
    num_brut = round(num_brut)
    num_brut = str("{:,.2f}".format(num_brut).replace(',', ' '))
    num_brut = num_brut.replace('.00', ' ')
    return num_brut + " €"

#DATE ET HEURE ACTUELLE
date_jour = pd.Timestamp.today()
x_date_jour = datetime.now().strftime("%d/%m/%Y")

# HEURE DU JOUR TRUQUEE POUR ANDROID
t_heure_jour = datetime.now().strftime("%H:%M")  # Séparer heures et minutes
heures, minutes = map(int, t_heure_jour.split(":"))
heures += 2 # Ajouter 2 heures
heures %= 24 #Corriger si on dépasse 23h
t_heure_jour = f"{heures:02d}:{minutes:02d}"
#print(t_heure_jour)  # Donne : 16:25

#CALCULER LE COURS DU DOLLAR
usd_eur_data = yf.Ticker("EURUSD=X")
x_cours_dollar = round(usd_eur_data.history(period="1d")["Close"].iloc[-1], 4)

#LISTE DES DONNEES
liste_donnees =[]

#FONCTION PRINCIPALE DE CALCUL DES DONNEES
def Get_tout(x_code_valeur,x_nom_valeur,x_date_jour,x_qte,x_currency):

#   CHERCHER LE TICKER
    x_ticker = yf.Ticker(x_code_valeur)
    data = x_ticker.history(start="2025-08-01")['Close']   # PLANTAGE ICI A LONDRES
    if data.empty:
        st.warning(f"Données absentes pour {x_nom_valeur}, vérifier la date")
        return
    else:
        t_open  = data.iloc[-2]
        t_close = data.iloc[-1]

#   CALCULER LE LIBELLE DE DATE
    t_label_date = "" if x_date_jour == data.index[-1].strftime("%d/%m/%Y") else "Hier"

#   Suite incident Londres
    #print(x_nom_valeur,t_open,t_close)

    # GAINS OU PERTES DU JOUR EN PC **********  OK
    t_jour_pc = (t_close-t_open) / t_open

    # MONTANT DE l'ACTION EN EUROS  **********  OK
    t_mt_action = t_close * x_qte / x_currency

    # GAINS OU PERTES DU JOUR EN EUROS
    t_jour_Euro = ((t_close - t_open) * x_qte) / x_currency

    #DEFINIR LES COLONNES DU TABLEAU
    nom_et_montant = f"{x_nom_valeur} - {format_euro(t_mt_action)}"
    liste_donnees.append([t_label_date,nom_et_montant,t_mt_action,t_jour_pc,int(t_jour_Euro)])

# LISTE DES VALEURS (code, nom, quantité, devise)
valeurs = [
('FR0000120404', 'ACCOR',            259, 1),   #214
#'FR0000120404', 'ACCOR (2)',         45, 1),   # 45
('NL0000235190', 'AIRBUS',            95, 1),
('GOOGL',        'ALPHABET',          79, x_cours_dollar),
('US0231351067', 'AMAZON',            52, x_cours_dollar),
('NL0010273215', 'ASML',              21, 1),   # 18
#'NL0010273215', 'ASML (2)',           3, 1),   # 3
('FR0000131104', 'BNP (2)',           28, 1),
('US11135F1012', 'BROADCOM',          73, x_cours_dollar),
('FR0014004L86', 'DASSAULT AVIATION',  8, 1),
('FR0000121667', 'ESSILOR',           34, 1),
('ES0144580Y14', 'IBERDROLA',        712, 1),
('IT0003856405', 'LEONARDO',         142, 1),
('FR0000121014', 'LVMH (2)',           5, 1),
('US5949181045', 'MICROSOFT',         48, x_cours_dollar),
('US64110L1061', 'NETFLIX',           10, x_cours_dollar),
('US67066G1040', 'NVDIA',            160, x_cours_dollar),
('US6974351057', 'PALO ALTO',         56, x_cours_dollar),
('DE0007030009', 'RHEINMETALL',       10, 1),
('US79466L3024', 'SALESFORCE',        46, x_cours_dollar),
#'DE0007164600', 'SAP ',              42, 1),   # 34
('DE0007164600', 'SAP (2)',            8, 1),   # 8
('FR0000121329', 'THALES',            24, 1),
('FR0000120271', 'TOTAL ENERGIE',    167, 1),   # 111
#'FR0000120271', 'TOTAL ENERGIE (2)', 56, 1),   #  56
('US92826C8394', 'VISA',              40, x_cours_dollar),
('FR0007054358', 'ETF STOXX 50',    1543, 1),
('LU3038520774', 'ETF DEFENSE (2)',  360, 1),
#'LU1829221024', 'ETF NASDAQ',       130, 1),
('FR0010315770', 'ETF MSCI',         305, 1)]

#CHARGEMENT DES DONNEES
for code, nom, qte, devise in valeurs:
    Get_tout(code, nom, x_date_jour, qte, devise)

#TITRES DES COLONNES
df = pd.DataFrame(liste_donnees,columns=["Date", "Valeur", "Montant", "Jour_PC", "Jour_Euro"])

#TRI PRINCIPAL
df_sorted = df.sort_values(by=["Date", "Jour_PC"], ascending=[True, False]).reset_index(drop=True)

#TOTALISER LES 2 INFOS
total_prix = df["Montant"].sum()
total_prog = df[df["Date"] != "Hier"]["Jour_Euro"].sum()

#JOURNAL
#chemin_fichier = "/storage/emulated/0/Download/log.txt"
#ligne_log =  x_date_jour + " à " + t_heure_jour + "Total_Prog : " + format_euro(total_prix+t_reserves) + " - Jour : " + format_euro(total_prog)

#st.warning("Mon fichier " + "/storage/emulated/0/Download/log.txt")
# Écriture avec vérification
#try:
    #with open(chemin_fichier, "a") as f:
        #f.write(ligne_log)
    #st.warning("✅ Fichier écrit avec succès.")
#except FileNotFoundError:
    #st.warning("❌ Erreur : Dossier introuvable.")
#except PermissionError:
    #st.warning("❌ Erreur : Permission refusée (autorisez l'accès au stockage).")
#except Exception as e:
    #st.warning(f"❌ Erreur inattendue : {e}")

#AFFICHER LE TITRE DES GAINS
if total_prog > 0:
    st.markdown(
    f"<div style='margin: 0; padding: 0;'>"  f"<p style='margin: 0;            font-size: 24px;'>"
    f"<strong>Total : {format_euro(  round( total_prix+t_reserves)  )} &nbsp;&nbsp; "
    f"<span style='color: green;'>- Gains : {format_euro(total_prog)}</span>" f"</p>"
    f"<p style='margin: 0; font-size: 16px;'>"
    f"Le {x_date_jour} à {t_heure_jour} {x_version}</p>"        f"</div>",
    unsafe_allow_html=True)

#TITRES DES PERTES
else:
    st.markdown(
    f"<p style='margin-top: 0; margin-bottom: 5px; font-size: 24px;'>"
    f"<strong><span style='color: blue;'>📊 Total : {format_euro(  round(  total_prix + t_reserves)   )} &nbsp;"
    f"<strong><span style='color: red;'>- Pertes : {format_euro(total_prog)} &nbsp; "
    f"</p><p style='margin-top: 10px; font-size: 16px;'>"
    f"Le {x_date_jour} à {t_heure_jour}  {x_version} </p>",
    unsafe_allow_html=True)

#DEFINIR LES COULEURS DES RUBRIQUES NUMERIQUES DANS LA LISTE exe
cell_style_js = JsCode("""
function(params) {
    if (params.data && params.data.Date === "Hier") {
        return { color: 'Orange', fontWeight: 'bold' };    }
    if (params.value > 0) {
        return { color: 'green', fontWeight: 'bold' };
    } else if (params.value < 0) {
        return { color: 'red', fontWeight: 'bold' };    }
    return null;} """)

#CONFIGURATION DU TABLEAU
gb = GridOptionsBuilder.from_dataframe(df_sorted)
gb.configure_selection("single", use_checkbox=False)

#DEFINIR LES LARGEURS DE COLONNES
gb.configure_column("Date", width=40)
gb.configure_column("Valeur", width=100)
gb.configure_column("Montant", width=60)
gb.configure_column("Jour_Euro", width=100)
gb.configure_column("Jour_PC", width=100)

#VENDREDI
gb.configure_column(
    "Valeur",
    width=120, maxWidth=200,
    resizable=False,
    cellStyle=JsCode("""
        function(params) {
            return {whiteSpace: 'nowrap', overflow: 'hidden',
            textOverflow: 'ellipsis', maxWidth: '160px'}; } """),tooltipField="Valeur" )

#APPLIQUER DES FORMATAGES AUX COLONNES NUMERIQUES
gb.configure_column("Jour_Euro", type=["numericColumn"],valueFormatter="x.toLocaleString('fr-FR', {style: 'currency', currency: 'EUR', minimumFractionDigits: 0, maximumFractionDigits: 0})")
gb.configure_column("Jour_PC",   type=["numericColumn"],valueFormatter="(x * 100).toLocaleString('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' %'")

#APPLIQUER DES COULEURS AUX ZONES NUMERIQUES
colonnes_numeriques = ["Jour_Euro", "Jour_PC"]
for col in colonnes_numeriques:
    gb.configure_column(col, cellStyle=cell_style_js)
    valeur_montant_style_js = JsCode("""
    function(params) {
        if (params.data && params.data.Date === "Hier") {
            return { color: 'blue', fontWeight: 'normal' };
        } else {
            return { color: 'blue', fontWeight: 'bold' }; } } """)

    #APPLIQUER COULEUR ET GRAS AUX DEUX COLONNES MONTANT ET VALEUR
    gb.configure_column("Valeur", cellStyle=valeur_montant_style_js)

#   CACHER DEUX COLONNES
    gb.configure_column("Date", hide=True)
    gb.configure_column("Montant", hide=True)

#ACTIVER LES OPTIONS
grid_options = gb.build()

#APPLIQUE RAFRAICHISSEMENT TOUTES LES 3 MINUTES
st_autorefresh(interval=120000, key="refresh")

#PARAMETRES DE TAILLE DU TABLEAU
hauteur_ligne = 32
hauteur_totale = len(df_sorted) * hauteur_ligne #+ 20

#UTILE
grid_response = AgGrid(
    df_sorted,
    gridOptions=grid_options,
    height=hauteur_totale,
    fit_columns_on_grid_load=False,
    enable_enterprise_modules=False,
    update_mode='SELECTION_CHANGED',
    allow_unsafe_jscode=True,
    width='100%',
    containerStyle={"width": "100%"})

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




