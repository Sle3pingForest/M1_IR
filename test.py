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
    tab[0].extend( (data[0][4], data[1][4] , data[2][4]) )
    tab[1].extend( (data[0][4], data[1][4] , data[4][4]) )
    tab[2].extend((data[0][4], data[2][4] , data[3][4]))
    tab[3].extend((data[0][4], data[3][4] , data[4][4]))

    tab[4].extend((data[5][4], data[1][4] , data[2][4]))
    tab[5].extend((data[5][4], data[1][4] , data[4][4]))
    tab[6].extend((data[5][4], data[2][4] , data[3][4]))
    tab[7].extend((data[5][4], data[3][4] , data[4][4]))

    return tab


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
    tabCoin = []
    tab_coeff = {}
    for k in range(0,6):
      color_center.append([])
      

    for k in range(0,8):
        tabCoin.append([])

    tabCoin[0].append(data[0][0]) 
    tabCoin[0].append(data[1][6])
    tabCoin[0].append(data[2][2])
    tabCoin[1].extend((data[0][2], data[1][8], data[4][0]))
    tabCoin[2].extend((data[0][6], data[2][8], data[3][0]))
    tabCoin[3].extend((data[0][8], data[3][2], data[4][6]))


    tabCoinCheck = couleurCoin(data)
    tabdiffFinal = []
    for i in range(0,1):
        tabC = []
        for p in range(0,3):
            tabC.append([])
        

        tabC[0].append(moyenneRGB(tabCoin[0][0] , tabCoinCheck[i][0]))
        tabC[0].append(moyenneRGB(tabCoin[0][0] , tabCoinCheck[i][1]))
        tabC[0].append(moyenneRGB(tabCoin[0][0] , tabCoinCheck[i][2]))

        tabC[1].append(moyenneRGB(tabCoin[0][1] , tabCoinCheck[i][0]))
        tabC[1].append(moyenneRGB(tabCoin[0][1] , tabCoinCheck[i][1]))
        tabC[1].append(moyenneRGB(tabCoin[0][1] , tabCoinCheck[i][2]))

        tabC[2].append(moyenneRGB(tabCoin[0][2] , tabCoinCheck[i][0]))
        tabC[2].append(moyenneRGB(tabCoin[0][2] , tabCoinCheck[i][1]))
        tabC[2].append(moyenneRGB(tabCoin[0][2] , tabCoinCheck[i][2]))
        

        tabaffiche = []
        for j in range(0,3):
            
            min = 256
            indice = -1
            
            
            for i in range(0,3):
                if min > tabC[i][j]:
                    min = tabC[i][j]
                    indice = i
            tabdiffFinal.append(tabC[indice][j])
            tabaffiche.append(tabCoin[0][indice])
            tabC[indice][0] = 256 
            tabC[indice][1] = 256 
            tabC[indice][2] = 256 
    
    for i in range(0,len(tabaffiche)):
        tabaffiche[i] = rgb255to01(tabaffiche[i],68)
        tabCoinCheck[0][i] = rgb255to01(tabCoinCheck[0][i],68)
    print tabdiffFinal

    f = plt.figure(1)

    #for j in range (0,8):
    for i in range(0,3):
        plt.scatter(i, 0, s=800, marker='o', c=tabCoinCheck[0][i])
        plt.scatter(i, 10, s=800, marker='o', c=tabaffiche[i])
    """
    plt.scatter(x, y, s=800, marker='s', c=color)
    plt.title('Rubik\'s cube unfolding')
    plt.axis('off')
    plt.savefig('unfolding.png')
    """  

    g = plt.figure(2)
    plt.scatter(x, y, s=800, marker='s', c=color)
    
    plt.show()

    # CA OUVRE 2 FENETRE YOUPI



def moyenneRGB(c1, c2):
    r1 = abs(c1[0] - c2[0])

    g1 = abs(c1[1] - c2[1])

    b1 = abs(c1[2] - c2[2])

    return (r1+g1+b1)/3

def rgb255to01(c1,div):
    c1[0] = round(c1[0])/div
    c1[1] = round(c1[1])/div
    c1[2] = round(c1[2])/div
    return c1
    

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
draw2(data)
#draw(data_turned)

""" 
16  [34, 39, 31]
00 [3, 5, 6]
22 [22, 7, 5]

[52, 60, 62]
[24, 29, 40]
[15, 41, 40]

"""
