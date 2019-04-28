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
import math
import colorsys
from data.data3 import data3
from data.data_lumiere import data_lumiere
from data.data_lumiere2 import data_lumiere2
from data.data_sombre import data_sombre
from data.data_sombre2 import data_sombre2
from data.rubiks_desordre import data_desordre
from data.data_dernier import data_dernier
from data.data_nam_L import data_nam_L
from data.data_lumiere_04_04 import data_04_04
from data.data_04_04_2 import data_04_04_2
from data.data_0404_coin_340 import data_coin_340
from data.data_0404_anglecoin_330 import data_coin_330
from data.data_0404_anglecoin_340_sombre import data_sombre_coin_340
from data.data_0904_2 import data_0904_2
from data.data_1004_anglemaxarriere import data_1004_anglemaxarriere
from data.data_1004_anglemaxarriere_sombre import data_1004_anglemaxarriere_sombre
from data.data_1004_max_L_1_3pi import data_1004_max_L_1_3pi
from data.data_1004_max_S_0_3pi import data_1004_max_S_0_3pi
from data.data_1004_max_L_0_3pi import data_1004_max_L_0_3pi
from data.data_turned_1004_max_S_0_3pi import data_turned_1004_max_S_0_3pi
from data.test_feuille_couleur import test_feuille_couleur
from data.test_feuille_couleur_pres import test_feuille_couleur_pres
from data.test_feuille_couleur_tres_pres import test_feuille_couleur_tres_pres
from data.test_rubiks_rube2 import test_rubiks_rube2
from data.data_1204_max_S_0_3pi import data_1204_max_S_0_3pi
from data.data_1204_rubiks1_max_S_0_3pi import data_1204_rubiks1_max_S_0_3pi
from data.data_rubiks4_2804_toucher import data_rubiks4_2804_toucher
from data.data_rubiks4_2804 import data_rubiks4_2804
from data.data_rubiks4_2804_centrer import data_rubiks4_2804_centrer
from data.data_rubiks4_2804_rgbmode import data_rubiks4_2804_rgbmode
from data.data_2804_800_prof import data_2804_800_prof
from data.data_2804_800 import data_2804_800
from data.data_2804_750_prof import data_2804_750_prof
# given a side index and a facet index, return x,y coordinates of the corresponding unfolding
def coord2(s,f):
    x,y = [[0,0],[0,30],[-30,0],[0,-30],[30,0],[60,0]][s]
    x += (f% 3)*10
    y -= (f//3)*10
    return x,y

# retourne les huits combinaisons de triplets possibles en fonction des centres
def couleurCoin(data):
    tab = []
    tab_diff = []
    tab_nuance = []
    for i in range(0,8):
        tab.append([])
        tab_diff.append([])

    tab[0].extend((data[0][4], data[1][4] , data[2][4]))
    tab[1].extend((data[0][4], data[1][4] , data[4][4]))
    tab[2].extend((data[0][4], data[2][4] , data[3][4]))
    tab[3].extend((data[0][4], data[3][4] , data[4][4]))

    tab[4].extend((data[5][4], data[1][4] , data[4][4]))
    tab[5].extend((data[5][4], data[1][4] , data[2][4]))
    tab[6].extend((data[5][4], data[3][4] , data[4][4]))
    tab[7].extend((data[5][4], data[2][4] , data[3][4]))

   

    #pour chaque couleur du triplet
    for i in range(0, len(data)):
        color = [0,0,0]
        #pour chaque r g b de la couleur
        for j in range(0, len(data[i][4])):
            #print data[i][j]
            #print diffCoin[i]
            color[j] = data[i][4][j] - diffCoin[i][j]
        tab_nuance.append( color )


    tab_diff[0].extend((tab_nuance[0], tab_nuance[1] , tab_nuance[2]))
    tab_diff[1].extend((tab_nuance[0], tab_nuance[1] , tab_nuance[4]))
    tab_diff[2].extend((tab_nuance[0], tab_nuance[2] , tab_nuance[3]))
    tab_diff[3].extend((tab_nuance[0], tab_nuance[3] , tab_nuance[4]))

    
    tab_diff[4].extend((tab_nuance[5], tab_nuance[1] , tab_nuance[4]))
    tab_diff[5].extend((tab_nuance[5], tab_nuance[1] , tab_nuance[2]))
    tab_diff[6].extend((tab_nuance[5], tab_nuance[3] , tab_nuance[4]))
    tab_diff[7].extend((tab_nuance[5], tab_nuance[2] , tab_nuance[3]))

        
    return tab, tab_diff

def couleurCentre(data):
     tab = []
     for s, side in enumerate(data):
         tab.append(data[s][4])
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

    
    tabCoin[4].extend((data[1][2], data[4][2], data[5][0]))
    tabCoin[5].extend((data[1][0], data[2][0], data[5][2]))
    tabCoin[6].extend((data[3][8], data[4][8], data[5][6])) 
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



def draw_diffRGB(data):
    x, y, color, c, max_color = donnees(data)
   
    n = 9
    m = 6
    c = couleurCentre(data)
    color_center = []
    for k in range(0,6):
      color_center.append([])
  

    for s, side in enumerate(data):
        for f, (r,g,b) in enumerate(side):
            if f != 4:
	        indice = 0
	        min_color = max_color
	        size = len(c)
          
                #compare avec chaque centre
	        for i in range(0,size):

                    #calcul la nouvelle nuance de chaque centre
                    color = [0,0,0]
                    for l in range(0,3):
                        color[l] = c[i][l] - diff[i][l]
              
	            rr = abs(r - color[0])
	            gg = abs(g - color[1])
	            bb = abs(b - color[2])
	            if (min_color > ((rr +gg+bb)/3) ):
	                min_color = (rr +gg+bb)/3
	                indice = i
	        color_center[indice].append( [r,g,b] )
                
    nb_erreur = 0
    for i in range(0, len(color_center)):
        if ( len(color_center[i]) > 8):
            nb_erreur +=  len(color_center[i]) - 8

    print float(nb_erreur)/48 *100 , "% d erreur  " ,   nb_erreur , "   sur 48"
          
    #coeff couleur uniforme
    plt.figure(0)
    for i in range(0, len(c)):
        
        plt.scatter(i, 0, s=800, marker='s', c=t255to01(c[i], max_color))
        #decalage
        decalage = 5
        for j in range (0,len(color_center[i])):
             plt.scatter(i, decalage + j, s=800, marker='s', c=t255to01(color_center[i][j], max_color) )
          

    
    c = couleurCentre(data)

    color_center = []
    for k in range(0,6):
      color_center.append([])
  

    for s, side in enumerate(data):
        for f, (r,g,b) in enumerate(side):
            if f != 4:
	        indice = 0
	        min_color = max_color
	        size = len(c)
                
	        for i in range(0,size):

                    color = [0,0,0]
                    for l in range(0,3):
                        if f%2 == 0:
                            color[l] = c[i][l] - diffCoin[i][l]
                        else:
                            color[l] = c[i][l] - diffCote[i][l]
	            rr = abs(r - color[0])
	            gg = abs(g - color[1])
	            bb = abs(b - color[2])
	            if (min_color > ((rr +gg+bb)/3) ):
	                min_color = (rr +gg+bb)/3
	                indice = i
	        color_center[indice].append( [r,g,b] )


    nb_erreur = 0
    for i in range(0, len(color_center)):
        if ( len(color_center[i]) > 8):
            nb_erreur +=  len(color_center[i]) - 8
    print float(nb_erreur)/48 *100 , "% d erreur  " ,   nb_erreur , "   sur 48"
          
    #coeff couleur uniforme
    plt.figure(1)
    for i in range(0, len(c)):
        
        plt.scatter(i, 0, s=800, marker='s', c=t255to01(c[i], max_color))
        #decalage
        decalage = 5
        for j in range (0,len(color_center[i])):
             plt.scatter(i, decalage + j, s=800, marker='s', c=t255to01(color_center[i][j], max_color) )
          
    
    
    plt.show()
    
# draw the unfolding / TA PARTIE A FINIR NAM
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
    
    tabCoinCheck, tabCoinCheckDiff = couleurCoin(data)


    # stocke les moyennes des differences les plus basses pour chaque coin centre
    for i in range(0, len(tabCoin)): #parcours tous les coins 
        for j in range(0,len(tabCoinCheck)): #parcours tous les triplets de couleurs des centre a comparer
            #print tabCoin[i], "    " , tabCoinCheck[j]
            #t, tt, indice = choixPlusPetiteDiff(tabCoin[i], tabCoinCheck[j])
            t = diffRGBCoin( tabCoin[i], tabCoinCheck[j] )
            tabPref[i].append(t)
    """
    for i in range(0, len(tabPref)):
        print tabPref[i]
    """        
    for i in range(0, len(tabPref)):
        coinPref.append( choixMeilleurCentre(tabPref[i]) )

    tabFinal = []
    tabIndice = []


    test_coin = repartition(tabPref)

    nb_erreur = 0
    for i in range(0, len(test_coin)):
        if test_coin[i] != data_turned_coin_ok[i][1]:
            nb_erreur += 1
            #print test_coin[i] , "     " , data_coin_ok[i][1]

    print float(nb_erreur)/8 *100 , "% d erreur  " ,   nb_erreur , "   sur " , len(test_coin)

    print "affectation ", test_coin
    
    plt.figure(0)
    
    decalage = 0
    for i in range(0,8):

        for j in range(0,3):
            couleurTabCoin = [ round( tabCoin[i][j][0] )/68 , round( tabCoin[i][j][1])/68 , round( tabCoin[i][j][2])/68 ]
            couleurCentreAssocie = [ round( tabCoinCheck[ test_coin[i] ][j][0])/68 , round( tabCoinCheck[ test_coin[i] ][j][1])/68 , round( tabCoinCheck[ test_coin[i] ][j][2])/68  ]
            couleurCentre = [ round( tabCoinCheck[ i ][j][0])/68 , round( tabCoinCheck[ i ][j][1])/68 , round( tabCoinCheck[ i ][j][2])/68  ]
            if j == 0:
                decalage += 5
            plt.scatter(i*3+j + decalage, 0, s=800, marker='o', c= couleurTabCoin )
            plt.scatter(i*3+j + decalage, 5, s=800, marker='o', c= couleurCentreAssocie )
            plt.scatter(i*3+j + decalage, 10, s=800, marker='o', c= couleurCentre )
    
    #plt.savefig('tri_coin.png')
    plt.show()

    """
    for i in range(0,len(tabCoin)):
        tabIndice.append( coinPref[i][1])
        indice = coinPref[i][1]
        #t , tt, ttt= choixPlusPetiteDiff(tabCoin[i], tabCoinCheck[indice])
        #tabFinal.append( tt )

    nb_erreur = 0
    for i in range(0, len(tabIndice)):
        if tabIndice[i] != data_turned_coin_ok[i][1]:
            nb_erreur += 1

    print float(nb_erreur)/8 *100 , "% d erreur  " ,   nb_erreur , "   sur " , len(tabCoin)
    """
    copieCheck = tabCoinCheck
    tabFigure = ['f', 'g', 'h', 'j' ,'k', 'l', 'm', 'n']

    #print " association " , tabFinal
    # print " coin centre " , copieCheck
    """
    plt.figure(0)
    
    decalage = 0
    for i in range(0,8):

        for j in range(0,3):
            couleurTabCoin = [ round( tabCoin[i][j][0] )/68 , round( tabCoin[i][j][1])/68 , round( tabCoin[i][j][2])/68 ]
            couleurCentreAssocie = [ round( tabCoinCheck[ tabIndice[i] ][j][0])/68 , round( tabCoinCheck[ tabIndice[i] ][j][1])/68 , round( tabCoinCheck[ tabIndice[i] ][j][2])/68  ]
            if j == 0:
                decalage += 5
            plt.scatter(i*3+j + decalage, 0, s=800, marker='o', c= couleurCentreAssocie )
            plt.scatter(i*3+j + decalage, 10, s=800, marker='o', c= couleurTabCoin )

    
    #plt.savefig('tri_coin.png')
    plt.show()

    """

    datas = [data_2804_750_prof,data_2804_800_prof, data_2804_800,data_rubiks4_2804_rgbmode, data_rubiks4_2804_centrer]#data_turned_1004_max_S_0_3pi,data_1004_max_S_0_3pi, data_1004_max_L_0_3pi]#data3, data_lumiere, data_lumiere2, data_sombre, data_sombre2]
    showData(datas,True)

    # CA OUVRE 2 FENETRE YOUPI


#############################
def draw3(data):
    x, y, color, c, max_color = donnees(data)   
    color_center = []
    tabPref = [] 
    coinPref = [] 
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
    plt.show()

"""
def repartitionParPosition(data):
    tab = positionnement(data)

    tab_pref = []
    for i in range(0, len(tab)):
        tab_pref.append([])
"""


# draw the unfolding
def draw_rgb_debut(data):
    x, y, color, c, max_color = donnees(data)
   
    n = 9
    m = 6
    #color_center = [[] * 54] * 6
    color_center = []
    for k in range(0,6):
      color_center.append([])
   
    cccc = []
    
    compteur = 0

    print " JESUIS CENTRE ", c
    
    for s, side in enumerate(data):
        for f, (r,g,b) in enumerate(side):
	  indice = 0
	  min_color = max_color
	  size = len(c)
	  for i in range(0,size):
	    rr = abs(r - c[i][0])
	    gg = abs(g - c[i][1])
	    bb = abs(b - c[i][2])
	    if (min_color > ((rr +gg+bb)/3) ):
	     min_color = (rr +gg+bb)/3
	     indice = i
	  #print indice
	  color_center[indice].append( [r,g,b] )
	   #print ' JESUIS FACE ' , s , ' EN FACET ', f , ' JAJOUTE DANS ' , indice , ' COMPTEUR ' , compteur
	   #print color_center[indice]



    nb_erreur = 0
    for i in range(0, len(color_center)):
        for j in range (0, len(color_center[i])):
            dedans = False
            for k in range(0, len(data[i])):
                if sameColor( color_center[i][j], data[i][k]):
                   dedans = True
            if dedans == False:
                nb_erreur += 1

    print float(nb_erreur)/54 *100 , "% d erreur  " ,   nb_erreur , "   sur " , 54

           
    for i in range(0,len(color_center) ):
        
      #print ' COULEUR SIDE ',  c[i], '  liste facet: ', color_center[i], '\n'
      tabColor = []
      for j in range (0 , len(color_center[i])):
            plt.scatter(i, 10 + j* 5, s=800, marker='o', c=  rgb255to01(color_center[i][j], 68) )
            plt.scatter(i, 0, s=800, marker='o', c= t255to01(c[i],68) )
    """
    plt.scatter(x, y, s=800, marker='s', c=color)
    plt.title('Rubik\'s cube unfolding')
    plt.axis('off')
    plt.savefig('unfolding.png')
    """
    plt.show()    

"""
a utiliser sur un rubik resolu
compare les facet avec le centre associe et calcul
l ecart de couleur du aux problemes mecaniques du robot
qui capte les facet a une hauteur differente
"""
def calculEcartAvecCentre(data):
    diff = []
    for i in range(0,6):
        diff.append([data[i][4]])
    
    for s, side in enumerate(data):
        for f, (r,g,b) in enumerate(side):
            if f != 4:
                diffR = abs(diff[side][0][0] - r)
                diffG = abs(diff[side][0][1] - g)
                diffB = abs(diff[side][0][2] - b)
                diff.append([diffR, diffG, diffB])
    return diff





###########################


def distance_hsv(hsv1, hsv2):
    r = math.pow(hsv1[0] - hsv2[0], 2)
    g = math.pow(hsv1[1] - hsv2[1], 2)
    b = math.pow(hsv1[2] - hsv2[2], 2)
    return math.sqrt( float(r) +float(g) + float(b) )

#comparaison des couleurs hsv avec chaque centre et sa distance vectoriel 
def test_hsv(data):

    centre = couleurCentre(data)
    centre_hsv = []
    tab_hsv = []
    tab_rgb, data_rgb = [], []

    #conversion face i en hsv
    for i in range(0, len(data[1])):
        color = t255to01(data[1][i],68)
        data_rgb.append(color)
        #print "  couleur des donnees :  " , data[1][4] , "      couleur en format 0-1 : ", color
        tab_hsv.append( colorsys.rgb_to_hsv(color[0], color[1], color[2]) )
        #tab_rgb.append( colorsys.hsv_to_rgb( tab_hsv[i][0], tab_hsv[i][1], tab_hsv[i][2]) )

    #conversion centre rgb to hsv
    for i in range(0, len(centre)):
        color = t255to01(centre[i],68)
        #print "  couleur des donnees :  " , data[1][4] , "      couleur en format 0-1 : ", color
        centre_hsv.append( colorsys.rgb_to_hsv(color[0], color[1], color[2]) )

    for j in range(0, len(centre)):
        #calcul distance
        for i in range(0, len(tab_hsv)):
            if i==0:
                print data[1][i], "     " , data[j][4]
            print "distance facet ",i," avec centre de ", j," : ", distance_hsv(tab_hsv[i], centre_hsv[j] )
        print "\n"

    #test sur toutes les facets
    
    data_hsv ,color_center = [], []
    for i in range(0, len(data)):
        data_hsv.append([])
        color_center.append([])
        
    for s, side in enumerate(data):
        for f, (r,g,b) in enumerate(side):
            data_hsv[s].append( colorsys.rgb_to_hsv(r, g, b) )
            min_distance = 100000
            indice = 0
            for i in range(0, len(centre_hsv)):
                dist = distance_hsv(data[s][f], centre[i])
                if dist < min_distance:
                    min_distance = dist
                    indice = i
	    color_center[indice].append( [r,g,b] )

    for i in range(0,len(color_center) ):

      tabColor = []
      for j in range (0 , len(color_center[i])):
            plt.scatter(i, 10 + j* 5, s=800, marker='o', c=  rgb255to01(color_center[i][j], 68) )
            plt.scatter(i, 0, s=800, marker='o', c= t255to01(centre[i],68) )
   
    plt.show()    


def sameColor(c1, c2):
    return c1[0] == c2[0] and c1[1] == c2[1] and c1[2] == c2[2]

# retourne la difference la plus petite et l indice du triplet centre associe
def choixMeilleurCentre(tabPref):
    min = 256
    indice = -1
    for i in range(0, len(tabPref)):
        if min > tabPref[i]:
            min = tabPref[i]
            indice = i
    return tabPref[indice], indice



def diffRGBCoin(tabCoin, tabCoinCheck):

    somme1 = [0,0,0]
    somme2 = [0,0,0]

    for i in range (0, len(tabCoin)):
        for j in range(0, len(tabCoin[i])):
            somme1[j] += tabCoin[i][j]
            somme2[j] += tabCoinCheck[i][j]

    return round( float(  abs(somme1[0] - somme2[0] ) + abs(somme1[1] - somme2[1] ) + abs(somme1[2] - somme2[2] ) / 3), 2)
    

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
        indice = 0
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
            tabC[indice][0] = 256 
            tabC[indice][1] = 256 
            tabC[indice][2] = 256

    #print "\n saut \n" 
    somme = 0
    for i in range (0, len(tabdiffFinal)):
        somme = tabdiffFinal[i]
    return round( round(somme)/3, 2), tabaffiche, indice


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
        #print "couleur   : ",  tabCoin , "    tabcoincheck   "   , tabCoinCheck[0] ,  "  " ,tabCoinCheck[1] , "    valeur diff     ", tabC[0]    , "  camembert           " ,   tabC[1]
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

def showData(data, plusieurs=False):

    taille = 0
    # if true there is many array of data
    if plusieurs == True:
        taille = len(data)
    elif len(data) != 0:
        taille = 1
    for i in range(0, taille):
        
        x, y, color, c, max_color = donnees(data[i])
        plt.figure(i)
        plt.axis('off')
        plt.scatter(x, y, s=800, marker='s', c=color)
    plt.show()

def positionnement(data):

    tab_faces_group = []

    for i in range(0, len(data[0])):
        tab_faces_group.append([])

    
    for i in range(0, len(data[0])):
        for j in range(0, len(data)):
            tab_faces_group[i].append(data[j][i])

    return tab_faces_group

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
  
"""
je recupere la plus petite difference pour chaque coin centre
je compare et recupere le plus petit des 8 differences et son indice
jassocie le triplet au coin centre et je modifie toutes les valeurs a cet indice a un max
je refais la meme jusqua avoir tout compare
"""

def moyenneRGB(c1, c2):
    r1, g1, b1 = diffRGB(c1,c2)

    return round( (r1+g1+b1)/3 , 2)

def rgb255to01(c1,div):
    c1[0] = round(c1[0])/div
    c1[1] = round(c1[1])/div
    c1[2] = round(c1[2])/div
    return c1


def t255to01(c1,div):
    color = 0
    color = [ round(c1[0])/div,  round(c1[1])/div,  round(c1[2])/div ] 
    return  color

def calculDiffColorRGB(c1, c2):

    r1 = c1[0]/ (c1[0]+c1[1]+c1[2])
    r2 = c2[0]/ (c2[0]+c2[1]+c2[2])

    g1 = c1[1]/ (c1[0]+c1[1]+c1[2])
    g2 = c2[1]/ (c2[0]+c2[1]+c2[2])

    b1 = c1[2]/ (c1[0]+c1[1]+c1[2])
    b2 = c2[2]/ (c2[0]+c2[1]+c2[2])
    return abs(r1-r2), abs(g1-g2),abs(b1-b2)

def diffRGB(c1, c2): 
    r1 = abs(c1[0] - c2[0])

    g1 = abs(c1[1] - c2[1])

    b1 = abs(c1[2] - c2[2])

    return r1,g1,b1

def compare2Couleur(c1 , c2):
    r1, g1, b1 = diffRGB(c1,c2)

    return round(math.sqrt(r1*r1+g1*g1+b1*b1) , 2)


def calculDiffCentre(data, mode="uniforme"):
    
    tab = couleurCentre(data)
    moyenneDiff = []
    for s, side in enumerate(data):
        somme = [0,0,0]
        for f, (r,g,b) in enumerate(side):
            if f != 4:
                c1 = [r,g,b]
                colordiff = diffRGB(c1, tab[s])
                for i in range(0,3):
                    somme[i] += colordiff[i]
        #calcul moyenne diff
        for j in range(0,3):
            somme[j] = somme[j]/8
        moyenneDiff.append(somme)
    return moyenneDiff


def calculDiffCentreCoinCote(data, mode="uniforme"):
    
    tab = couleurCentre(data)
    moyenneDiffCoin, moyenneDiffCote = [], []
    for s, side in enumerate(data):
        sommeCoin, sommeCote = [0,0,0], [0,0,0]
        for f, (r,g,b) in enumerate(side):
            if f != 4:
                c1 = [r,g,b]
                colordiff = diffRGB(c1, tab[s])
                for i in range(0,3):
                    if f%2 == 0:
                        sommeCoin[i] += colordiff[i]
                    else:
                        sommeCote[i] += colordiff[i]
        #calcul moyenne diff
        for j in range(0,3):
            sommeCoin[j] = sommeCoin[j]/4
            sommeCote[j] = sommeCote[j]/4
        moyenneDiffCoin.append(sommeCoin)
        moyenneDiffCote.append(sommeCote)
    return moyenneDiffCoin,  moyenneDiffCote


    
data = [
[[3, 5, 6],[4, 6, 8],[5, 7, 9],[3, 5, 8],[4, 6, 9],[3, 5, 7],[4, 6, 7],[4, 6, 8],[3, 4, 7]],
[[31, 35, 29],[46, 52, 38],[35, 40, 33],[44, 48, 36],[59, 68, 45],[45, 50, 37],[34, 39, 31],[47, 51, 38],[36, 42, 33]],
[[21, 8, 5],[28, 8, 5],[22, 7, 5],[25, 9, 4],[32, 12, 6],[24, 8, 4],[17, 7, 4],[27, 9, 4],[19, 7, 5]],
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

data_coin_ok = [
    [0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,7]
]

data_turned_coin_ok = [
    [0,2], [1,0], [2,3], [3,1], [4,6], [5,4], [6,7], [7,5]
]


diff = calculDiffCentre(data)
diffCoin, diffCote = calculDiffCentreCoinCote(data)

#test_hsv(data)
#draw_diffRGB(data)
#draw_rgb_debut(data)
draw2(data_turned)
#draw(data)





"""
tabDiffEucl = []
for i in range(0,8):
    tabDiffEucl.append([])
min = 256
indiceI  = -1
indiceJ = -1
temp = 255
for i in range (0,len(data)):
    print "face : ",i
    min = 256
    for j in range (0,len(data[0])):
        for k in range (0,6):
            if j!= 4 :
                temp = compare2Couleur(data[i][j],data[k][4])
                tabDiffEucl[i].append(temp)
                if min > temp :
                    #print"COUCOU"
                    min = temp
                    
                    indiceK = k
                indiceI = i
                indiceJ = j
                
            #print i , j ,": ", i , k," (i j) " , " i k"
            #print temp
        print tabDiffEucl[i]
        #print "min : ", min ,"cote : ",indiceI,indiceJ , "centre : ", indiceK,4
    #print "face : ",i
    
    print "\n"

"""
            
"""
c1 =[3, 5, 6]
c2 = [4, 6, 8]
test = compare2Couleur(c1, c2)
print test
"""
"""
c1 =[59, 68, 45]
c2 =[31, 35, 29]
test = compare2Couleur(c1, c2)
print test


c1 =[38, 43, 47]
c2 =[31, 35, 29]
test = compare2Couleur(c1, c2)
print test


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
