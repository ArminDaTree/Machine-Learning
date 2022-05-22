# Principe 
A l'aide d'une image où l'utilisateur dessine une suite de chiffres, cet algorithme tente de prédire les chiffres inscrits sur l'image.   
Il s'agit du principe d'un OCR  
# **Sortie de programme**:  
Valeur prédite par le programme  
Liste des probabilités (% de chance que la lettre soit la bonne, selon l'algorithme)  
![alt text](https://github.com/ArminDaTree/Machine-Learning/blob/7f0cc58a46730c5504bc40fbf4cd01fdcbc8129b/digits/digit%20outpout.png)  
# Utilisation
## Recommandations
Je recommande l'ouverture du fichier digits.ipynb dans une application du type google colab  
Il faut alors lancer tous les blocs de codes 1 à 1 (excepté les deux derniers) afin de créer le modèle et de l'entraîner  

## Prédiction 
Si vous souhaitez que votre programme prédit ce qu'il y a d'inscrit sur votre image:  
### Un seul digit:
Un seul chiffre: il faut **IMPERATIVEMENT** que l'image soit de taille 28x28, le nom par défaut est "test.png" (à glisser directement dans le dossier où les fichiers sont). Ce nom peut être changé directement dans le code, la taille de l'image également (ligne 2 de l'avant dernier bloc de code)
### Une suite de chiffres:
Dans ce cas, il faudra utiliser le dernier bloc de code.  
Il faut que l'image soit de hauteur 28, la largeur est arbitraire.  
Le nom par défaut pour l'image est "number.png" mais de même il peut être changé dans le code. (2e ligne du dernier bloc de code)  
Afin de favoriser le bon fonctionnement du programme, merci de séparer nettement vos chiffres, qu'il n'y ait pas de chevauchements par exemple.
