import pygame,sqlite3
from pygame.locals import *
from random import *
import sources.Blackjack as Blackjack

base=sqlite3.connect('baseOeuvres.db')
curseur=base.cursor()

scène=pygame.image.load("data/textures_enchères/enchere_allume.png")
barreJoueur=pygame.image.load("data/textures_enchères/barreVente.png")

police=pygame.font.Font('data/fichiers_additionnels/Crang.ttf',18)
police2=pygame.font.Font('data/fichiers_additionnels/Crang.ttf',25)

vente=False
tempsJoueur=5

jetonsDisponibles=0
mise=0

listePos=[[(40,479),(314,480),(587,480),(861,479)],[(175,505),(450,505),(726,505)],[(40,546),(314,546),(587,546),(861,546)]]
listeAchat=[]
listeAcheteur=[]
nbAcheteur=0
dernierAcheteur=None

class Oeuvre:
    def __init__(self,id,screen):
        resultat=self.recherche(id)
        self.id=id
        self.nom=resultat[0][0]
        self.artiste=resultat[0][1]
        self.musée=resultat[0][2]
        self.importance=resultat[0][3]
        self.image=self.taille(pygame.image.load(nomImg(self.nom)))
        self.nbAcheteur=randint(1*self.importance+2,3+2*self.importance)
        self.rect=self.image.get_rect()
        self.rect.topleft=self.position(screen)
        self.prix=1000*self.importance**2+100*randint(10,50)

    def taille(self,img):
        """Réduit la taille de l'image afin quelle ne dépasse pas 150px X 150px."""
        X=img.get_width()
        Y=img.get_height()
        while X>150 or Y>150:
            X=X//1.1
            Y=Y//1.1
        return pygame.transform.scale(img,(X,Y))
    
    def recherche(self,id):
        """Récupère les informations relatives à l'oeuvre d'index id dans la base de données."""
        requete="""SELECT Oeuvres.Nom, Artistes.Nom, Musées.Nom, Importance FROM Oeuvres
                JOIN Artistes ON Artistes.IdArtiste=Oeuvres.Artiste
                JOIN Musées ON Musées.IdMusée=Oeuvres.Musée
                WHERE IdOeuvre=?"""
        curseur.execute(requete,[id])
        resultat=curseur.fetchall()
        return resultat

    def position(self,screen):
        """Ajuste les coordonnées du sommet haut-gauche de l'image en fonction d'un point central."""
        X=screen.get_width()//2-self.image.get_width()//2
        Y=screen.get_height()//2-self.image.get_height()//2-50
        return (X,Y)

class Place:
    def __init__(self,posX,posY):
        self.coordonnées=(posX,posY)
        self.occupé=False
        self.occupant=None

    def attribution(self,personne):
        if not self.occupé:
            self.occupant=personne
            self.occupé=True
            self.occupant.rect.bottomleft=self.coordonnées

    def desattribution(self):
        if self.occupé:
            self.occupant=None
            self.occupé=False

class Acheteur:
    def __init__(self):
        self.image=pygame.image.load("data/textures_enchères/person.png")
        self.bulle=pygame.image.load("data/textures_enchères/bulle.png")
        self.rect=self.image.get_rect()
        self.rect.bottomleft=(0,0)
        self.seuil=0
        self.prix=0
        self.aProposé=False
        self.timer=Blackjack.Timer()
    
    def affichage(self,screen):
        X=self.rect.bottomleft[0]
        Y=self.rect.bottomleft[1]-self.image.get_height()
        screen.blit(self.image,(X,Y))

    def seuilAchat(self,prixOeuvre,importance):
        self.seuil=prixOeuvre+100*randint(25,65)*importance

    def propositionVente(self,prixVente):
        self.aProposé=False
        if self.seuil>prixVente and prixVente/self.seuil<=(100-randint(0, 50))/100:
            self.aProposé=True
            self.prix=prixVente+choice([100,200,300,400,500])
            return self.prix
        
    def affichageBulle(self,screen):
        X=self.rect.topleft[0]+self.image.get_width()/2-self.bulle.get_width()/2
        Y=self.rect.topleft[1]-self.bulle.get_height()
        screen.blit(self.bulle,(X,Y))
        if self.aProposé:
            Blackjack.affichageTexte(str(self.prix),police,X+20,Y+20,'black',screen)
        else:
            Blackjack.affichageTexte('X',police,X+47,Y+20,'black',screen)


def nomImg(nom):
    """Renvoie le chemin du fichier à partir du nom de l'oeuvre."""
    nomFichier="" 
    for caractère in nom:
        if caractère==" ":
            nomFichier+="_"
        else:
            nomFichier+=caractère
    return f"data/oeuvres/{nomFichier}.png"

def organisation(nb):
    i=nb
    while i!=0:
        x=randint(0,10)
        place=listePlace[x]
        if not place.occupé:
            place.attribution(Acheteur())
            i-=1


oui=Blackjack.Bouton('Oui','Oui',300,300,None,"texte",police2)
non=Blackjack.Bouton('menu','Non',625,300,None,"texte",police2)
retour=Blackjack.Bouton('menu','Retour',450,300,None,"texte",police2)

bouton100=Blackjack.Bouton(100,"data/textures_enchères/+100.png",350,525,"data/bouton_sombre/100_sombre.png",'jeton')
bouton200=Blackjack.Bouton(200,"data/textures_enchères/+200.png",412,525,"data/bouton_sombre/200_sombre.png",'jeton')
bouton300=Blackjack.Bouton(300,"data/textures_enchères/+300.png",474,525,"data/bouton_sombre/300_sombre.png",'jeton')
bouton400=Blackjack.Bouton(400,"data/textures_enchères/+400.png",536,525,"data/bouton_sombre/400_sombre.png",'jeton')
bouton500=Blackjack.Bouton(500,"data/textures_enchères/+500.png",598,525,"data/bouton_sombre/500_sombre.png",'jeton')
listeBouton=[bouton100,bouton200,bouton300,bouton400,bouton500]

timerJoueur=Blackjack.Timer()

listeOeuvre=[]
listePerte=[] # !!!

listePlace=[]
for rangée in listePos:
    for emplacement in rangée:
        listePlace.append(Place(emplacement[0],emplacement[1]))