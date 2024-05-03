# Procédure de tests :

## EmergencyManager
- L'EmergencyManger dispose de ses propres tests unitaires pour les fonctions internes (contenus dans les fichiers service) (avec JUnit).
- Le logiciel dispose aussi de tests permettant de tester le correct fonctionnement de la communication avec une API concernant les fonctions de base associés à certains objets (Caserne, Equipement, Emlployé...). Ce test permet à la fois de contrôler la communication EM* => API et le fonctionnement correct de l'API au passage.


Ces tests unitaires sont réalisés automatiquement lors du build de l'EmergencyManager, en cas d'échec, le build ne se fait pas. L'interprétation des logs du test permettra de trouver l'origine du problème.
En plus de ces tests unitaires, lors du déploiement d'une nouvelle version, les logs sont inspectées afin de se rendre compte de tout problème le plus rapidement possible. Notamment, lors du lancement de l'applicatif, la configuration est affichée permettant de la relire une dernière fois afin de se rendre compte de toute erreur.
De plus, un répertoire `logs` contient les historiques des logs, dans ces fichiers est ressensé les logs de niveau WARN ou supérieur (WARN, ERROR).

## API
