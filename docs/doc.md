# Génération de la Documentation Sphinx

## Prérequis  
Assurez-vous d'avoir Sphinx installé dans votre environnement virtuel.  
Si ce n'est pas déjà fait, activez votre environnement et installez Sphinx :  

```bash
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install sphinx
```

## Génération de la Documentation  

Depuis le dossier `docs/`, exécutez la commande suivante :  

```bash
cd docs
make html
```

Cela générera la documentation dans le dossier `_build/html/`.  
Ouvrez le fichier suivant dans un navigateur pour la consulter :  

```bash
_build/html/index.html
```
