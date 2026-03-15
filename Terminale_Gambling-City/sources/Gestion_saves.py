import sqlite3,sources.Enchere as Enchere

base=sqlite3.connect('saves.db')
curseur=base.cursor()

class Gestion_sauvegarde():
    def __init__(self):
        self.bourseJetons = 0
        self.dette = 0
        self.succes_1 = False
        self.succes_2 = False
        self.succes_3 = False
        self.succes_4 = False
        self.succes_5 = False
        self.succes_6 = False
        self.succes_7 = False
        self.succes_8 = False

    def load(self):
        requete_load = """SELECT jeton,dette,succes_1,succes_2,succes_3,succes_4,succes_5,succes_6,succes_7,succes_8 FROM save"""
        (self.bourseJetons,self.dette,
         self.succes_1,self.succes_2,self.succes_3,
         self.succes_4,self.succes_5,self.succes_6,
         self.succes_7,self.succes_8) = curseur.execute(requete_load).fetchone()
        
    def save(self):
        requete_sauvegarde = """UPDATE save
        SET jeton = ?,dette = ?,
        succes_1 = ?,succes_2 = ?,succes_3 = ?,succes_4 = ?,succes_5 = ?,succes_6 = ?,succes_7 = ?,succes_8 = ? WHERE IdDescription = 1"""
        curseur.execute(requete_sauvegarde,(self.bourseJetons,self.dette,
                                            self.succes_1,self.succes_2,self.succes_3,
                                            self.succes_4,self.succes_5,self.succes_6,
                                            self.succes_7,self.succes_8))
        base.commit()

    def reset(self):
        requete_reset = """DELETE
                            FROM saveOeuvre"""
        curseur.execute(requete_reset)
        requete_reset = """DELETE
                            FROM saveOeuvrePerdu"""
        curseur.execute(requete_reset)
        requete_reset = """UPDATE save
        SET jeton = '100',dette = '0',
        succes_1 = 0,succes_2 = 0,succes_3 = 0,succes_4 = 0,succes_5 = 0,succes_6 = 0,
        succes_7 = 0,succes_8 = 0 WHERE IdDescription = 1
        """
        curseur.execute(requete_reset)
        base.commit()
        self.load()

def saveOeuvre(dicoOeuvre):
    ajout=True
    requete="""SELECT IdOeuvre FROM saveOeuvre"""
    curseur.execute(requete)
    for element in curseur.fetchall():
        if element[0]==dicoOeuvre["id"]:
            ajout=False
    if ajout:
        requete="""INSERT INTO saveOeuvre(IdOeuvre,Nom,Artiste,Musée,Prix,Largeur,Hauteur)
                    VALUES (?,?,?,?,?,?,?)"""
        curseur.execute(requete,(dicoOeuvre["id"],dicoOeuvre["nom"],dicoOeuvre["artiste"],
                                dicoOeuvre["musée"],dicoOeuvre["prix"],dicoOeuvre["tailleImg"][0],
                                dicoOeuvre["tailleImg"][1]))
        
def loadOeuvre():
    lst=[]
    requete="""SELECT IdOeuvre,Nom,Artiste,Musée,Prix,Largeur,Hauteur FROM saveOeuvre"""
    curseur.execute(requete)
    listeSave=curseur.fetchall()
    for elemnt in listeSave:
        lst.append({'id':elemnt[0],'nom':elemnt[1],'artiste':elemnt[2],'musée':elemnt[3],'image':Enchere.nomImg(elemnt[1]),'prix':elemnt[4],'tailleImg':(elemnt[5],elemnt[6])})
    return lst
        
def saveOeuvrePerdu(id):
    ajout=True
    requete="""SELECT IdOeuvre FROM saveOeuvrePerdu"""
    curseur.execute(requete)
    for element in curseur.fetchall():
        if element[0]==id:
            ajout=False
    if ajout:
        requete="""INSERT INTO saveOeuvrePerdu(IdOeuvre)
                    VALUES (?)"""
        curseur.execute(requete,(id,))

def loadOeuvrePerdu():
    lst=[]
    requete="""SELECT IdOeuvre FROM saveOeuvrePerdu"""
    curseur.execute(requete)
    listeSave=curseur.fetchall()
    for elemnt in listeSave:
        lst.append(elemnt[0])
    return lst