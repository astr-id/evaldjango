
Avant toute chose vous devez avoir le protocole de communication sécurisé SSH d’installer sur votre ordinateur. Si ce n’est pas le cas, vous devez l’installer suivant votre distribution. Il vous faudra aussi avoir installé Python sur votre machine virtuelle.
Afin de pouvoir déployer notre application de gestion de projet, il convient de télécharger les fichiers correspondants sous forme de d’archive .zip sur GitHub à l’adresse suivante (commit eaa057a) : lien 

Une fois l’archive téléchargée, dézipez-la à l’endroit de votre choix sur le disque dur. Notez bien cet emplacement, il vous resservira plus tard.
Démarrez la machine virtuelle.
Une fois celle-ci en route (vous demandant un mot de passe),nous allons maintenant copier le dossier de votre machine hôte vers la machine virtuelle.
Pour ce faire sur votre machine hôte, saisissez cette commande en remplaçant “monchemin” par le chemin où vous avez précédemment extrait l’archive : 

scp -r monchemin/evaldjango-master osboxes@192.168.56.12:~/

Saisissez le mot de passe de la machine virtuelle : osboxes.org si non modifié.
Vous devriez voir une liste de tous les fichiers qui ont été copiés, comme ceci.

Connectez vous maintenant sur votre machine virtuelle et saisissez le mot de passe depuis la machine hôte : 

ssh osboxes@192.168.56.12

Une fois que vous êtes connecté et donc à la racine de la machine virtuelle, tapez la commande “ls” pour voir les fichiers et dossiers présents. Vous devriez obtenir ceci : 

Rendez-vous dans le dossier evaldjango-master en saisissant : 

cd evaldjango-master/

Une fois dans le dossier, saisissez : 

python3 manage.py makemigrations projetmanagement

Ensuite : 

python3 manage.py migrate

Et enfin :

python3 GenererData.py

Si tout s’est bien déroulé, votre fenêtre de terminal devrait ressembler à ceci : 

Votre base de données est maintenant créée et vous avez quelques données qui ont été insérées en guise d’exemple pour vous montrer ce qu’il est possible de faire avec cette application Django de gestion de projets.
3 utilisateurs avec chacun un rôle différent sont enregistrés : 
Astrid avec le rôle de responsable.
Audrey avec le rôle de gestionnaire.
Gaëtan avec le rôle d’employé.
Pour ces 3 utilisateurs, le mot de passe est le même, à savoir : password123
Vous voudrez peut-être activer le compte administrateur. Pour ce faire, référez-vous à ce lien.
Une fois que vous êtes prêt, nous pouvons démarrer le serveur en saisissant la commande : 

python3 manage.py runserver 0.0.0.0:8000

Enfin, rendez vous à l’adresse suivante et appréciez pleinement les fonctionnalités de l’application de gestion de projet : http://192.168.56.12:8000

N.B. : Si vous avez créé un compte administrateur vous pouvez accéder à la page admin de Django à l’adresse suivante : http://192.168.56.12:8000/admin
