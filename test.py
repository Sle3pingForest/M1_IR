'''
This code draws Rubik's cube unfoldings with raw RGB data

         | 10 11 12 |
         | 13 14 15 |
         | 16 17 18 |
------------------------------------------
20 21 22 | 00 01 02 | 40 41 42 | 50 51 52
23 24 25 | 03 04 05 | 43 44 45 | 53 54 55
26 27 28 | 06 07 08 | 46 47 48 | 56 57 58
------------------------------------------
         | 30 31 32 |
         | 33 34 35 |
         | 36 37 38 |
'''

import matplotlib.pyplot as plt
import numpy as np

# given a side index and a facet index, return x,y coordinates of the corresponding unfolding
def coord2(s,f):
    x,y = [[0,0],[0,30],[-30,0],[0,-30],[30,0],[60,0]][s]
    x += (f% 3)*10
    y -= (f//3)*10
    return x,y

# retourne les huits combinaisons de triplets possibles en fonction des centres
def couleurCoin(data):
    tab = []
    for i in range(0,8):
        tab.append([])
    """
    tab[0].append(data[0][4])
    tab[0].append(data[1][4])
    tab[0].append(data[2][4])
    """
    tab[0].extend((data[0][4], data[1][4] , data[2][4]))
    tab[1].extend((data[0][4], data[1][4] , data[4][4]))
    tab[2].extend((data[0][4], data[2][4] , data[3][4]))
    tab[3].extend((data[0][4], data[3][4] , data[4][4]))

    tab[4].extend((data[5][4], data[1][4] , data[2][4]))
    tab[5].extend((data[5][4], data[1][4] , data[4][4]))
    tab[6].extend((data[5][4], data[2][4] , data[3][4]))
    tab[7].extend((data[5][4], data[3][4] , data[4][4]))

    return tab

def couleurArete(data):
    tab = []
    for i in range(0,12):
        tab.append([])

    tab[0].extend((data[1][4],data[0][4]))
    tab[1].extend((data[2][4],data[0][4]))
    tab[2].extend((data[3][4],data[0][4]))
    tab[3].extend((data[4][4],data[0][4]))
    tab[4].extend((data[1][4],data[4][4]))
    tab[5].extend((data[1][4],data[2][4]))
    tab[6].extend((data[1][4],data[5][4]))
    tab[7].extend((data[2][4],data[5][4]))
    tab[8].extend((data[2][4],data[3][4]))
    tab[9].extend((data[3][4],data[5][4]))
    tab[10].extend((data[3][4],data[4][4]))
    tab[11].extend((data[4][4],data[5][4]))
    return tab

def tabAreteCouleur(data):
    tab = []
    for i in range(0,12):
        tab.append([])
    tab[0].extend((data[1][7],data[0][1]))
    tab[1].extend((data[2][5],data[0][3]))
    tab[2].extend((data[3][1],data[0][7]))
    tab[3].extend((data[4][3],data[0][5]))
    tab[4].extend((data[1][5],data[4][1]))
    tab[5].extend((data[1][3],data[2][1]))
    tab[6].extend((data[1][1],data[5][1]))
    tab[7].extend((data[2][3],data[5][5]))
    tab[8].extend((data[2][7],data[3][3]))
    tab[9].extend((data[3][7],data[5][7]))
    tab[10].extend((data[3][5],data[4][7]))
    tab[11].extend((data[4][5],data[5][3]))
    return tab

def tabCoinCouleur(data):
    tabCoin = []
    for k in range(0,8):
        tabCoin.append([])
        
    tabCoin[0].extend((data[0][0], data[1][6], data[2][2])) 
    tabCoin[1].extend((data[0][2], data[1][8], data[4][0]))
    tabCoin[2].extend((data[0][6], data[2][8], data[3][0]))
    tabCoin[3].extend((data[0][8], data[3][2], data[4][6]))
    tabCoin[4].extend((data[3][8], data[4][8], data[5][6])) 
    tabCoin[5].extend((data[1][2], data[4][2], data[5][0]))
    tabCoin[6].extend((data[1][0], data[2][0], data[5][2]))
    tabCoin[7].extend((data[2][6], data[3][6], data[5][8]))
    return tabCoin


def voisinHaut(i):
    
    if i==0 or i==2 or i==4 or i== 5: return 1
    elif i==1: return 5
    elif i==3: return 0

def voisinDroite(i):
    if i==0 or i==1 or i==3: return 4
    elif i==2: return 0 
    elif i==4: return 5
    elif i==5: return 2

def voisinGauche(i): 
    if i==0 or i==1 or i==3: return 2
    elif i==2: return 5
    elif i==4: return 0
    elif i==5: return 4

def voisinBas(i): 
    if i==0 or i==2 or i==4 or i==5: return 3
    elif i==1: return 0
    elif i==3: return 5

# assemble x,y coordinates and sticker colors into three arrays
def donnees(data):
    x, y, color, color_true, group_color = [], [], [], [], []
    max_reading = 0
    for side in data:
        for facet in side:
            for reading in facet:
                max_reading = max(max_reading, reading)

    for s, side in enumerate(data):
        for f, (r,g,b) in enumerate(side):
            [tx,ty] = coord2(s, f)
            x.append(tx)
            y.append(ty)
            color.append([round(r)/round(max_reading), round(g)/round(max_reading), round(b)/round(max_reading)])
            if f == 4:
	     color_true.append([r, g, b])
    return x,y,color, color_true, max_reading




    
# draw the unfolding / TA PARTIE A FINIR NAM GROSAc
def draw(data):
    x, y, color, c, max_color = donnees(data)
   
    n = 9
    m = 6
   
    color_center = []
    tab_coeff = {}
    for k in range(0,6):
      color_center.append([])


  
    compteur = 0
    
    for s, side in enumerate(data):
        for f, (r,g,b) in enumerate(side):
	  indice = 0
	  size = len(c)
	  
	  v = '#{:02x}{:02x}{:02x}'.format( 200, 200 , 254 )
	  min_color = int(v[1:], 16)
	  for i in range(0,size):#parcour 6 cote
           
            cfR =abs(c[i][0]-r)
            cfG =abs(c[i][1]-g)
            cfB =abs(c[i][2]-b)
            tab_coeff[s*9+f] = cfR
	  color_center[indice].append( [r,g,b] )
          if (f == 6 and s == 3):
            print r 

	  #print indice
         
    tab_coeff = sorted(tab_coeff.iteritems(), key=lambda (k,v): (v,k))
    #print tab_coeff

  
    test_coeff =[]
    for k in tab_coeff:
        i = int(k[0] / 9)
        j = k[0]%9
        test_coeff.append(data[i][j])

    color_center = test_coeff
    #print c
    tamere = []
    tonpere = []
    for k in range(0,6):
      tonpere.append([])
    for i in range (0, len(c)):
        tamere.append( [ round(c[i][0])/68,  round(c[i][1]) / 68, round(c[i][2])/68] )
            
        

    
    for i in range(0,len(c) ):
        
        plt.scatter(i, 0, s=800, marker='s', c=tamere[i])
        p = 5
       
        for j in range(0, len(test_coeff) ):
            """
            p += 5
            #print ' COULEUR SIDE ',  c[i], '  liste facet: ', color_center[i], '\n'
            #print len(color_center) , "    "  , i   , "    " , len(color_center[i]) , "   " , j , " rgb   " , color_center[i][j][1], "  " , color_center[i][j][0] , "  " , color_center[i][j][2]
            tonpere[i].append(  [ round(color_center[i][j][0])/68,  round(color_center[i][j][1]) / 68, round(color_center[i][j][2])/68] )

            xplacer = i
            yplacer = j;
            if (j > 9 ):
                xplacer = i +0.5
                yplacer = j - 60
            """
            yplacer = j;
            #print " tamere " ,  test_coeff[i][0] , test_coeff[i][0] , test_coeff[i][0]
            tonpere.append( [ round(test_coeff[j][0])/68,  round(test_coeff[j][1]) / 68, round(test_coeff[j][2])/68 ] )
            plt.scatter(i, yplacer + 5 + p , s=800, marker='o', c=tonpere[0*9 + j])

    
    plt.savefig('unfolding.png')
    plt.show()
    """
    plt.scatter(x, y, s=800, marker='s', c=color)
    plt.title('Rubik\'s cube unfolding')
    plt.axis('off')
    plt.savefig('unfolding.png')
    plt.show()    
    """
         


#draw the unfolding 
def draw2(data):
    x, y, color, c, max_color = donnees(data)
   
    n = 9
    m = 6
   
    color_center = []
    tabPref = [] #tableau qui va stocker toutes les moyennes des coins a chaque triplet centre
    coinPref = [] # tableau qui va stocker pour chaque coin le triplet centre qui lui correspond le plus par rapport a la moyenne des rgb
    tabCoin = tabCoinCouleur(data)
    tab_coeff = {}
    for k in range(0,6):
      color_center.append([])
    for k in range(0,8):  
        tabPref.append([])
    
    tabCoinCheck = couleurCoin(data)


    # stocke les moyennes des differences les plus basses pour chaque coin centre
    for i in range(0, len(tabCoin)): #parcours tous les coin 
        for j in range(0,len(tabCoinCheck)): #parcours tous les triplets de couleurs des centre a comparer
            #print tabCoin[i], "    " , tabCoinCheck[j]
            t, tt = choixPlusPetiteDiff(tabCoin[i], tabCoinCheck[j])
            tabPref[i].append(t)

            
    for i in range(0, len(tabPref)):
        print tabPref[i]



            
    for i in range(0, len(tabPref)):
        coinPref.append( choixMeilleurCentre(tabPref[i]) )

    tabFinal = []
    for i in range(0,len(tabCoin)):
        indice = coinPref[i][1]
        t , tt = choixPlusPetiteDiff(tabCoin[i], tabCoinCheck[indice])
        tabFinal.append( tt  ) 

    copieCheck = tabCoinCheck
    tabFigure = ['f', 'g', 'h', 'j' ,'k', 'l', 'm', 'n']

    #print " association " , tabFinal
   # print " coin centre " , copieCheck
    for i in range(0,len(tabFigure)):
        plt.figure(i+1)
        
        for j in range(0,3):
            t = [round(copieCheck[i][j][0])/68 , round(copieCheck[i][j][1])/68, round(copieCheck[i][j][2])/68 ]
            #print t
            tt = [round(tabFinal[i][j][0])/68 , round(tabFinal[i][j][1])/68, round(tabFinal[i][j][2])/68 ]
            #print tt
            plt.scatter(j, 0, s=800, marker='o', c= t )
            plt.scatter(j, 10, s=800, marker='o', c= tt )
    plt.show()

    """
    f = plt.figure(1)

    #for j in range (0,8):
    for i in range(0,3):
        plt.scatter(i, 0, s=800, marker='o', c=tabCoinCheck[0][i])
        plt.scatter(i, 10, s=800, marker='o', c=tabaffiche[i])
    
    plt.scatter(x, y, s=800, marker='s', c=color)
    plt.title('Rubik\'s cube unfolding')
    plt.axis('off')
    plt.savefig('unfolding.png')
      

    g = plt.figure(2)
    plt.scatter(x, y, s=800, marker='s', c=color)
    
    plt.show()
    """
    # CA OUVRE 2 FENETRE YOUPI


#############################
def draw3(data):
    x, y, color, c, max_color = donnees(data)   
    color_center = []
    tabPref = [] #tableau qui va stocker toutes les moyennes des coins a chaque triplet centre
    coinPref = [] # tableau qui va stocker pour chaque coin le triplet centre qui lui correspond le plus par rapport a la moyenne des rgb
    tabCoin = tabAreteCouleur(data)
    tab_coeff = {}
    for k in range(0,6):
      color_center.append([])
    for k in range(0,12):  
        tabPref.append([])
    
    tabCoinCheck = couleurArete(data)


    # stocke les moyennes des differences les plus basses pour chaque coin centre
    for i in range(0, len(tabCoin)): #parcours tous les coin 
        for j in range(0,len(tabCoinCheck)): #parcours tous les triplets de couleurs des centre a comparer
            #print tabCoin[i], "    " , tabCoinCheck[j]
            t, tt = choixPlusPetiteDiffDoublons(tabCoin[i], tabCoinCheck[j])
            tabPref[i].append(t)

            
    for i in range(0, len(tabPref)):
        print tabPref[i]," coucou"



            
    for i in range(0, len(tabPref)):
        coinPref.append( choixMeilleurCentre(tabPref[i]) )

    tabFinal = []
    for i in range(0,len(tabCoin)):
        indice = coinPref[i][1]
        t , tt = choixPlusPetiteDiffDoublons(tabCoin[i], tabCoinCheck[indice])
        tabFinal.append( tt  ) 

    copieCheck = tabCoinCheck
    tabFigure = ['f', 'g', 'h', 'j' ,'k', 'l', 'm', 'n']

    #print " association " , tabFinal
   # print " coin centre " , copieCheck
    for i in range(0,12):
        plt.figure(i+1)
        
        for j in range(0,2):
           
            t = [round(copieCheck[i][j][0])/68 , round(copieCheck[i][j][1])/68, round(copieCheck[i][j][2])/68 ]
            print t
            tt = [round(tabFinal[i][j][0])/68 , round(tabFinal[i][j][1])/68, round(tabFinal[i][j][2])/68 ]
            #print tt
            plt.scatter(j, 0, s=800, marker='o', c= t )
            plt.scatter(j, 10, s=800, marker='o', c= tt )
    #plt.show()

###########################

# retourne la difference la plus petite et l indice du triplet centre associe
def choixMeilleurCentre(tabPref):
    min = 256
    indice = -1
    for i in range(0, len(tabPref)):
        if min > tabPref[i]:
            min = tabPref[i]
            indice = i
    return tabPref[indice], indice


# retourne la difference la plus petite et l'arangement de couleur qui lui correspond
# entre les couleurs des centres et les couleurs des coins
def choixPlusPetiteDiff(tabCoin, tabCoinCheck):

    tabdiffFinal = []
    for i in range(0,1):
        tabC = []
        for p in range(0,3):
            tabC.append([])
        

        tabC[0].append(moyenneRGB(tabCoin[0] , tabCoinCheck[0]))
        tabC[0].append(moyenneRGB(tabCoin[0] , tabCoinCheck[1]))
        tabC[0].append(moyenneRGB(tabCoin[0] , tabCoinCheck[2]))

        tabC[1].append(moyenneRGB(tabCoin[1] , tabCoinCheck[0]))
        tabC[1].append(moyenneRGB(tabCoin[1] , tabCoinCheck[1]))
        tabC[1].append(moyenneRGB(tabCoin[1] , tabCoinCheck[2]))

        tabC[2].append(moyenneRGB(tabCoin[2] , tabCoinCheck[0]))
        tabC[2].append(moyenneRGB(tabCoin[2] , tabCoinCheck[1]))
        tabC[2].append(moyenneRGB(tabCoin[2] , tabCoinCheck[2]))
        #print " debut   "

        tabaffiche = []
        for j in range(0,3):
            
            min = 256
            indice = -1
            
            
            for i in range(0,3):
                if min > tabC[i][j]:
                    min = tabC[i][j]
                    indice = i
                   
            tabdiffFinal.append(tabC[indice][j])
            tabaffiche.append(tabCoin[indice])
            #print tabCoinCheck , "      " , tabC[indice][j] , "    " , j , "   " , tabCoin[indice]
            tabC[indice][0] = 256 
            tabC[indice][1] = 256 
            tabC[indice][2] = 256

    """
    for i in range(0,len(tabaffiche)):
        tabaffiche[i] = rgb255to01(tabaffiche[i],68)
        #tabCoinCheck[0][i] = rgb255to01(tabCoinCheck[0][i],68)
    print tabdiffFinal
    """
    #print "\n saut \n" 
    somme = 0
    for i in range (0, len(tabdiffFinal)):
        somme = tabdiffFinal[i]
    return round( round(somme)/3, 2), tabaffiche


def choixPlusPetiteDiffDoublons(tabCoin, tabCoinCheck):

    tabdiffFinal = []
    for i in range(0,1):
        tabC = []
        for p in range(0,2):
            tabC.append([])
        

        tabC[0].append(moyenneRGB(tabCoin[0] , tabCoinCheck[0]))
        tabC[0].append(moyenneRGB(tabCoin[0] , tabCoinCheck[1]))
       
        tabC[1].append(moyenneRGB(tabCoin[1] , tabCoinCheck[0]))
        tabC[1].append(moyenneRGB(tabCoin[1] , tabCoinCheck[1]))
        print "couleur   : ",  tabCoin , "    tabcoincheck   "   , tabCoinCheck[0] ,  "  " ,tabCoinCheck[1] , "    valeur diff     ", tabC[0]    , "  camembert           " ,   tabC[1]
        tabaffiche = []
        for j in range(0,2):
            
            min = 256
            indice = -1
            
            
            for i in range(0,2):
                if min > tabC[i][j]:
                    min = tabC[i][j]
                    indice = i
                   
            tabdiffFinal.append(tabC[indice][j])
            tabaffiche.append(tabCoin[indice])
            #print tabCoinCheck , "      " , tabC[indice][j] , "    " , j , "   " , tabCoin[indice]
            tabC[indice][0] = 256 
            tabC[indice][1] = 256
    somme = 0
    for i in range (0, len(tabdiffFinal)):
        somme += tabdiffFinal[i]
        print tabdiffFinal[i]," tabdiffFinal  : ",i
    return round( round(somme)/2, 2), tabaffiche


def moyenneRGB(c1, c2):
    r1 = abs(c1[0] - c2[0])

    g1 = abs(c1[1] - c2[1])

    b1 = abs(c1[2] - c2[2])

    return round( (r1+g1+b1) , 2)

def rgb255to01(c1,div):
    c1[0] = round(c1[0])/div
    c1[1] = round(c1[1])/div
    c1[2] = round(c1[2])/div
    return c1


def t255to01(c1,div):
    return  round(c1[0],2)/div,  round(c1[0],2)/div,  round(c1[0],2)/div

def calculDiffColorRGB(c1, c2):

    r1 = c1[0]/ (c1[0]+c1[1]+c1[2])
    r2 = c2[0]/ (c2[0]+c2[1]+c2[2])

    g1 = c1[1]/ (c1[0]+c1[1]+c1[2])
    g2 = c2[1]/ (c2[0]+c2[1]+c2[2])

    b1 = c1[2]/ (c1[0]+c1[1]+c1[2])
    b2 = c2[2]/ (c2[0]+c2[1]+c2[2])
    return abs(r1-r2), abs(g1-g2),abs(b1-b2)



data = [
[[22, 7, 5],[4, 6, 8],[5, 7, 9],[3, 5, 8],[4, 6, 9],[3, 5, 7],[4, 6, 7],[4, 6, 8],[3, 4, 7]],
[[31, 35, 29],[46, 52, 38],[35, 40, 33],[44, 48, 36],[59, 68, 45],[45, 50, 37], [3, 5, 6],[47, 51, 38],[36, 42, 33]],
[[21, 8, 5],[28, 8, 5],[34, 39, 31],[25, 9, 4],[32, 12, 6],[24, 8, 4],[17, 7, 4],[27, 9, 4],[19, 7, 5]],
[[28, 33, 42],[35, 40, 47],[26, 32, 39],[37, 42, 47],[52, 60, 62],[34, 40, 48],[27, 34, 42],[34, 40, 45],[24, 29, 40]],
[[24, 36, 41],[33, 44, 49],[24, 34, 38],[29, 43, 44],[43, 61, 59],[28, 42, 44],[25, 38, 42],[33, 46, 48],[24, 35, 41]],
[[9, 24, 29],[11, 31, 34],[8, 23, 27],[13, 32, 34],[15, 41, 40],[12, 31, 33],[11, 27, 31],[13, 34, 34],[10, 26, 30]]
]


data_turned = [
[[4, 4, 8],[4, 5, 8],[4, 6, 8],[3, 5, 7],[5, 7, 9],[3, 6, 7],[3, 5, 8],[4, 5, 7],[4, 5, 8]],
[[27, 39, 44],[30, 44, 45],[26, 38, 43],[46, 52, 37],[59, 68, 45],[47, 52, 37],[22, 9, 4],[26, 10, 5],[24, 8, 5]],
[[39, 46, 35],[29, 10, 5],[32, 37, 45],[47, 54, 38],[37, 19, 7],[36, 43, 46],[32, 34, 28],[29, 10, 4],[30, 33, 43]],
[[27, 39, 45],[31, 45, 46],[28, 39, 44],[38, 43, 47],[52, 59, 62],[38, 43, 50],[22, 8, 4],[26, 9, 4],[20, 7, 4]],
[[38, 44, 35],[35, 48, 50],[27, 32, 43],[48, 54, 39],[47, 64, 62],[36, 43, 48],[41, 46, 37],[35, 48, 48],[30, 35, 44]],
[[11, 29, 32],[13, 32, 34],[9, 25, 29],[12, 33, 33],[16, 42, 41],[10, 33, 34],[11, 30, 32],[13, 33, 34],[10, 28, 30]],
]
draw3(data)
#draw(data_turned)

""" 
16  [34, 39, 31]
00 [3, 5, 6]
22 [22, 7, 5]

[52, 60, 62]
[24, 29, 40]
[15, 41, 40]


[1.67, 14.33, 7.67, 14.33, 4.0, 16.33, 17.67, 16.33]
[7.33, 6.67, 8.0, 6.67, 3.67, 15.67, 7.0, 15.67]
[2.0, 14.67, 7.67, 14.67, 3.67, 16.0, 17.33, 16.0]
[6.33, 7.33, 7.67, 7.33, 4.0, 16.33, 8.33, 16.33]
[6.33, 7.67, 8.0, 7.67, 6.67, 10.33, 11.67, 10.33]
[6.67, 7.33, 8.67, 7.33, 6.33, 11.0, 12.33, 11.0]
[6.0, 11.67, 12.67, 11.67, 1.67, 14.33, 12.67, 14.33]
[6.67, 10.67, 7.67, 10.67, 2.33, 15.0, 12.0, 15.0]



"""
