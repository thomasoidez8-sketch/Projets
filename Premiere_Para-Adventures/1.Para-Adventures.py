import pygame
from pygame.locals import *
from random import randint

pygame.init()

# Création de l'écran d'acueuil
fenetre=pygame.display.set_mode((800,600))
pygame.display.set_caption("Para-adventure")
# Création de l'affichage du texte
bulle = pygame.image.load("bulle_texte.png")
bulle = pygame.transform.scale(bulle,(800,100))
carré = pygame.image.load("carré.jpg")
carré = pygame.transform.scale(carré,(250,250))
font=pygame.font.Font('Crang.ttf',16)
huge_font=pygame.font.Font('Crang.ttf',75)
text=""

# Variables
# Déroulement du jeu
avance=0
i=0
recueillement=0
inspection=0
code=0000
masque="non"
clé="non"
# Combat
pv_zombie=30
dfc=3
pv=10
pv_fant=20
arme_choisi="Main"
crucifix=0
arme_secondaire="none"
# Textes
# Intro
text1=font.render("Vous entrez dans l'étrange monde de l'étrange et du surnaturel.",True,'white')
text2=font.render("Souhaitez-vous continuer ? [Oui ; Non] =",True,'white')
# Histoire
text3=font.render("Le paranormal : ce terme désigne un évènement anormal et étrange",True,'white')
text4=font.render("que l'on ne peut expliquer, notamment les phénomènes d'apparition ",True,'white')
text5=font.render("de l'après vie [fantômes, génie] ou encore d'aliens.",True,'white')
text6=font.render("Depuis toujours l'être humain est facsiné par l'inexplicable,",True,'white')
text7=font.render("de tout temps il s'est créé des crétures fantastiques pour donner",True,'white')
text8=font.render("une forme à ses peurs et ses croyances.",True,(255,255,255))
text9=font.render("Je vous propose désormais d'entrer sans plus attendre dans l'inconnu.",True,'white')
# Menu
text10=font.render("Esprits ou Créatures ?",True,'white')
text_fant=font.render("Très bien. Je vous souhaite donc une bonne chasse aux fantômes.",True,'white')
text_mons=font.render("Etendu. Tâchez de revenir vivant.",True,'white')
# Chasse aux fantômes
# Portail
text_cimetière1=font.render("Vous voici devant le cimetière de votre village. En tant qu'amateur du",True,'white')
text_cimetière2=font.render("paranormal vous avez pris quelques appareils et votre caméra avant de ",True,'white')
text_cimetière3=font.render("venir. Souhaitez-vous continuer ?",True,'white')
# Cimetière
text_cimetiere4=font.render("Vous entrez dans le cimetière en refermant le portail derrière vous.",True,'white')
text_cimetiere5=font.render("Souhaitez-vous vous recuellir sur la tombe de votre grand-père avant ?",True,'white')
# Inspection
text_cimetiere6=font.render("Voulez-vous inspecter le cimetière avant de commencer ?",True,'white')
# Commencement
text_choix_debut=font.render("Que souhaiter vous faire pour commencer ?",True,'white')
text_choix_debut1=font.render("Poser des [questions] ou des [appareils] ?",True,'white')
# Questions
text_questions=font.render("Vous trouvez un coin tranquille avec un banc et commencez.",True,'white')
text_questions1=font.render("« Est-ce qu'il y a quelqu'un avec moi ici ce soir ? »",True,'white')
text_questions2=font.render("Le silence... Puis soudain vous entendez un gémissement.",True,'white')
# Dame
text_dame=font.render("Vous apercevez une dame portant une robe blanche semblant pleurer",True,'white')
text_dame1=font.render("près d'une tombe.",True,'white')
text_dame2=font.render("Que fait-elle ici ? Elle n'était pourtant pas là lors de votre inspection",True,'white')
text_dame3=font.render("et vous n'avez pas ententendu le lourd portail s'ouvrir.",True,'white')
text_dame4=font.render("Elle vous semble familière... Aller-la voir ?",True,'white')
# Danger
text_danger=font.render("Vous décidez de vous rapprocher d'elle. Rien ne se passe.",True,'white')
text_danger1=font.render("Vous décidez donc de lui parler et elle se retourne brusquement vers vous",True,'white')
text_danger2=font.render("en vous fixant des yeux. Quelque chose cloche avec elle...",True,'white')
text_danger3=font.render("Vous pensez apercevoir en elle votre grand-mère décédée récemment",True,'white')
text_danger4=font.render(" mais à peine vous ayez le temps de réagir qu'elle se lance vers vous.",True,'white')
text_danger5=font.render("Vous tentez de saisir de quoi riposter. Ne profanez pas les tombes !",True,'white')
text_danger6=font.render("[Barre] en métal d'une tombe ou [branche] ?",True,'white')
text_sauver=font.render("Vous voyez l'espace d'un instant quelque chose s'interposer entre vous",True,'white')
text_sauver1=font.render("et elle. Puis la seconde d'après plus rien. Vous chercher votre caméra",True,'white')
text_sauver2=font.render("pour vous assurez de n'être pas fou. Elle n'a plus de batterie...",True,'white')
# Appareils
text_appareils=font.render("Où souhaitez-vous poser vos appareils ? ",True,'white')
text_appareils1=font.render("Vers le [fond] du cimetière, la [chapelle] ou près des [anciennes] tombes ?",True,'white')
# Chapelle
text_chapelle=font.render("Vous déposez un détecteur EMF et une spiritbox et vous posez quelques",True,'white')
text_chapelle1=font.render("questions et vous attendez.",True,'white')
text_chapelle2=font.render("Souhaitez-vous explorer la chapelle ?",True,'white')
text_chapelle3=font.render("Au bout d'une heure il n'y a toujours rien. Continuer ?",True,'white')
text_chapelle4=font.render("Vous sortez.",True,'white')
text_chapelle_obj1=font.render("Vous trouvez derrière l'autel une vielle croix dorée.",True,'white')
text_chapelle_obj2=font.render("Vous décidez de la prendre pour la nuit.",True,'white')
# Anciennes tombes
text_anciennes=font.render("Vous déposez un détecteur EMF et une spiritbox et vous posez quelques",True,'white')
text_anciennes1=font.render("questions. De manière [calme] ou [provocatrice] ?",True,'white')
# Provoque
text_provoc=font.render("Le vent se lève et l'environnement devient pesant. De nombreux bruits se",True,'white')
text_provoc1=font.render("font entendre. Les esprits sont en colère. Les [affronter] ou [fuir] ?",True,'white')
# Prep
text_prep=font.render("Vous rassemblez votre courage et vos armes, plein de détermination.",True,'white')
# Combat
text_combat=font.render("[Attaque]----[Riposte]",True,'white')
text_pv=font.render("PV = ",True,'white')
text_pv_fant=font.render("PV ennemi =",True,'white')
# Fond
text_fond=font.render("Vous décidez de sortir votre détecteur EMF et vous l'allumez.",True,'white')
text_fond1=font.render("Lorsque vous le pointez vers le mausolé il se met à bipper et clignoter.",True,'white')
text_fond2=font.render("Souhaitez-vous allez voir ?",True,'white')

text_fond_inaccessible=font.render("Vous êtes déjà allez là.",True,'white')
# Mausolé
text_mausolé=font.render("Il n'y a rien ici mis a part une pelle.",True,'white')
text_mausolé1=font.render("Souhaitez-vous la prendre ?",True,'white')

# Monstre
# Maison
text_maison=font.render("Vous vous trouvez devant une vieille maison abandonnée.",True,'white')
text_maison1=font.render("Souhaitez-vous continuer ?",True,'white')
# Salon
text_salon=font.render("Vous arrivez dans le salon.",True,'white')
text_salon1=font.render("Il y a une porte sur le côté. Avancer ou inspecter ?",True,'white')

text_salon2=font.render("Vous trouver une serrure cachée derrière la télévision. Chercher la clé !",True,'white')

text_salon3=font.render("Vous insérez la clé dans la serrure cachée. Une porte dérobée s'ouvre.",True,'white')
text_salon4=font.render("Vous entrez.",True,'white')
# Salle-à-manger
text_salle_a_manger=font.render("Vous vous trouvez dans le réfectoire.",True,'white')
text_salle_a_manger1=font.render("Il y a 2 portes. Avancer ou inspecter ?",True,'white')

text_salle_a_manger2=font.render("Cuisine ou salon ?",True,'white')

text_salle_a_manger3=font.render("Chercher autour de la table ou dans les meubles ?",True,'white')
text_salle_a_manger4=font.render("Il n'y a rien à part de vieux bibelot.",True,'white')
text_salle_a_manger5=font.render("Il y a une suite de chiffres sous les assiettes :",True,'white')
# Cuisine
text_cuisine=font.render("Vous vous trouvez dans la cuisine.",True,'white')
text_cuisine1=font.render("Il y a 2 portes. Avancer ou inspecter ?",True,'white')

text_cuisine2=font.render("Refectoire ou couloir ?",True,'white')

text_cuisine3=font.render("Chercher dans le four, le frigo, l'évier ?",True,'white')
text_cuisine4=font.render("Vous trouvez une tête dans un bocal mais rien d'intéressant.",True,'white')
text_cuisine5=font.render("Vous trouvez une étrange baguette sous les assiettes. Vous la prenez.",True,'white')
text_cuisine5_bis=font.render("Il n'y a plus que des assiettes cassées.",True,'white')
text_cuisine6=font.render("L'odeur venant du four vous empêche de l'ouvrir.",True,'white')
text_cuisine7=font.render("Vous trouvez un coffre-fort. Il y a un code :",True,'white')
text_cuisine8=font.render("Vous trouvez une petite clé.",True,'white')
text_cuisine8_bis=font.render("C'est vide",True,'white')
# Couloir
text_couloir=font.render("Vous vous trouvez dans le couloir.",True,'white')
text_couloir1=font.render("Il y a 3 portes. Avancer ou inspecter ?",True,'white')

text_couloir2=font.render("Cuisine, chambre ou douche ?",True,'white')

text_couloir3=font.render("Vous ne trouvez rien ici.",True,'white')
# Salle de bain
text_douche=font.render("Vous vous trouvez dans la salle de bain.",True,'white')
text_douche1=font.render("Il y a une porte derrière vous. Avancer ou inspecter ?",True,'white')

text_douche2=font.render("Vous prenez un masque filtrant dans la trousse de secours.",True,'white')
text_douche2_bis=font.render("Il n'y a plus rien.",True,'white')
# Chambre
text_chambre=font.render("Vous vous trouvez dans la chambre.",True,'white')
text_chambre1=font.render("Il y a une porte derrière vous. Avancer ou inspecter ?",True,'white')

text_chambre2=font.render("Vous trouvez une épée sous le lit. Vous la prenez.",True,'white')
text_chambre3=font.render("Il n'y a plus rien ici ... sauf un nounours.",True,'white')
# Cave
text_cave=font.render("Vous arrivez dans une vieille cave. Un revenant apparait.",True,'white')
text_cave1=font.render("Vous utilisez la baguette que vous avez trouvé et une vive lumière en sort.",True,'white')
text_cave2=font.render("Vous vous échappez.",True,'white')
text_cave3=font.render("Vous brandissez ensuite votre épée et eliminez le zombie.",True,'white')

text_cave4=font.render("Baguette ou épée ?",True,'white')
# Fins
# Chasse aux fantômes
text_game_over=huge_font.render("Game over",True,'red')
text_fin=huge_font.render("Fin",True,'green')
text_fin_peur=font.render("Vous ne pouvez pas renoncer comme ça maintenant !",True,'red')
text_fin_peur2=font.render("Reprenez-vous ! Ne laissez pas la peur vous envahir !",True,'red')

text_fin_abandon=font.render("Vous vous dites que ce n'est peut-être ni le jour ni le lieu pour cela.",True,'orange')
text_fin_abandon2=font.render("La prochaine fois assurer de ne pas être déranger...si il y a une prochaine fois...",True,'orange')

text_bonne_fin=font.render("Suite à cette expérience vous avez perdu toute envie de recommencer.",True,'green')
text_bonne_fin1=font.render("Vous êtes parti chercher des fleurs pour les tombes de vos grands-parents.",True,'green')
text_bonne_fin2=font.render("Qu'est-ce qui à pu vider la batterie de votre caméra ?",True,'green')

text_fin_chap=font.render("Vous avez attendu toute la nuit dans la chapelle en vain.",True,'orange')
text_fin_chap1=font.render("Il n'y a pas d'esprits dans la chapelle, c'est un sanctuaire sacré.",True,'orange')

text_fin_calm=font.render("Après avoir attendu 1h vous décidé de rentrer.",True,'green')
text_fin_calm1=font.render("Alors que vous rangiez vos affaires vous entendez",True,'green')
text_fin_calm2=font.render("dans votre spiritbox une voix.",True,'green')
text_fin_calm3=font.render("De plus sur l'enregistrement de votre caméra on aperçoit",True,'green')
text_fin_calm4=font.render("un feu follet entre 2 tombes.",True,'green')

text_fin_mort=font.render("Vous êtes des leur maintenant.",True,'red')
text_fin_mort1=font.render("Vous n'avez pas profané une tombe j'espère ?",True,'red')

text_bad_ending=font.render("Vous êtes heureux ?",True,'green')
text_bad_ending1=font.render("Vous avez triomphé mais ...",True,'green')
text_bad_ending2=font.render("A quel prix ?",True,'green')
# Monstre
text_fin_zombie=font.render("Vous n'avez pas pu vous défendre.",True,'red')
text_fin_zombie1=font.render("Rest in peace.",True,'red')

text_fin_fuite=font.render("Vous profitez de l'éblouissement du zombie pour fuir.",True,'orange')
text_fin_fuite1=font.render("Vous courez aussi loin que vous pouvez.",True,'orange')

text_fin_tresor=font.render("Une fois le zombie retourné parmi les morts.",True,'green')
text_fin_tresor1=font.render("Vous vous rendez au fond de la cave.",True,'green')
text_fin_tresor2=font.render("Vous y trouvez un grand trésor. La richesse est vôtre !",True,'green')
# Fonctions
# Début du jeu
def intro():
    global text
    global avance
    accueil=pygame.image.load("fond_menu.jpg")
    accueil=pygame.transform.scale(accueil, (800,600))
    fenetre.blit(accueil,(0,0))
    logo=pygame.image.load("logo.png")
    logo = pygame.transform.scale(logo, (375,400))
    fenetre.blit(logo,(200,0))
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text1,(25,515))
    fenetre.blit(text2,(25,540))
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (425, 540))
    if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(text)
                    if text=="oui":
                        avance=1
                    elif text=="non":
                        pygame.quit()
                    text = ""
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += pygame.key.name(event.key)
    return avance

def histoire():
    global i
    global avance
    grimoire=pygame.image.load("grimoire.jpg")
    grimoire=pygame.transform.scale(grimoire,(800,600))
    fenetre.blit(grimoire,(0,0))
    fenetre.blit(bulle,(0,500))
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        i+=1
    if i == 0:
        fenetre.blit(text3,(25,515))
        fenetre.blit(text4,(25,540))
        fenetre.blit(text5,(25,565))
    elif i == 1:
        fenetre.blit(text6,(25,515))
        fenetre.blit(text7,(25,540))
        fenetre.blit(text8,(25,565))
    elif i == 2:
        fenetre.blit(text9,(25,540))
    else:
        i=0
        avance = 2
        return avance

def menu():
    global avance
    global text
    global i
    global pv
    global pv_fant
    pv=10
    pv_fant=10
    menu=pygame.image.load("menu.jpg")
    menu=pygame.transform.scale(menu,(800,500))
    fenetre.blit(menu,(0,0))
    fenetre.blit(bulle,(0,500))
    if i == 0:
        fenetre.blit(text10,(25,515))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 540))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="esprits":
                    i=1
                elif text=="creatures":
                    i=2
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    elif i == 1:
        trace=pygame.image.load("trace.png")
        trace=pygame.transform.scale(trace,(400,400))
        fenetre.blit(trace,(375,75))
        fenetre.blit(text_fant,(25,515))
        if event.type == pygame.KEYDOWN and event.key == K_RETURN:
            i=0
            avance="esprits"
    elif i == 2:
        trace=pygame.image.load("trace.png")
        trace=pygame.transform.scale(trace,(400,400))
        fenetre.blit(trace,(115,40))
        fenetre.blit(text_mons,(25,515))
        if event.type == pygame.KEYDOWN and event.key == K_RETURN:
            i=0
            avance="monstre"
    return avance and pv and pv_fant

# Chasse aux fantômes
cimetiere=pygame.image.load("cimetière.jpg")
def portail():
    global avance
    global text
    portail=pygame.image.load("portail.jpg")
    portail=pygame.transform.scale(portail,(800,500))
    fenetre.blit(portail,(0,0))
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_cimetière1,(25,515))
    fenetre.blit(text_cimetière2,(25,540))
    fenetre.blit(text_cimetière3,(25,565))
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (400, 565))
    if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(text)
                    if text=="oui":
                        avance="cimetière"
                    elif text=="non":
                        avance="peur"
                    text = ""
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += pygame.key.name(event.key)
    return avance

def cimetière():
    global avance
    global text
    global recueillement
    global cimetiere
    cimetiere=pygame.transform.scale(cimetiere,(800,500))
    fenetre.blit(cimetiere,(0,0))
    fenetre.blit(bulle,(0,500))
    tombe=pygame.image.load("tombe.png")
    tombe=pygame.transform.scale(tombe,(200,200))
    fenetre.blit(carré,(275,175))
    fenetre.blit(tombe,(300,200))
    fenetre.blit(text_cimetiere4,(25,515))
    fenetre.blit(text_cimetiere5,(25,540))
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (25, 565))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            print(text)
            if text=="oui":
                recueillement=1
                avance="cimetière1"
            elif text=="non":
                recueillement=2
                avance="cimetière1"
            text = ""
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += pygame.key.name(event.key)
    return avance,recueillement,cimetiere

def Inspection():
    global cimetiere
    global avance
    global text
    global inspection
    fenetre.blit(cimetiere,(0,0))
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_cimetiere6,(25,515))
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (25, 540))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            print(text)
            if text=="oui":
                inspection=1
                avance="cimetière2"
            elif text=="non":
                inspection=0
                avance="cimetière2"
            text = ""
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += pygame.key.name(event.key)
    return avance,inspection

def commencement():
    global text
    global avance
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_choix_debut,(25,515))
    fenetre.blit(text_choix_debut1,(25,540))
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (25, 565))
    appareil=pygame.image.load("appareil.png")
    appareil=pygame.transform.scale(appareil,(200,200))
    question=pygame.image.load("question.png")
    question=pygame.transform.scale(question,(200,200))
    fenetre.blit (carré,(125,175))
    fenetre.blit (carré,(425,175))
    fenetre.blit(appareil,(450,200))
    fenetre.blit(question,(150,200))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            print(text)
            if text=="questions":
                avance="questions"
            elif text=="appareils":
                avance="appareils"
            text = ""
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += pygame.key.name(event.key)
    return avance

def questions():
    global avance
    fenetre.blit(cimetiere,(0,0))
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_questions,(25,515))
    fenetre.blit(text_questions1,(25,540))
    fenetre.blit(text_questions2,(25,565))
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        avance="dame"
    return avance
        
def dame():
    global avance
    global i
    global text
    fenetre.blit(bulle,(0,500))
    fenetre.blit(cimetiere,(0,0))
    dame=pygame.image.load("dame.png")
    dame=pygame.transform.scale(dame,(200,200))
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        i+=1
    if i == 0:
        fenetre.blit(carré,(275,175))
        fenetre.blit(dame,(300,200))
        fenetre.blit(text_dame,(25,515))
        fenetre.blit(text_dame1,(25,540))
    elif i == 1 and inspection == 0:
        avance="abandon"
        i=0
    elif i >= 1 and inspection == 1: 
        fenetre.blit(carré,(275,175))
        fenetre.blit(dame,(300,200))
        fenetre.blit(text_dame2,(25,515))
        fenetre.blit(text_dame3,(25,540))
        fenetre.blit(text_dame4,(25,565))
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (480, 565))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            print(text)
            if text=="oui":
                i=0
                avance="danger"
            elif text=="non":
                i=0
                avance="peur"
            text = ""
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += pygame.key.name(event.key)
        return avance

def danger():
    global arme_choisi
    global i
    global avance
    global text
    global pv_fant
    fenetre.blit(bulle,(0,500))
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        i+=1
    if i==0:
        fenetre.blit(text_danger,(25,515))
        fenetre.blit(text_danger1,(25,540))
        fenetre.blit(text_danger2,(25,565))
    elif i==1:
        fenetre.blit(carré,(275,175))
        dame_cours=pygame.image.load("dame_cours.png")
        dame_cours=pygame.transform.scale(dame_cours,(200,200))
        fenetre.blit(dame_cours,(300,200))
        fenetre.blit(text_danger3,(25,515))
        fenetre.blit(text_danger4,(25,540))
    elif i==2 and recueillement==1:
        fenetre.blit(carré,(275,175))
        réunion=pygame.image.load("réunion.png")
        réunion=pygame.transform.scale(réunion,(200,200))
        fenetre.blit(réunion,(300,200))
        fenetre.blit(text_sauver,(25,515))
        fenetre.blit(text_sauver1,(25,540))
        fenetre.blit(text_sauver2,(25,565))
    elif i==3 and recueillement==1:
        avance="retrouvaille"
        i=0
    elif i>=2 and recueillement==2:
        fenetre.blit(text_danger5,(25,515))
        fenetre.blit(text_danger6,(25,540))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 565))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="barre":
                    arme_choisi="Barre"
                    pv_fant=15
                    avance="combat"
                    i=0
                elif text=="branche":
                    arme_choisi="Branche"
                    pv_fant=10
                    avance="combat"
                    i=0
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    return avance and arme_choisi and pv_fant

def appareils():
    global text
    global avance
    fenetre.blit(cimetiere,(0,0))
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_appareils,(25,515))
    fenetre.blit(text_appareils1,(25,540))
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (25, 565))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            print(text)
            if text=="fond":
                avance="fond"
            elif text=="chapelle":
                avance="chapelle"
            elif text=="anciennes":
                avance="anciennes"
            text = ""
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += pygame.key.name(event.key)
    return avance

def chapelle():
    global i
    global text
    global avance
    Chapelle=pygame.image.load("chapelle.jpg")
    Chapelle=pygame.transform.scale(Chapelle,(800,500))
    fenetre.blit(Chapelle,(0,0))
    fenetre.blit(bulle,(0,500))
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        i+=1
    if i==0:
        fenetre.blit(text_chapelle,(25,515))
        fenetre.blit(text_chapelle1,(25,540))
    elif i>=1:
        fenetre.blit(text_chapelle3,(25,515))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 540))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="oui":
                    avance="fin_chap"
                    i=0
                elif text=="non":
                    avance="sortir"
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    return avance

def ancienne():
    global avance
    global text
    global pv_fant
    pv_fant=15
    ancienne_tombes=pygame.image.load("ancienne_tombes.jpg")
    ancienne_tombes=pygame.transform.scale(ancienne_tombes,(800,500))
    fenetre.blit(ancienne_tombes,(0,0))
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_anciennes,(25,515))
    fenetre.blit(text_anciennes1,(25,540))
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (25, 565))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            print(text)
            if text=="calme":
                avance="calme"
            elif text=="provocatrice":
                avance="provoque"
            text = ""
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += pygame.key.name(event.key)
    return avance and pv_fant

def provoque():
    global avance
    global text
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_provoc,(25,515))
    fenetre.blit(text_provoc1,(25,540))
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (25, 565))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            print(text)
            if text=="fuir":
                avance="peur"
            elif text=="affronter":
                avance="preparation"
            text = ""
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += pygame.key.name(event.key)
    return avance

def prep():
    global avance
    esprits=pygame.image.load("esprits_en_colère.png")
    esprits=pygame.transform.scale(esprits,(800,300))
    fenetre.blit(esprits,(0,200))
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_prep,(25,515))
    if event.type == pygame.KEYDOWN:
        avance="combat2"
    return avance

def combat():
    global dfc
    global pv
    global pv_fant
    global avance
    global text
    global arme_choisi
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_combat,(25,515))
    aff_pv=font.render(f"{pv:02d}",True,'white')
    fenetre.blit(aff_pv,(500,515))
    fenetre.blit(text_pv,(450,515))
    aff_pv_fant=font.render(f"{pv_fant:02d}",True,'white')
    fenetre.blit(aff_pv_fant,(750,515))
    fenetre.blit(text_pv_fant,(610,515))
    # Combat
    if arme_choisi=="Barre":
        atk=randint(0,8)
        atk_fant=randint(2,8)
        dfc=2
    elif arme_choisi=="Branche":
        atk=randint(0,4)
        atk_fant=randint(3,6)
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (25, 565))
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="attaque":
                    pv_fant=pv_fant-atk
                    pv=pv-(atk_fant-dfc)
                elif text=="riposte":
                    pv=pv-randint(1,2)
                    pv_fant=pv_fant-randint(1,2)
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    if pv <=0:
        avance="perdu"
    if pv_fant <=0:
        avance="gagner"

def fond():
    global avance
    global text
    img_fond=pygame.image.load("fond_cimetière.jpg")
    img_fond=pygame.transform.scale(img_fond,(800,500))
    fenetre.blit(img_fond,(0,0))
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_fond,(25,515))
    fenetre.blit(text_fond1,(25,540))
    fenetre.blit(text_fond2,(25,565))
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (325, 565))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            print(text)
            if text=="oui":
                avance="mausolé"
            elif text=="non":
                avance="appareils"
            text = ""
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += pygame.key.name(event.key)

def mausolé():
    global avance
    global arme_choisi
    global text
    img_mausolé=pygame.image.load("mausolé.jpg")
    img_mausolé=pygame.transform.scale(img_mausolé,(800,500))
    fenetre.blit(img_mausolé,(0,0))
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_mausolé,(25,515))
    fenetre.blit(text_mausolé1,(25,540))
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (25, 565))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            print(text)
            if text=="oui":
                arme_choisi="pelle"
                avance="appareils"
            elif text=="non":
                avance="appareils"
            text = ""
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += pygame.key.name(event.key)
    return arme_choisi

def combat_2():
    global dfc
    global pv
    global pv_fant
    global avance
    global text
    global arme_choisi
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_combat,(25,515))
    aff_pv=font.render(f"{pv:02d}",True,'white')
    fenetre.blit(aff_pv,(500,515))
    fenetre.blit(text_pv,(450,515))
    aff_pv_fant=font.render(f"{pv_fant:02d}",True,'white')
    fenetre.blit(aff_pv_fant,(750,515))
    fenetre.blit(text_pv_fant,(610,515))
    # Combat
    if arme_choisi=="pelle":
        atk=randint(0,10)
        atk_fant=randint(2,8)
        dfc=2
    elif arme_choisi=="Main":
        atk=randint(0,2)
        atk_fant=randint(3,6)
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (25, 565))
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="attaque":
                    pv_fant=pv_fant-atk
                    pv=pv-(atk_fant-dfc)
                elif text=="riposte":
                    pv=pv-randint(1,2)
                    pv_fant=pv_fant-randint(1,2)
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    if pv <=0:
        avance="perdu"
    if pv_fant <=0:
        avance="gagner"

# Monstre

def maison():
    global avance
    global text
    global code
    global masque
    global clé
    global arme_secondaire
    global arme_choisi
    arme_choisi="Main"
    arme_secondaire="none"
    masque="non"
    clé="non"
    code=randint(0,9999)
    img_maison=pygame.image.load("maison.jpg")
    img_maison=pygame.transform.scale(img_maison,(800,500))
    fenetre.blit(img_maison,(0,0))
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_maison,(25,515))
    fenetre.blit(text_maison1,(25,540))
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (25, 565))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            print(text)
            if text=="oui":
                avance="salon"
            elif text=="non":
                avance="peur"
            text = ""
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += pygame.key.name(event.key)
    return code and masque and arme_choisi and arme_secondaire

def salon():
    global avance
    global text
    global i
    global clé
    img_salon=pygame.image.load("salon.jpg")
    img_salon=pygame.transform.scale(img_salon,(800,500))
    fenetre.blit(img_salon,(0,0))
    if i==0:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_salon,(25,515))
        fenetre.blit(text_salon1,(25,540))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 565))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="avancer":
                    avance="salle-a-manger"
                    i=0
                elif text=="inspecter":
                    i=1
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    elif i==1:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_salon2,(25,515))
        if clé=="non":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                i=0
        elif clé=="oui":
            fenetre.blit(bulle,(0,500))
            fenetre.blit(text_salon3,(25,515))
            fenetre.blit(text_salon4,(25,540))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                i=0
                avance="cave"

def salle_a_manger():
    global avance
    global text
    global i
    img_salle_a_manger=pygame.image.load("salle-a-manger.jpg")
    img_salle_a_manger=pygame.transform.scale(img_salle_a_manger,(800,500))
    fenetre.blit(img_salle_a_manger,(0,0))
    if i==0:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_salle_a_manger,(25,515))
        fenetre.blit(text_salle_a_manger1,(25,540))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 565))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="avancer":
                    i=1
                elif text=="inspecter":
                    i=2
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    elif i==1:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_salle_a_manger2,(25,515))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 540))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="salon":
                    avance="salon"
                    i=0
                elif text=="cuisine":
                    avance="cuisine"
                    i=0
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    elif i==2:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_salle_a_manger3,(25,515))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 540))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="meubles":
                    i=3
                elif text=="table":
                    i=4
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    elif i==3:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_salle_a_manger4,(25,515))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            i=0
    elif i==4:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_salle_a_manger5,(25,515))
        aff_code=font.render(f"{code:04d}",True,'white')
        fenetre.blit(aff_code,(25,540))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            i=0

def cuisine():
    global avance
    global text
    global i
    global arme_choisi
    global code
    global clé
    img_cuisine=pygame.image.load("cuisine.jpg")
    img_cuisine=pygame.transform.scale(img_cuisine,(800,500))
    fenetre.blit(img_cuisine,(0,0))
    if i==0:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_cuisine,(25,515))
        fenetre.blit(text_cuisine1,(25,540))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 565))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="avancer":
                    i=1
                elif text=="inspecter":
                    i=2
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    elif i==1:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_cuisine2,(25,515))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 540))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="refectoire":
                    avance="salle-a-manger"
                    i=0
                elif text=="couloir":
                    avance="couloir"
                    i=0
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    elif i==2:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_cuisine3,(25,515))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 540))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="frigo":
                    i=3
                elif text=="evier":
                    i=4
                elif text=="four":
                    i=5
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    elif i==3:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_cuisine4,(25,515))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            i=0
    elif i==4:
        fenetre.blit(bulle,(0,500))
        if arme_choisi=="baguette":
            fenetre.blit(text_cuisine5_bis,(25,515))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                i=0
        else:    
            fenetre.blit(text_cuisine5,(25,515))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                arme_choisi="baguette"
                i=0
    elif i==5 and masque=="non":
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_cuisine6,(25,515))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            i=0
    elif i==5 and masque=="oui":
        if clé=="oui":
            fenetre.blit(bulle,(0,500))
            fenetre.blit(text_cuisine8_bis,(25,515))
        else:
            fenetre.blit(bulle,(0,500))
            fenetre.blit(text_cuisine7,(25,515))
            text_surface = font.render(text, True, (255, 255, 255))
            fenetre.blit(text_surface, (25, 540))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(text)
                    if text==str(code):
                        i=6
                    else:
                        i=0
                    text = ""
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += pygame.key.name(event.key)
    elif i==6:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_cuisine8,(25,515))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            clé="oui"
            i=0
    return clé

def couloir():
    global avance
    global text
    global i
    img_couloir=pygame.image.load("couloir.jpg")
    img_couloir=pygame.transform.scale(img_couloir,(800,500))
    fenetre.blit(img_couloir,(0,0))
    if i==0:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_couloir,(25,515))
        fenetre.blit(text_couloir1,(25,540))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 565))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="avancer":
                    i=1
                elif text=="inspecter":
                    i=2
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    elif i==1:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_couloir2,(25,515))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 540))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="cuisine":
                    avance="cuisine"
                    i=0
                elif text=="chambre":
                    avance="chambre"
                    i=0
                elif text=="douche":
                    avance="salle-de-bain"
                    i=0
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    elif i==2:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_couloir3,(25,515))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            i=0

def salle_de_bain():
    global avance
    global text
    global i
    global masque
    img_douche=pygame.image.load("salle_de_bain.jpg")
    img_douche=pygame.transform.scale(img_douche,(800,500))
    fenetre.blit(img_douche,(0,0))
    if i==0:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_douche,(25,515))
        fenetre.blit(text_douche1,(25,540))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 565))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="avancer":
                    avance="couloir"
                elif text=="inspecter":
                    i=1
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    elif i==1:
        if masque=="non":
            fenetre.blit(bulle,(0,500))
            fenetre.blit(text_douche2,(25,515))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                masque="oui"
                i=0
        elif masque=="oui":
            fenetre.blit(bulle,(0,500))
            fenetre.blit(text_douche2_bis,(25,515))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                i=0
    return masque

def chambre():
    global avance
    global i
    global text
    global arme_secondaire
    img_chambre=pygame.image.load("chambre.jpg")
    img_chambre=pygame.transform.scale(img_chambre,(800,500))
    fenetre.blit(img_chambre,(0,0))
    if i==0:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_chambre,(25,515))
        fenetre.blit(text_chambre1,(25,540))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 565))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="avancer":
                    avance="couloir"
                elif text=="inspecter":
                    i=1
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    elif i==1:
        fenetre.blit(bulle,(0,500))
        if arme_secondaire=="épée":
            fenetre.blit(text_chambre3,(25,515))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                i=0
        else:
            fenetre.blit(text_chambre2,(25,515))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                i=0
                arme_secondaire="épée"
    return arme_secondaire

def cave():
    global avance
    global i
    global text
    global arme_secondaire
    global arme_choisi
    img_cave=pygame.image.load("cave.jpg")
    img_cave=pygame.transform.scale(img_cave,(800,500))
    fenetre.blit(img_cave,(0,0))
    fenetre.blit(carré,(275,175))
    zombie=pygame.image.load("zombie.png")
    zombie=pygame.transform.scale(zombie,(200,200))
    fenetre.blit(zombie,(300,200))
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            i+=1
    if i==0:
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_cave,(25,515))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            i=1
    if i==1 and arme_choisi=="baguette" and arme_secondaire=="none":
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_cave1,(25,515))
        fenetre.blit(text_cave2,(25,540))
    elif i==2 and arme_choisi=="baguette" and arme_secondaire=="none":
        avance="fuite"
        i=0
    if i>=1 and arme_choisi=="baguette" and arme_secondaire=="épée":
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_cave4,(25,515))
        text_surface = font.render(text, True, (255, 255, 255))
        fenetre.blit(text_surface, (25, 540))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="baguette":
                    avance="baguette"
                    i=0
                elif text=="epee":
                    avance="epee"
                    i=0
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)

def baguette():
    global avance
    global i
    global text
    global arme_secondaire
    global arme_choisi
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_cave1,(25,515))
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        i+=1
    if i==1 and arme_secondaire=="épée": 
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_cave3,(25,515))
    if i==2:
        avance="fin_tresor"
        i=0

def épée():
    global avance
    global i
    global text
    global arme_secondaire
    global arme_choisi
    global pv
    global pv_zombie
    atk=randint(0,10)
    atk_zombie=randint(0,5)
    fenetre.blit(bulle,(0,500))
    fenetre.blit(text_combat,(25,515))
    aff_pv=font.render(f"{pv:02d}",True,'white')
    fenetre.blit(aff_pv,(500,515))
    fenetre.blit(text_pv,(450,515))
    aff_pv_zombie=font.render(f"{pv_zombie:02d}",True,'white')
    fenetre.blit(aff_pv_zombie,(750,515))
    fenetre.blit(text_pv_fant,(610,515))
    # Combat
    atk=randint(0,10)
    atk_zombie=randint(3,8)
    text_surface = font.render(text, True, (255, 255, 255))
    fenetre.blit(text_surface, (25, 565))
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                if text=="attaque":
                    pv_zombie=pv_zombie-atk
                    pv=pv-(atk_zombie-dfc)
                elif text=="riposte":
                    pv=pv-randint(1,2)
                    pv_zombie=pv_zombie-randint(1,2)
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += pygame.key.name(event.key)
    if pv <=0:
        avance="fin_zombie"
    if pv_zombie <=0:
        avance="fin_tresor"

# Fins
def fin_peur():
    global avance
    fenetre.fill('black')
    fenetre.blit(text_game_over,(150,100))
    fenetre.blit(text_fin_peur,(125,250))
    fenetre.blit(text_fin_peur2,(120,300))
    cam=pygame.image.load("caméra.png")
    cam=pygame.transform.scale(cam,(200,200))
    fenetre.blit(cam,(250,350))
    if event.type == pygame.KEYDOWN and event.key == K_RETURN:
        avance=2
    return avance

def fin_abandon():
    global avance
    fenetre.fill('black')
    fenetre.blit(text_game_over,(150,100))
    fenetre.blit(text_fin_abandon,(70,250))
    fenetre.blit(text_fin_abandon2,(5,300))
    voiture=pygame.image.load("voiture.png")
    voiture=pygame.transform.scale(voiture,(200,200))
    fenetre.blit(voiture,(280,350))
    if event.type == pygame.KEYDOWN and event.key == K_RETURN:
        avance=2
    return avance

def bonne_fin():
    global avance
    fenetre.fill('black')
    fenetre.blit(text_fin,(325,100))
    fenetre.blit(text_bonne_fin,(50,250))
    fenetre.blit(text_bonne_fin1,(10,300))
    bouquet=pygame.image.load("bouquet.png")
    bouquet=pygame.transform.scale(bouquet,(200,200))
    fenetre.blit(bouquet,(300,350))
    fenetre.blit(text_bonne_fin2,(125,550))   
    if event.type == pygame.KEYDOWN and event.key == K_RETURN:
        avance=2
    return avance

def fin_chapelle():
    global avance
    global i
    i=0
    if avance =="sortir":
        fenetre.blit(bulle,(0,500))
        fenetre.blit(text_chapelle4,(25,515))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            i+=1
        if i==1:
            avance="dame"
            i=0
    elif avance=="fin_chap":
        fenetre.fill('black')
        fenetre.blit(text_game_over,(150,100))
        fenetre.blit(text_fin_chap,(100,250))
        fenetre.blit(text_fin_chap1,(60,300))
        croix=pygame.image.load("crucifix.png")
        croix=pygame.transform.scale(croix,(200,200))
        fenetre.blit(croix,(275,375))
        if event.type == pygame.KEYDOWN and event.key == K_RETURN:
            avance=2
    return avance

def calme():
    global avance
    fenetre.fill('black')
    fenetre.blit(text_fin,(325,100))
    fenetre.blit(text_fin_calm,(150,250))
    fenetre.blit(text_fin_calm1,(125,300))
    fenetre.blit(text_fin_calm2,(225,325))
    fenetre.blit(text_fin_calm3,(105,375))
    fenetre.blit(text_fin_calm4,(225,400))
    feu=pygame.image.load("feu follet.png")
    feu=pygame.transform.scale(feu,(200,200))
    fenetre.blit(feu,(300,400))
    if event.type == pygame.KEYDOWN and event.key == K_RETURN:
        avance=2
    return avance

def game_over():
    global avance
    fenetre.fill('black')
    fenetre.blit(text_game_over,(150,100))
    fenetre.blit(text_fin_mort,(240,275))
    crane=pygame.image.load("crane.png")
    crane=pygame.transform.scale(crane,(200,200))
    fenetre.blit(crane,(280,375))
    fenetre.blit(text_fin_mort1,(175,550)) 
    if event.type == pygame.KEYDOWN and event.key == K_RETURN:
        avance=2
    return avance

def bad_ending():
    global avance
    fenetre.fill('black')
    fenetre.blit(text_fin,(325,100))
    fenetre.blit(text_bad_ending,(300,250))
    fenetre.blit(text_bad_ending1,(275,300))
    fenetre.blit(text_bad_ending2,(335,350))
    sortie=pygame.image.load("sortie.png")
    sortie=pygame.transform.scale(sortie,(200,200))
    fenetre.blit(sortie,(300,400))
    if event.type == pygame.KEYDOWN and event.key == K_RETURN:
        avance=2
    return avance

def fin_zombie():
    global avance
    fenetre.fill('black')
    fenetre.blit(text_game_over,(150,100))
    fenetre.blit(text_fin_zombie,(225,275))
    cerveau=pygame.image.load("cerveau.png")
    cerveau=pygame.transform.scale(cerveau,(200,200))
    fenetre.blit(cerveau,(280,325))
    fenetre.blit(text_fin_zombie1,(300,550)) 
    if event.type == pygame.KEYDOWN and event.key == K_RETURN:
        avance=2

def fuite():
    global avance
    fenetre.fill('black')
    fenetre.blit(text_game_over,(150,100))
    fenetre.blit(text_fin_fuite,(120,275))
    baguette=pygame.image.load("baguette.png")
    baguette=pygame.transform.scale(baguette,(200,200))
    fenetre.blit(baguette,(280,325))
    fenetre.blit(text_fin_fuite1,(180,550)) 
    if event.type == pygame.KEYDOWN and event.key == K_RETURN:
        avance=2

def fin_tresor():
    global avance
    fenetre.fill('black')
    fenetre.blit(text_fin,(325,100))
    fenetre.blit(text_fin_tresor,(150,250))
    fenetre.blit(text_fin_tresor1,(200,300))
    tresor=pygame.image.load("trésor.png")
    tresor=pygame.transform.scale(tresor,(200,200))
    fenetre.blit(tresor,(300,350))
    fenetre.blit(text_fin_tresor2,(125,550))   
    if event.type == pygame.KEYDOWN and event.key == K_RETURN:
        avance=2
    return avance

# BOUCLE INFINIE
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
    
# Jeu
        if avance==0:
            intro()

        elif avance==1:
            histoire()

        elif avance==2:
            menu()

        elif avance=="esprits":
            portail()
        
        elif avance=="cimetière":
            cimetière()

        elif avance=="cimetière1":
            Inspection()

        elif avance=="cimetière2":
            commencement()

        elif avance=="questions":
            questions()

        elif avance=="dame":
            dame()

        elif avance=="danger":
            danger()

        elif avance=="appareils":
            appareils()

        elif avance=="chapelle":
            chapelle()

        elif avance=="anciennes":
            ancienne()

        elif avance=="provoque":
            provoque()

        elif avance=="combat":
            combat()

        elif avance=="preparation":
            prep()

        elif avance=="fond":
            fond()

        elif avance=="mausolé":
            mausolé()

        elif avance=="combat2":
            combat_2()

    # Monstre
        elif avance=="monstre":
            maison()

        elif avance=="salon":
            salon()

        elif avance=="salle-a-manger":
            salle_a_manger()

        elif avance=="cuisine":
            cuisine()

        elif avance=="couloir":
            couloir()

        elif avance=="salle-de-bain":
            salle_de_bain()

        elif avance=="chambre":
            chambre()

        elif avance=="cave":
            cave()

        elif avance=="baguette":
            baguette()

        elif avance=="epee":
            épée()

    # Fins
    # Monstre
        elif avance=="fin_zombie":
            fin_zombie()

        elif avance=="fin_tresor":
            fin_tresor()

        elif avance=="fuite":
            fuite()

    # Chasse aux fantômes
        elif avance=="peur":
            fin_peur()

        elif avance=="abandon":
            fin_abandon()

        elif avance=="retrouvaille":
            bonne_fin()

        elif avance=="calme":
            calme()
        
        elif avance=="perdu":
            game_over()
        
        elif avance=="gagner":
            bad_ending()

        elif avance=="sortir" or "fin_chap":
            fin_chapelle()
    
    pygame.display.flip()