<!DOCTYPE HTML>
<html lang="fr">
    <head>
        <title>Informations client</title>
        <meta charset="utf-8">
        <link rel="stylesheet" href="Projet_style.css">
    </head>
<body>
    <div class="title_infos">Informations</div>

    <div class="Zone_infos">
        <form method="post" action="informations.php">
            <font face="Britannic">
            <p>Saisissez votre adresse email :</p>
            <input class="adresse" type="text" name="adresse" placeholder="Votre_adresse@email.com">
            <br>
            <p>Votre numéro de carte bleue :<input type="text" name="numéro" placeholder="XXXX-XXXX-XXXX-XXXX">
            Date d'expiration :<input type="text" name="date" placeholder="XX/XXXX">
            CCV :<input type="text" name="code" placeholder="XXX"></p>
            <p>Version : <select>
                <option value="option 1">Windows</option>
                <option value="option 2">IOS</option>
                <option value="option 3">Linux</option>
            </select></p>
            <input type="submit" name="valider" value="Valider">
            <?php
                $adresse_email="Invalide";
                $num="Invalide";
                $date_expiration="Invalide";
                $CCV="Invalide";
                // Définition des variables
                if (isset($_POST['valider']) AND $_POST['valider']=='Valider') {
                    // On vérifie si l'on clique sur le bouton "Valider"
                    $email=$_POST['adresse'];
                    $numéro=$_POST['numéro'];
                    $date=$_POST['date'];
                    $code=$_POST['code'];
                    // On récupère les données entrées par l'utilisateur
                    if ($email=="") {
                        echo "<br>Merci de rentrer une adresse.";
                    }
                    else{
                        $adresse_email="Valide";
                    };

                    if ($numéro=="") {
                        echo "<br>Merci de rentrer un numéro.";
                    }
                    else{
                        $num="Valide";
                    };

                    if ($date=="") {
                        echo "<br>Merci de rentrer une date d'expiration.";
                    }
                    else{
                        $date_expiration="Valide";
                    };

                    if ($code=="") {
                        echo "<br>Merci de rentrer un code.";
                    }
                    else{
                        $CCV="Valide";
                    };
                    // On vérifie si l'utilisateur n'a pas laissé des cases blanches
                };
                if ($adresse_email=="Valide" AND $num=="Valide" AND $date_expiration=="Valide" AND $CCV=="Valide") {
                    header("location: Téléchargement.html");
                    exit();
                }
                // Si les infos de l'utilisateur sont valides il est redirigé vers la page de téléchargement
            ?>
        </font>
        </form>
    </div>
    <button class="Bouton_repos" onclick="location.href='Boutique.html'" onmouseover="fonc_in()" onmouseout="fonc_out()" id="Bouton">Retour</button>

</body>
<script src="JavaScript.js"></script>