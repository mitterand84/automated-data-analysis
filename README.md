# automated-data-analysis
Cet outil permet de télécharger un fichier Excel contenant des données de transactions,  d'analyser ces données, de générer un rapport PDF et d'envoyer ce rapport par email.  Les utilisateurs peuvent également ajouter des pièces jointes supplémentaires à l'email
Description:
-----------
Cette plateforme permet de télécharger un fichier Excel contenant des données de transactions, d'analyser ces données, de générer un rapport PDF et d'envoyer ce rapport par email. 
Les utilisateurs peuvent également ajouter des pièces jointes supplémentaires à l'email.

Fonctionnalités:
---------------
1- Authentification: Les utilisateurs doivent se connecter pour accéder à la plateforme.
2- Téléchargement de fichier Excel: Les utilisateurs peuvent uploader un fichier Excel contenant les données de transactions.
3- Analyse des données: Les données du fichier Excel vont subit une analyse exploratoire des données(dans la stricte pédagogie de la data science) puis générer des graphiques et des statistiques.
4- Génération de rapport PDF: Un rapport PDF est généré automatiquement à partir des résultats de la Data Analyst.
5- Envoi par email: Le rapport PDF peut être envoyé par email à un ou plusieurs destinataires, avec des pièces jointes supplémentaires si besoin.

Prérequis:
---------
les bibliothèques ci-dessous doivent être installées pour le bon fonctionnement de l'outil:

	-  Python 3.x
	-  Flask
	-  Flask-Mail
	-  Pandas
	-  Matplotlib
	-  FPDF
ils sont presents dans le fichier requirements.txt

Installation:
------------
1- Créez et activez un environnement virtuel:
	- sur windows venv\Scripts\activate
 	- sur linux: source venv/bin/activate

2- Installez les dépendances:

	pip install -r requirements.txt

Configuration:
-------------
1- Flask-Mail: Configurez les paramètres de votre serveur SMTP dans mon_app.py:

	app.config['MAIL_SERVER'] = 'votre adresse de serveur SMTP'
	app.config['MAIL_PORT'] = 587
	app.config['MAIL_USE_TLS'] = True
	app.config['MAIL_USERNAME'] = 'votre email'
	app.config['MAIL_PASSWORD'] = 'votre mot de passe'
	app.config['MAIL_DEFAULT_SENDER'] = 'votre email'


2- Clés secrètes: Définissez une clé secrète pour Flask:
	app.secret_key = "votre-cle-secrete"

Utilisation:
-----------
1- Démarrer le serveur Flask via le terminal:
	python app.py

2- Accéder à la plateforme:
   Ouvrez votre navigateur et allez à l'adresse http://127.0.0.1:5000

3- Se connecter:
	voici les identifiants par defaut pour vous connecter:

	Nom d'utilisateur: admin
	Mot de passe: admin

4- Télécharger un fichier pdf généré:

	Cliquez sur "Parcourir" pour sélectionner un fichier Excel.
	Entrez les adresses email des destinataires, séparées par des virgules.
	Ajoutez des pièces jointes supplémentaires si nécessaire.
	Cliquez sur "Générer le rapport et envoyer par email".

5- Recevoir le rapport:

	Les destinataires recevront un email contenant le rapport PDF et les pièces jointes supplémentaires.

6- Structure du projet

	- mon_app.py: Le fichier principal contenant le code Flask.
	- templates/: Dossier contenant les templates HTML.
	- static/xlsx/: Dossier pour les fichiers Excel téléchargés.
	- static/pdf/: Dossier pour les rapports PDF générés.

7- Contribuer
	Les contributions sont les bienvenues! Veuillez ouvrir une issue pour discuter de ce que vous aimeriez changer.

8- Licence
	Voir le fichier LICENSE pour plus de détails.
