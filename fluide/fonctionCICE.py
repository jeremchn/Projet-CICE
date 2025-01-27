#%%
#import pandas as pd
#output = r"C:\Users\Marion\AppData\Local\Programs\Python\Python312\sidequests\profil.csv"
#input = r"C:\Users\Marion\AppData\Local\Programs\Python\Python312\sidequests\e471-il.csv"

def modif_fichier_airfoil (file, output):
    """ La fonction prend en entrée un fichier airfoil .csv
    et extrait la surface d'airfoil
    PAS D'OUTPUT, la fonction écrit dans le fichier output
    utilise pandas
    """
    with open(file, 'r') as file:
        lines = file.readlines()[8:70]
    
    with open(output, 'w') as file:
        file.writelines(lines)

    df = pd.read_csv(output, sep=',')
    df_mod = df / 100
    df_mod.to_csv(output, sep='\t', index=False, header=True)
    #print( df_mod)

def modif_fichier(file, output):
    """La fonction retire l'entête 16 premières lignes et les 3 dernières colonnes
    au passage la fonction crée un fichier output .txt
    
    file : fichier a modifier
    output : fichier de sortie (.csv)
    
    utilise pandas"""
 #supprimer les 16 premières lignes
    with open(file, 'r') as file:
        lines = file.readlines()[16:]  # Ignorer les 16 premières lignes

    # supprimer les 3 dernières colonnes
    processed_lines = []
    for line in lines:
        columns = line.split()  # Diviser la ligne en colonnes (par espace ou tabulation)
        if len(columns) > 3:    # S'assurer qu'il y a au moins 3 colonnes
            processed_line = " ".join(columns[:-3])  # Supprimer les 3 dernières colonnes
            processed_lines.append(processed_line + "\n")  # Ajouter un retour à la ligne

    with open(output, 'w') as file:
        file.writelines(processed_lines)

def re_corde (DFchordangl, uinf, vrot, nu):
    """ Calcule le Reynolds en fonction de la corde
    chordangl : fichier .dat (rayon / cordes / angles)
    N : nombre de points
    uinf : vitesse de l'air
    vrot : vitesse de rotation de l'éolienne
    nu : viscosité cinématique
    """
    index = DFchordangl.index
    r = DFchordangl[index [0]] # rayon
    c = DFchordangl[index[0]] # corde
    U = np.sqrt(uinf**2 + (vrot * r)**2)
    re = r * c * U / nu
    c75 = c * 0.75
    re75 = r * c75 * U / nu
    return (re, re75)

def graph_re(x,re):
    """ Fonction qui trace le graphique du Reynolds en fonction de la corde
    x : corde
    re : Reynolds
    """
    plt.plot(x,re)
    plt.xlabel('Corde')
    plt.ylabel('Reynolds')
    plt.title('Reynolds en fonction de la corde')
    plt.show()
