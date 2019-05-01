


"""
calcul la distance (moyenne rgb) entre les valeurs du tableau et tous les centres 
retourne un tableau qui associe a chaque valeur de tab une comparaison avec les 
6 centres
"""

from test import moyenneRGB, diffRGB


def compare_centre_rgb(data,tab):

    centre = []
    for i in range(0, len(data)):
        centre.append(data[i][4])


    tabPref = []
    for i in range(0, len(tab)):
        tabPref.append([])
        
    #parcours tout le tableau
    for i in range(0, len(tab)):
        #parcours les 6 centres
        for j in range(0, len(centre)):
            tabPref[i].append( moyenneRGB(tab[i], centre[j]) )

            
    return tabPref
