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

# draw the unfolding
def draw(data):
    x, y, color, c, max_color = donnees(data)
   
    n = 9
    m = 6
    #color_center = [[] * 54] * 6
    color_center = []
    for k in range(0,6):
      color_center.append([])
   
    cccc = []
    
    compteur = 0
    
    for s, side in enumerate(data):
        for f, (r,g,b) in enumerate(side):
	  indice = 0
	  size = len(c)
	  
	  v = '#{:02x}{:02x}{:02x}'.format( 200, 200 , 254 )
	  min_color = int(v[1:], 16)
	  for i in range(0,size):
	    valeur = '#{:02x}{:02x}{:02x}'.format( r, g , b )
	    valeur2 = '#{:02x}{:02x}{:02x}'.format( c[i][0], c[i][1] , c[i][2] )
	    """ rr = abs(r - c[i][0])
	    gg = abs(g - c[i][1])
	    bb = abs(b - c[i][2])"""
	    m = abs(int(valeur2[1:], 16) - int(valeur[1:], 16))
	    if (min_color >  m):
	     min_color = m
	     indice = i
	  #print indice
	  color_center[indice].append( [r,g,b] )
	   #print ' JESUIS FACE ' , s , ' EN FACET ', f , ' JAJOUTE DANS ' , indice , ' COMPTEUR ' , compteur
	   #print color_center[indice]
    
    print c
    tamere = []
    tonpere = []
    for k in range(0,6):
      tonpere.append([])
    for i in range (0, len(c)):
        tamere.append( [ round(c[i][0])/68,  round(c[i][1]) / 68, round(c[i][2])/68] )
            
        
    
    for i in range(0,len(color_center) ):
        
        plt.scatter(i, 0, s=800, marker='s', c=tamere[i])
        p = 5
        for j in range(0, len(color_center[i]) ):
            p += 5
            print ' COULEUR SIDE ',  c[i], '  liste facet: ', color_center[i], '\n'
            #print len(color_center) , "    "  , i   , "    " , len(color_center[i]) , "   " , j , " rgb   " , color_center[i][j][1], "  " , color_center[i][j][0] , "  " , color_center[i][j][2]
            tonpere[i].append(  [ round(color_center[i][j][0])/68,  round(color_center[i][j][1]) / 68, round(color_center[i][j][2])/68] )

            xplacer = i
            yplacer = j;
            if (j > 9 ):
                xplacer = i +0.5
                yplacer = j - 60
            plt.scatter(xplacer, yplacer + 5 + p , s=800, marker='o', c=tonpere[i][j])


    
    plt.savefig('unfolding.png')
    plt.show()
    """
    plt.scatter(x, y, s=800, marker='s', c=color)
    plt.title('Rubik\'s cube unfolding')
    plt.axis('off')
    plt.savefig('unfolding.png')
    plt.show()    
    """
    
     

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
#draw(data)
draw(data_turned)

