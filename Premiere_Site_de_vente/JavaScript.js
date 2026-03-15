function fonc_in(){
	document.querySelector("#Bouton").classList.remove("Bouton_repos")	//Permet au bouton "Accueil" et "Retour" de s'assombrir lorsque l'on passe la souris dessus
	document.querySelector("#Bouton").classList.add("Bouton_activé")	// Fonctionnement : Retire une classe CSS et en rajoute une autre à l'élément associé à l'ID "Bouton"
}
function fonc_out(){
	document.querySelector("#Bouton").classList.remove("Bouton_activé")	//Permet au bouton "Accueil" et "Retour" de s'éclaircir lorsque l'on retire la souris du bouton
	document.querySelector("#Bouton").classList.add("Bouton_repos")
}

function fonc_in2(){
	document.querySelector("#Bouton2").classList.remove("Bouton_repos")  //Permet au bouton "Boutique" de s'assombrir lorsque l'on passe la souris dessus
	document.querySelector("#Bouton2").classList.add("Bouton_activé")
}
function fonc_out2(){
	document.querySelector("#Bouton2").classList.remove("Bouton_activé") //Permet au bouton "Boutique" de s'éclaircir lorsque l'on retire la souris du bouton
	document.querySelector("#Bouton2").classList.add("Bouton_repos")
}

function fonc_in3(){
	document.querySelector("#Bouton3").classList.remove("Bouton_repos")	//Permet au bouton "Guide" de s'assombrir lorsque l'on passe la souris dessus
	document.querySelector("#Bouton3").classList.add("Bouton_activé")
}
function fonc_out3(){
	document.querySelector("#Bouton3").classList.remove("Bouton_activé") //Permet au bouton "Guide" de s'éclaircir lorsque l'on retire la souris du bouton
	document.querySelector("#Bouton3").classList.add("Bouton_repos")
}

function fonc_in_art(){
	document.querySelector("#article").classList.remove("Article")		//Permet au bouton d'achat du jeu de s'assombrir lorsque l'on passe la souris dessus
	document.querySelector("#article").classList.add("Article_activé")
}
function fonc_out_art(){
	document.querySelector("#article").classList.remove("Article_activé") //Permet au bouton d'achat du jeu de s'éclaircir lorsque l'on retire la souris du bouton
	document.querySelector("#article").classList.add("Article")
}

function fonc_in_link(){
	document.querySelector("#link").classList.remove("a")				//Permet au lien de téléchargement de changer de couleur lorsque l'on passe la souris dessus
	document.querySelector("#link").classList.add("a_activé")
}
function fonc_out_link(){
	document.querySelector("#link").classList.remove("a_activé")		//Permet au lien de téléchargement de changer de couleur lorsque l'on retire la souris du bouton
	document.querySelector("#link").classList.add("a")
}