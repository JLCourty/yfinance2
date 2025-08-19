#INITIALISATION
from tkinter import *
import sqlite3
from Mes_fonctions import *
import subprocess
import pandas as pd

#DECLARER DES VARIABLES
VD="Verdana"
t_debut_annee = 593000    # DEBUT 2025
t_sepa = " │ "

#LES 3 DATES
start_date = pd.to_datetime("2025-05-01")
start_fin  = pd.to_datetime("2025-12-31")
today_date = pd.Timestamp.today().normalize()

#JOURS DEPUIS 1 MAI (OUVRES OU PAS)
nb_jm = pd.bdate_range(start=start_date, end=today_date)
nb_jm = len(nb_jm)

#CREER LA FENETRE PRINCIPALE
fenetre = Tk()
fenetre.title('Affichage des valeurs 2025')
largeur_fenetre = 1500
hauteur_fenetre = 950

#POSITIONNER LA FENETRE
largeur_ecran = fenetre.winfo_screenwidth()
position_x = (largeur_ecran-largeur_fenetre) // 2
position_y = 66
fenetre.geometry(f"{largeur_fenetre}x{hauteur_fenetre}+{position_x}+{position_y}")

#CREER DES CADRES SEPARES POUR LES INDICES ET LES VALEURS
frame_titres = Frame(fenetre)
frame_titres.grid(row=0,column=0,pady=20)
frame_valeurs = Frame(fenetre)
frame_valeurs.grid(row=9,column=0)
frame_message = Frame(fenetre)
frame_message.grid(row=22,column=0)

#CONFIGURER LES COLONNES
for i in range(3):  # 3 colonnes pour les titres
    frame_titres.columnconfigure(i,minsize=6)
for i in range(7):  # 7 colonnes pour les valeurs
    frame_valeurs.columnconfigure(i,minsize=20)

#SE CONNECTER A LA BASE DE DONNEES
conn = sqlite3.connect('ma_base_de_valeurs.db')
cursor = conn.cursor()

#EFFACER ECRAN
def clear_labels(frame):
    for widget in frame.winfo_children():
        if isinstance(widget, Label):
            widget.destroy()

#DEFINIR FONCTION QUI CALCULE ET AFFICHE EN BOUCLE
def update_label():

    #RELANCER LE CALCUL DES VALEURS
    subprocess.run(["python","Calculer.py"])

    # CHERCHER LES INFOS DES LES PARAMETRES
    cursor.execute("SELECT objectif,date_record,mt_reserve1,mt_reserve2 FROM parametres WHERE id = ?", (1,))
    t_objectif,t_date_record,t_reserve1,t_reserve2 = cursor.fetchone()  # TUPLE

    #PRENDRE LA LIGNE DE RESULTATS DU JOUR (LA PLUS RECENTE)
    cursor.execute("SELECT mt_actions,mt_total,mt_veille FROM resultats ORDER BY id DESC LIMIT 1")
    t_mt_actions,t_mt_total,t_mt_veille = cursor.fetchone()
    t_gains = t_mt_total-t_mt_veille
    mess_gains = "   Gains " if t_gains >= 0 else "   Pertes "
    mess_gains = mess_gains

    # VIDER LE BAS DE L'ECRAN
    clear_labels(frame_valeurs)

    # AFFICHER LIGNE 1
    Update_affichage = Label(frame_titres, text="HAUT" )   #   + str(da tetime.now())[11:19]    ,font=(VD, 22, "bold"), fg='Brown', width=40

    #AFFICHER LES RESULTATS SUR 2 LIGNES (2 et 3)
    t_lig=2
    Label(frame_titres,font=(VD,16,"bold"),fg=ma_coul2(t_gains),text="Portefeuille").grid(row=2,column=0,sticky="w")
    Label(frame_titres,font=(VD,16,"bold"),fg=ma_coul2(t_gains),text=mess_gains    ).grid(row=2,column=1,sticky="ew")
    Label(frame_titres,font=(VD,16,"bold"),fg="Brown" ,  text="     Réserves         Taux").grid(row=2,column=4,sticky="w") # RESTE A GAGNER

    #AFFICHER LES RESULTATS SUR 2 LIGNES (2 et 3)
    Label(frame_titres,font=(VD,16,"bold"),fg=ma_coul2(t_gains),text=format_euro2(t_mt_total)+ t_sepa).grid(row=3,column=0,sticky="ew")
    Label(frame_titres,font=(VD,16,"bold"),fg=ma_coul2(t_gains),text=format_euro2(t_mt_total-t_mt_veille)).grid(row=3,column=1,sticky="ew")
    Label(frame_titres,font=(VD,16,"bold"),fg="Brown",          text=t_sepa+format_euro2(t_reserve1+t_reserve2)+ "  - Soit remontée de : " +   str(    round(    (t_mt_total-510000)/(590000-510000)  *100   ,2)     )         + "%").grid(row=3,column=4,sticky="ew")

    # TOTALISER LE MONTANT DES ACTIONS AU 1MAI
    cursor.execute("SELECT SUM(cours_1mai*qte_valeur) FROM valeurs")
    x_mt_mai = cursor.fetchone()[0]  # TUPLE DE 1 LIGNE

    # TOTALISER LE MONTANT DES ACTIONS AUJOURD'HUI
    cursor.execute("SELECT SUM(mt_valeur) FROM valeurs")
    x_mt_actions = cursor.fetchone()[0]  # TUPLE DE 1 LIGNE

    # TOTALISER LES PREVISIONS DE FIN D'ANNEE
    cursor.execute("SELECT SUM(mt_31dec) FROM valeurs where qte_valeur>0")
    x_mt_31dec = cursor.fetchone()[0]  # TUPLE DE 1 LIGNE

    #EXTRAIRE LES INFOS DE LA TABLE DES VALEURS
    cursor.execute("SELECT code_valeur,zone,nom_valeur,pc_jour,pc_annee,cours_1janv,cours_achat,cours_1mai,mt_31dec,cours_open,cours_close,qte_valeur,mt_valeur,cur_valeur,jour FROM valeurs ORDER BY pc_jour desc")
    results = cursor.fetchall()

    #AFFICHER LE TITRE FRANCE
    Label(frame_valeurs,font=(VD,12,"bold"),fg="Purple",text=" ──  France  "+"─"*15).grid(row=t_lig,column=0,sticky="w")
    Label(frame_valeurs,font=(VD, 9,"bold"),fg="Orange",text="        Date").grid(row=t_lig,  column=1, sticky="w")
    Label(frame_valeurs,font=(VD, 9,"bold"),fg="Orange",text="% Jour ").grid(row=t_lig,       column=2, sticky="we")
    Label(frame_valeurs,font=(VD, 9,"bold"),fg="Orange",text="  Gain Jour").grid( row=t_lig,  column=3, sticky="w")
    Label(frame_valeurs,font=(VD, 9,"bold"),fg="Orange",text=" Position Jour").grid(row=t_lig,column=4, sticky="we")
    Label(frame_valeurs,font=(VD, 9,"bold"),fg="Orange",text=" │ % Année").grid(row=t_lig,column=9,sticky="w")
    Label(frame_valeurs,font=(VD, 9,"bold"),fg="Orange",text=" │ % Achat").grid(row=t_lig,column=10,sticky="w")

    #BALAYER LES VALEURS FR
    for code_valeur,zone,nom_valeur,pc_jour,pc_annee,cours_1janv,cours_achat,cours_1mai,mt_31dec,cours_open,cours_close,qte_valeur,mt_valeur,cur_valeur,jour in results:

        t_lig = t_lig + 1
        if zone < "G":
            atten = mt_31dec - ( cours_1mai * qte_valeur)  # ATTENDU ENTRE MAI ET 31 DECEMBRE
            #print(nom_valeur,cours_close)
            reali = ( cours_close-cours_1mai) * qte_valeur  # REALISE DEPUIS LE 1ER MAI ??? EN FAIT LE PLUS BAS APRES TRUMP
            mt_close = cours_close * qte_valeur

            #mt_close = cours_close * qte_valeur
            to_reali2 = int(reali / atten * 30)

            Label(frame_valeurs, font=(VD, 8, "bold"), fg=ma_coul(pc_jour, zone, jour),
                  text=f"{(pc_jour):,.2f}" + " % ").grid(row=t_lig, column=2, sticky="e")
            Label(frame_valeurs, font=(VD, 8, "bold"), fg=ma_coul(pc_jour, zone, jour),
                  text=format_euro4(pc_jour * mt_valeur / 100) + "  ").grid(row=t_lig, column=3, sticky="e")
            Label(frame_valeurs, font=(VD, 10, "bold"), fg=ma_coul(pc_jour, zone, jour),
                  text=format_euro4(mt_valeur) + "  │").grid(row=t_lig, column=4, sticky="e")

            # AFFICHAGE AVANCEMENT
            if cours_close > cours_1mai:  # BARRE VERTE
                t_barre = "▓" * to_reali2
                Label(frame_valeurs, font=(VD, 8, "bold"), fg="Green",
                      text=t_barre + " (" + str(to_reali2) + ") (Manque " + format_euro4(
                          mt_31dec - mt_close) + " sur " + format_euro4(mt_31dec) + ")").grid(row=t_lig, column=6, sticky="w")
            else:  # SI RECUL PAR RAPPORT A MAI
                Label(frame_valeurs, font=(VD, 8, "bold"), fg="Red", text="Recul de " + format_euro4(
                    (cours_1mai * qte_valeur) - mt_valeur) + " depuis Mai - Attendus " + format_euro4(mt_31dec)).grid(
                    row=t_lig, column=6, sticky="w")

            # AFFICHER CE QUI RESTE
            to_reali2 = int(reali / atten * 30)
            Label(frame_valeurs,font=(VD,8,"bold"), fg=ma_coul(pc_jour, zone, jour),text=" " * 10 + nom_valeur + " " * 6).grid(row=t_lig, column=0, sticky="w")  # + zone + " "
            Label(frame_valeurs,font=(VD,8,"bold"), fg=ma_coul(pc_jour, zone, jour),text=jour).grid(row=t_lig,     column=1,                                                                                                        sticky="ew")

            t_reste_pc = round(100 * (1 - (mt_close / mt_31dec)), 2)
            if t_reste_pc>10:
                Label(frame_valeurs, font=(VD,10,"bold"), fg="Red",text=str(t_reste_pc ) +"%"    ).grid(row=t_lig, column=8, sticky="e")
            else:
                Label(frame_valeurs, font=(VD,10,"bold"), fg="Green",text=str(t_reste_pc ) +"%"    ).grid(row=t_lig, column=8, sticky="e")

            #AFFICHER LA PROGRESSION ANNEE
            if mt_valeur - (cours_1janv * qte_valeur) > 0:
                Label(frame_valeurs, font=(VD,8), fg="Green",text="│ Année: +" + format_pc(cours_close, cours_1janv)).grid(row=t_lig, column=9, sticky="w")
            else:
                Label(frame_valeurs, font=(VD,8,), fg="Red",  text="│ Année: -" + format_pc(cours_1janv, cours_close)).grid(row=t_lig, column=9, sticky="w")

            #AFFICHER LA PROGRESSION DEPUIS ACHAT
            if mt_valeur - (cours_achat * qte_valeur) > 0:
                Label(frame_valeurs, font=(VD, 8, "bold"), fg="Green", text="│ Nous: +" + format_pc(cours_close, cours_achat)     ).grid(row=t_lig, column=10, sticky="w")
                #Label(frame_valeurs, font=(VD, 8, "bold"), fg="Purple", text="(+" + format_euro4(  (cours_close-cours_1janv) * qte_valeur   )+")").grid(row=t_lig, column=11, sticky="e")

            else:
                Label(frame_valeurs, font=(VD, 8, "bold"), fg="Red",  text="│ Nous: -" + format_pc(cours_achat, cours_close)).grid(row=t_lig, column=10, sticky="w")
                #Label(frame_valeurs, font=(VD, 8, "bold"), fg="Purple", text="(-"       + format_euro4( (cours_1janv - cours_close) * qte_valeur)+")").grid(row=t_lig, column=11, sticky="e")

    #TITRE DES VALEURS US
    t_lig=t_lig+2
    Label(frame_valeurs,font=(VD,12,"bold"),fg="Purple",text=" ──  Etats-Unis  "+"─"*10).grid(row=t_lig,column=0,sticky="w")

    #BALAYER LES VALEURS US
    for code_valeur,zone,nom_valeur,pc_jour,pc_annee,cours_1janv,cours_achat,cours_1mai,mt_31dec,cours_open,cours_close,qte_valeur,mt_valeur,cur_valeur,jour in results:

        #COLONNES DES VALEURS US
        if zone > "G":
            t_lig=t_lig+1
            atten = mt_31dec - (cours_1mai * qte_valeur)  # ATTENDU D ICI LE 31 DECEMBRE  non par rapport au plus haut sur 12 mois
            reali = (cours_close - cours_1mai) * qte_valeur  # REALISE DEPUIS LE 1ER MAI ??? EN FAIT LE PLUS BAS APRES TRUMP
            mt_close = cours_close * qte_valeur
            to_reali2 = int(  reali/atten * 20)
            Label(frame_valeurs,font=(VD,8,"bold"),fg=ma_coul(pc_jour, zone, jour),text=" "*10  + nom_valeur + " "*6).grid(row=t_lig,column=0,sticky="w")  #+ zone + " "
            Label(frame_valeurs,font=(VD,8 ,"bold"),fg=ma_coul(pc_jour, zone, jour),text=jour).grid(row=t_lig, column=1,                                                                                                    sticky="ew")
            Label(frame_valeurs,font=(VD,8 ,"bold"),fg=ma_coul(pc_jour, zone, jour),text=f"{(pc_jour):,.2f}" + " % ").grid(row=t_lig,column=2,sticky="e")
            Label(frame_valeurs,font=(VD,8 ,"bold"),fg=ma_coul(pc_jour, zone, jour),text= format_euro4(pc_jour * mt_valeur / 100) + "  ").grid(row=t_lig, column=3, sticky="e")
            Label(frame_valeurs,font=(VD,10,"bold"),fg=ma_coul(pc_jour, zone, jour),text=format_euro4(mt_valeur) + " │").grid(row=t_lig,column=4,sticky="e")

            #GAINS A CE JOUR DEPUIS MAI   (DIVISE PAR LE NOMBRE DE JOURS)
            if to_reali2>1.3:  # BARRE VERTE
                t_barre = "▓" * to_reali2
                Label(frame_valeurs, font=(VD,8, "bold"), fg="Green",text=t_barre +" ("+str(to_reali2)+") (Manque "+ format_euro4(mt_31dec-(cours_close*qte_valeur))+" sur " +format_euro4(mt_31dec)+")").grid(row=t_lig,column=6,sticky="w")
            else:  # RECUL
                Label(frame_valeurs, font=(VD,8, "bold"), fg="Red",  text="Recul de " + format_euro4(  (cours_1mai * qte_valeur) - mt_valeur) + " depuis Mai - Attendus " + format_euro4(mt_31dec)).grid(row=t_lig,    column=6, sticky="w")

            # AFFICHER CE QUI RESTE
            t_reste_pc = round(100 * (1 - (mt_close / mt_31dec)), 2)
            if t_reste_pc > 10:
                Label(frame_valeurs, font=(VD, 10, "bold"), fg="Red",  text=str(t_reste_pc) + "%").grid(row=t_lig, column=8, sticky="e")
            else:
                Label(frame_valeurs, font=(VD, 10, "bold"), fg="Green",text=str(t_reste_pc) + "%").grid(row=t_lig,column=8, sticky="e")

           #AFFICHER LA PROGRESSION ANNEE
            if mt_valeur - (cours_1janv * qte_valeur) > 0:
                Label(frame_valeurs, font=(VD, 8), fg="Green",text="│ Année: +" + format_pc(cours_close, cours_1janv)).grid(row=t_lig, column=9, sticky="w")
            else:
                Label(frame_valeurs, font=(VD, 8), fg="Red",  text="│ Année: -" + format_pc(cours_1janv, cours_close)).grid(row=t_lig, column=9, sticky="w")

            #AFFICHER LA PROGRESSION DEPUIS ACHAT
            if mt_valeur - (cours_achat * qte_valeur) > 0:
                Label(frame_valeurs, font=(VD, 8, "bold"), fg="Green",text="│ Nous: +" + format_pc(cours_close, cours_achat)).grid(row=t_lig, column=10, sticky="w")
            else:
                Label(frame_valeurs, font=(VD, 8, "bold"), fg="Red",  text="│ Nous: -" + format_pc(cours_achat, cours_close)).grid(row=t_lig, column=10, sticky="w")

    # JOURS OUVRES RESTANT JUSQU'AU AU 31 DEC (VRAIS)
    nb_jm2 = 8 + 22 + 22 + 22 + 22
    t_moyenne_jour = (x_mt_actions-x_mt_mai)/nb_jm

#   MESSAGE D'INFORMATION EN BAS D'ECRAN
    t_message1 = "---"
    t_message2 = "Situation 1er mai : "+format_euro4(x_mt_mai+t_reserve1+t_reserve2) + "  - Objectif : "+format_euro4(x_mt_31dec+   (  t_reserve1*1.03)+(t_reserve2*1.03 )   )
    t_message3 = ("Gains " + format_euro4(x_mt_actions-x_mt_mai) + " en " + str(nb_jm) + (" jours ouvrés, "
       "soit ") + format_euro4((x_mt_actions-x_mt_mai)/nb_jm)+ " par jour -  Tendance dans " +str(nb_jm2)+ " jours : " +
                  format_euro4( x_mt_actions  + t_reserve1 + t_reserve2 + (t_moyenne_jour*nb_jm2)    ))

    # AFFICHER LES MESSAGES
    Label(frame_message,font=(VD,10,"bold"),fg="Brown",text=t_message1).grid(row=t_lig+3,column=0, sticky="we")
    Label(frame_message,font=(VD,10,"bold"),fg="Brown",text=t_message2).grid(row=t_lig+4,column=0, sticky="we")
    Label(frame_message,font=(VD,10,"bold"),fg="Brown",text=t_message3).grid(row=t_lig+5,column=0, sticky="we")

    #REAFFICHAGE EN BOUCLE
    Update_affichage.after(57000, update_label)  # 57 000 = 1 MINUTE

#REAFFICHER
update_label()

#VALIDATION DE LA FENETRE
fenetre.mainloop()
