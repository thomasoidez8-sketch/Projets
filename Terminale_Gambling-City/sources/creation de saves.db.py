import sqlite3

base=sqlite3.connect('saves.db')
curseur=base.cursor()

requete="DROP TABLE save"
curseur.execute(requete)

requete="""CREATE TABLE IF NOT EXISTS saveOeuvre(
            Id INTEGER PRIMARY KEY,
            IdOeuvre INTEGER,
            Nom VARCHAR(255),
            Artiste VARCHAR(255),
            Musée VARCHAR(255),
            Prix INTEGER,
            Largeur INTEGER,
            Hauteur INTEGER)"""
curseur.execute(requete)

requete="""CREATE TABLE IF NOT EXISTS saveOeuvrePerdu(
            IdOeuvre INTEGER PRIMARY KEY)"""
curseur.execute(requete)

requete_table="""
CREATE TABLE IF NOT EXISTS save(
	IdDescription INTEGER PRIMARY KEY,
	jeton INTEGER,
	dette INTEGER,
	succes_1 BOOLEAN,
	succes_2 BOOLEAN,
    succes_3 BOOLEAN,
    succes_4 BOOLEAN,
    succes_5 BOOLEAN,
    succes_6 BOOLEAN,
    succes_7 BOOLEAN,
    succes_8 BOOLEAN
    );"""
requete_insertion = """INSERT INTO save (jeton,dette,succes_1,succes_2,succes_3,succes_4,succes_5,succes_6,succes_7,succes_8) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
curseur.execute(requete_table)
valeur = (100,0,False,False,False,False,False,False,False,False)
curseur.execute(requete_insertion, valeur)
base.commit()

