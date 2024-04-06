Pour télécharger ce projet, vous devez disposer d'une machine virtuelle connectée à internet et de l'outil de versionning git.

Si vous n'avez pas git d'installé, vous pouvez saisir cette commande : ```sudo apt install git```

Depuis votre machine virtuelle, entrez la commande suivante : 

```git clone https://github.com/astr-id/evaldjango.git```

Une fois le projet récupéré, rendez-vous dans le dossier téléchargé en saisissant la commande : ```cd evaldjango```

Lancez ensuite le script d'automatisation de l'installation, de génération d'exemples afin de populer la base de données et de lancement du serveur : ```python3 installation.py```

Vous devriez avoir le serveur qui tourne à la fin de l'exécution du script. Pour s'y connecter, rendez vous à l’adresse suivante et appréciez pleinement les fonctionnalités de l’application de gestion de projet : http://192.168.56.12:8000

Si vous ne parveniez pas à vous y connecter, vous pouvez toujours arrêter le serveur via la commande : ```Ctl + C```
Et ensuite relancer le serveur pour utiliser l'adresse par défaut : ```python3 manage.py runserver```

3 utilisateurs avec chacun un rôle différent sont enregistrés : 

Astrid avec le rôle de responsable.

Audrey avec le rôle de gestionnaire.

Gaëtan avec le rôle d’employé.

Pour ces 3 utilisateurs, le mot de passe est le même, à savoir : password123

Vous voudrez peut-être activer le compte administrateur. Pour ce faire, référez-vous à ce [lien](https://docs.djangoproject.com/en/4.2/intro/tutorial02/#introducing-the-django-admin).
