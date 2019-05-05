"""

verifie si tous les tableaux ne depassent pas une taille limite 
si oui on trie et on repartie le surplus dans les autres 
dans le cas du rubik's cube il y a 6 tableaux de 8 ou 9 faces selon si 
l'on garde les centres ou non
"""

import calcul

def repartition_egal(tab_color,tab_centre, nb):
    #nb : nombre de cases pour chaque faces
    #tab_data : tableau 2d de triplet de couleur (r,g,b) 
    m = 0
    check = False
    while check == False:
        check = True
        tab_indice_depassement = []
        tab_indice_manque = []
        for i in range(0, len(tab_color)):
            if len(tab_color[i]) > nb:
                #indice des faces qui ont trop de cases associes
                tab_indice_depassement.append(i)
                check = False
            elif len(tab_color[i])  < nb:
                #indice des faces qui n ont pas assez de cases associes
                tab_indice_manque.append(i)

        #si la repartition n est pas egale
        if check == False:
            # recupere les tableaux ou il y a du depassement
            tab_copy = []
            reste = []
            for i in range(0, len(tab_indice_depassement)):
                tab_copy.append([])
                tab_copy[i] = tab_color[ tab_indice_depassement[i] ]
                
            #commence le tri
            for i in range(0, len(tab_copy)):
                #tri ascendant sur la distance rgb
                t = tri_fusion(tab_copy[i], tab_centre[  tab_indice_depassement[i] ] )
                tab_color[ tab_indice_depassement[i] ] = t[0:nb]

                #cases en trop a repartir
                reste.extend(t[nb:])
            #print reste
            #repartir le reste
            for i in range(0, len(reste)):
                min = 256
                indice = 0
                for j in range(0, len(tab_indice_manque)):
                    moy = calcul.moyenneRGB(reste[i], tab_centre[ tab_indice_manque[j] ] )
                    if moy < min:
                        min = moy
                        indice = tab_indice_manque[j]
                tab_color[ indice ].append(reste[i])
    return tab_color



def fusion(t1, t2, centre):
    t = []
    size1 = len(t1)
    size2 = len(t2)
    i = 0
    j = 0
    while i < size1 and j < size2:
        if calcul.moyenneRGB(centre,t1[i]) < calcul.moyenneRGB(centre,t2[j]) :
            t.append(t1[i])
            i += 1
        else:
            t.append(t2[j])
            j += 1
    if i == size1:
        t.extend(t2[j:])
    else:
        t.extend(t1[i:])
    return t


def tri_fusion(tab, centre):
    if len(tab) <= 1:
        return tab
    else:
        size = len(tab)
        return fusion( tri_fusion(tab[0:size/2], centre), tri_fusion(tab[size/2:], centre), centre)



    #parcours et choisit pour chaque triplet le centre le plus ressemblant (rgb)
def repartition(tabPref):
    
    fini = False

    #tableau ou sera indique laffectation de chaque triplet avec le centre le plus ressemblant 
    tabFinal = [-1] * len(tabPref)
    compt = 0

    # si 0 le centre i na pas ete affecte si 1 le centre a ete affecte
    tabChoix = [0] * len(tabPref)

    for i in range(0, len(tabPref)):
        print tabPref[i] 
    print "\n"
    
    while fini == False:
        tab = []
        for i in range(0, len(tabPref)):
            #stocke le coin le plus ressemblant avec sa valeur associe a un centre  i   
            tab.append([])
            
        #tableau qui compte le nombre de triplet qui veulent etre associe au centre i
        tabCount = [0] * len(tabPref)
        
        # parcours les colonnes pour chaque coin des centres
        for i in range(0, len(tabPref[0])):
            
            min = 256
            indicelig = 0
            #parcours les lignes pour choisir le plus mieux de lindice i
            for j in range(0, len(tabPref)):
            
                if tabPref[j][i] < min:
                    min = tabPref[j][i]
                    indicelig = j
            tab[indicelig].append( [min, i , indicelig] )
            tabCount[indicelig] += 1


        for i in range(0, len(tabCount)):
            
            #si celui que je check,  na pas de coin centre  attribue 
            if tabFinal[i] == -1:
                
                # si il a un seul meilleur coin et que le coin centre n a pas ete attribue
                if tabCount[i] == 1 and tabChoix[ tab[i][0][1] ] == 0:
                    
                    indicecol = tab[i][0][1]
                    #jenleve la ligne et la colonne du coin que jai check 
                    #et jattribue dans les tableaux
                    for j in range(0, len(tabPref[0])):
                        tabPref[i][j] = 256.
                    for k in range(0, len(tabPref)):
                        tabPref[k][indicecol] = 256.
                    tabFinal[i] = tab[i][0][1]
                    tabChoix[ tabFinal[i] ] = 1
                        
                #si il a plus d un meilleur
                elif tabCount[i] > 1:
                    indicecol = 0
                    min = 256 
                    indice = 0
                    #je choisis le plus petit
                    for k in range(0, len(tab[i])):
                        if tab[i][k][0] < min:
                            min = tab[i][k][0]
                            indicecol = tab[i][k][1]
                            indice = k
                            
                    #et si le coin centre n a pas ete attribue
                    if tabChoix[ tab[i][indice][1] ] == 0:
                        #jenleve la ligne et la colonne du coin que jai check 
                        # et jattribue dans les tableaux
                        for j in range(0, len(tabPref[0])):
                            tabPref[i][j] = 256.
                        for k in range(0, len(tabPref)):
                            tabPref[k][indicecol] = 256.
                        tabFinal[i] = tab[i][indice][1]
                        tabChoix[ tabFinal[i] ] = 1

        
        for i in range(0, len(tabPref)):
            print tabPref[i] 
        print "\n"
        
        #si tous les coin ont ete attribue a un coin centre je sors
        fini = True
        for i in range(0, len(tabFinal)):
            if tabFinal[i] == -1:
                fini = False
    return tabFinal
  