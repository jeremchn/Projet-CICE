#%%  BIBLIOTHEQUES +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

# %% LECTURE DES FICHIER PROFILS +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
nb_profil = 1
Lp = [] #liste des profils utilisés (pour l'instant 1 seul)
filename = 'profil' #racine du nom des fichiers .txt
 

for i in range (1, nb_profil+1):
    j = str(i)
    nom_fichier_profil = filename + j + '.dat'

     #Lecture du fichier ligne par ligne pour obtenire une liste correcte
    with open(nom_fichier_profil, 'r') as file:
        lines = file.readlines()

    # Traiter les lignes pour extraire les données
    data = []
    for line in lines:
        values = line.split()  # Diviser par espace ou un autre séparateur
        data.append([float(v) for v in values])  # Convertir en float

    Lp.append (np.array(data)) # lp[i] correspond a un array de chaque fichier
    #Lp[0][0] renvoie sous forme de liste la première ligne du fichier 1

#print(Lp [0][0])
# print (Lp)
#%% AFFICHAGE PLOT (juste pour le fun)
array = Lp[0]
x = [array [i][0]for i in range (len(array))]
y = [array [i][1]for i in range (len(array))]

plt.plot (x,y)
plt.show ()

#%% LECTURE DU FICHIER CORDES/ANGLES DE VRILLAGE ET PROFILS ASSOCIES ++++++++++++++++++++++++++

C = pd.read_csv('ChordAngle.dat', delim_whitespace=True, header=None)
nbP = len(C)  # Nombre de points (r)
C.columns = ['rayon', 'corde', 'twist']
print(C) 
#print(f'Number of data points (nbP): {nbP}')

#%% CREATION DE LA PALE +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CREATION DE LA BASE DE LA PALE 

# Diamètre de la base de la pale (en mm)
d = 4

# Longueur de la base de la pale (en mm)
# L est initialisé selon vos choix arbitraires dans MATLAB
L = 0.24  # Longueur en mètre
L = L * 1000  # Conversion en millimètres

# Définition des offsets
offsetD = 0

# Création d'une plage de valeurs pour x
x = np.arange(0, 361, 5)  # Équivaut à 0:5:360 en MATLAB

# Construction des points pour les deux sections (C1 et C2) => crée un cylindre 
C1 = np.column_stack([
    d * np.cos(2 * np.pi / 360 * x) - offsetD,
    d * np.sin(2 * np.pi / 360 * x) - offsetD,
    np.zeros(len(x)) - L
])

C2 = np.column_stack([
    d * np.cos(2 * np.pi / 360 * x) - offsetD,
    d * np.sin(2 * np.pi / 360 * x) - offsetD,
    np.full(len(x), L) - L
])

# Construction des profils de la pale
P = [C1, C2]  # Liste contenant les deux profils
print (P)


#%% 2.2 - Création du reste de la pale

nb_point = C.shape[0]  # Nombre de points
offset = 0.25  # Décalage d'un quart de corde
P = P.copy()  # Utilisation de la liste des profils existants (C1 et C2)

# Convert DataFrame C to a numpy array for indexing
C_array = C.to_numpy()

# Boucle sur chaque point
for i in range(nb_point):
    #np_index = int(C_array[i, 3])  # Numéro du profil (adjusting column index as third column is at index 2)
    #if np_index > len(Lp) : print ('erreur indice Lp')
    # pour l'instant il y a  des erreurs d'index liées au fichier mais sinon c ok
    np_index = 1 #temp
    a = 2 * np.pi * C_array[i, 1] / 360  # Angle de vrillage en radians (adjusting to column index 1)
    c = np.diag([1000 * C_array[i, 0], 1000 * C_array[i, 0], 1])  # Matrice de corde en mm (adjust first column index to 0)

    # Ajout de la colonne pour l'emplacement de la section (axe z)
    S = np.column_stack([
        Lp[np_index][:, 0] - offset,
        Lp[np_index][:, 1],
        np.full(Lp[np_index].shape[0], 1000 * C_array[i, 0])  # Emplacement sur l'axe z
    ])

    # Matrice de rotation autour de l'axe z
    Rot = np.array([
        [np.cos(a), np.sin(a), 0],
        [-np.sin(a), np.cos(a), 0],
        [0, 0, 1]
    ])

    # Rotation et homothétie
    transformed_section = S @ c @ Rot
    P.append(transformed_section)

# Exportation des profils dans des fichiers texte
format_spec = '{:4.1f}  {:4.1f}  {:4.1f}\n'

for i, profile in enumerate(P):
    file_name = f"{i+1}.txt"  # Génération du nom de fichier
    with open(file_name, 'w') as file:
        # Écriture des données avec le format spécifié
        for row in profile:
            file.write(format_spec.format(*row))