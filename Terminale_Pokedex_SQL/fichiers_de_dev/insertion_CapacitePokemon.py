import sqlite3

pokeBase=sqlite3.connect("pokeBase.db")
curseur=pokeBase.cursor()

numPokemon=int(input("Numéro du Pokémon = "))

nBase=int(input("nb base= "))
nNiveau=int(input("nb niveau = "))
nCTCS=int(input("nb CT/CS = "))

def nomCapaToId(n):
    capacité=[]
    id=[]
    for i in range(n):
        capacité.append(input("Capacité : "))
        requete="""SELECT IdCapacité,Capacité
                FROM Attaques
                WHERE Capacité LIKE ?"""
        curseur.execute(requete,[f'{capacité[i]}%'])
        atk=curseur.fetchall()[0]
        id.append(atk[0])
        print(atk[1])
    return id

def insertion(pkmn,liste,methode,n):
    if methode==2:
        for i in range(n):
            niveau=int(input("Quel niveau ? = "))
            requete="""INSERT INTO CapacitePokemon (NumPokedex,IdCapacité,Methode,Niveau)
                        VALUES
                        (?,?,?,?)"""
            curseur.execute(requete,(pkmn,liste[i],methode,niveau))
            pokeBase.commit()
    else:
        for i in range(n):
            requete="""INSERT INTO CapacitePokemon (NumPokedex,IdCapacité,Methode,Niveau)
                        VALUES
                        (?,?,?,?)"""
            curseur.execute(requete,(pkmn,liste[i],methode,'null'))
            pokeBase.commit()

print("Capacité de base")
capaBase=nomCapaToId(nBase)
insertion(numPokemon,capaBase,1,nBase)
print("Capacité de niveau")
capaNiveau=nomCapaToId(nNiveau)
insertion(numPokemon,capaNiveau,2,nNiveau)
print("Capacité CT/CS")
capaCTCS=nomCapaToId(nCTCS)
insertion(numPokemon,capaCTCS,3,nCTCS)

pokeBase.close()