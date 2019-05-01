
"""
data : donnees d un rubiks cube scanne
tab : tableau ou on va regrouper les cases du meme indice dans un tableau 

Pour chaque i nombre de cases d'une (0 a 8 sauf le 4 le centre)
	pour chaque j face du rubiks (0 a 5)
		regrouper toutes les cases i des faces j dans un tableau
		tab[i].append(data[j][i])

Nous avons 8 tableaux de 6 cases d'un meme indice (toutes les cases 1, toutes les cases 2, etc)


Pour chaque tab[i] (i de 0 a len(tab) ) 
	Appliquer le repartition sur chaque tableau 
	(on va calculer une distance de couleur entre chaque case et les centres)
	(puis affecter les cases aux centres qui sont les plus proches en terme de distance)

a la fin afficher l affectation et regarder le taux d'erreur
"""

from donnees_des_tests.data_rubiksofficiel import data_rubiksofficiel
from donnees_des_tests.data_rubiksponce import data_rubiksponce
from donnees_des_tests.data_rubiksdamiennoir import data_rubiksdamiennoir
from donnees_des_tests.data import data
from donnees_des_tests.data_turned import data_turned
from test import repartition
import matplotlib.pyplot as plt
from test import rgb255to01, t255to01, donnees
from compare_avec_centre_rgb import compare_centre_rgb


    

def tri_groupement_de_cases(data):
    x, y, color, c, max_color = donnees(data)

    tab = []
    tab_affectation = []
    nb_cases = len(data[0])
    nb_faces = len(data)
    centre = []
    for i in range(0,nb_cases):
        tab.append([])
        
        if i < 6:
            tab_affectation.append([])
            centre.append(data[i][4])
        
    for i in range(0, nb_cases):
        for j in range(0, nb_faces):
            tab[i].append(data[j][i])
            

            

    #pour chaque groupe de cases lancer la repartition
    for i in range(0, len(tab)):
        
        tabPref = compare_centre_rgb(data, tab[i])
        """
        for j in range(0, len(tabPref)):
            print tabPref[j]
        print "\n"
        """
        tabChoix = repartition(tabPref)
        
        #affecte les cases au centre associe
        for j in range(0,len(tabChoix)):
            tab_affectation[ tabChoix[j] ].append( tab[i][j] ) 

  
    fig = plt.figure(0)
    for i in range(0,len(tab_affectation) ):
        for j in range (0 , len(tab_affectation[i])):
            plt.scatter(i, 10 + j* 5, s=800, marker='o', c=  t255to01(tab_affectation[i][j], max_color) )

        plt.scatter(i, 0, s=800, marker='o', c= t255to01(centre[i],max_color) )

        
    plt.show()    

tri_groupement_de_cases(data_rubiksdamiennoir)
