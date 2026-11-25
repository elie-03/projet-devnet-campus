# Contribuer

Les contributions sont bienvenues : corrections, nouvelles plates-formes, nouveaux gabarits.

1. Créez une branche : `git checkout -b ma-modification`
2. Vérifiez que tout passe : `pytest -v` puis `python run.py --dry-run`
3. Ajoutez un test pour tout nouveau comportement.
4. Ouvrez une *pull request* (demande d'intégration) en décrivant la plate-forme et
   la version IOS utilisées pour vos essais.

Ne publiez jamais d'identifiants, de sauvegardes de configuration réelles ni d'images Cisco.

La branche `main` est protégée : toute modification passe par une pull request dont les tests (CI) doivent être verts.
