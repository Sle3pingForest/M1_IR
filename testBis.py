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
from __future__ import division
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
    
    tab_new_rgb_centre=[]

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
                new_r = round(r/(r+g+b),3)
                new_g = round(g/(r+g+b),3)
                new_b = round(b/(r+g+b),3)
        tab_new_rgb_centre.append([new_r,new_g,new_b])
    return x,y,color, tab_new_rgb_centre, color_true, max_reading

# draw the unfolding
def draw(data):
    x, y, color, tab_new_rgb_centre, c, max_color = donnees(data)
   
    n = 9
    m = 6
   
    color_center = []
    tab_coeff = []
    for k in range(0,6):
      color_center.append([])


      
    compteur = 0
    
    for s, side in enumerate(data):
        for f, (r,g,b) in enumerate(side):

            
            indice = 0
            size = len(c)
        	  
           #v = '#{:02x}{:02x}{:02x}'.format( 200, 200 , 254 )
           #min_color = int(v[1:], 16)
                
            cfR =round(r/(r+g+b),3)
            cfG =round(g/(r+g+b),3)
            cfB =round(b/(r+g+b),3)
            tab_coeff.append([cfR,cfG,cfB])
                #color_center[indice].append( [r,g,b] )
    

	  #print indice
         
    #tab_coeff = sorted(tab_coeff.iteritems(), key=lambda (k,v): (v,k))
    #print tab_coeff
    #print "\n"
    #print len(tab_coeff)
    #print "\n"
    #print tab_new_rgb_centre
  
    #print "color center taille"
    #print len(color_center[0])
    for i in range(0,54):
        var = int(i/9)
        m = i%9
        ecart = 2500000
        ok = False;
        for j in range(0,len(tab_new_rgb_centre)):
            difR = abs(tab_coeff[i][0]-tab_new_rgb_centre[j][0])
            difG = abs(tab_coeff[i][1]-tab_new_rgb_centre[j][1])
            difB = abs(tab_coeff[i][2]-tab_new_rgb_centre[j][2])
            if(difR + difG + difB < ecart ):
                ecart = difR+difG+difB
                var = j
                ok = True
                print "var: ", var ,"**", ok
        print "var exterieur", var,"--", ok ,"\n"
        if(len(color_center[var]) < 9):
            color_center[var].append((data[var][m]))


    test_coeff= color_center
    tamere = []
    tonpere = []
    for i in range (0, len(c)):
        tamere.append( [round(c[i][0])/68,  round(c[i][1]) / 68, round(c[i][2])/68] )
         

    k = 0;
    for i in range(0,len(c)):
        print "\n"
        plt.scatter(i, 0, s=800, marker='s', c=tamere[i])
        p = 5
        for j in range(0, len(test_coeff[i]) ):
            yplacer = j+10
            p +=10
            tonpere.append([round(test_coeff[i][j][0]/68,3), round(test_coeff[i][j][1]/68,3), round(test_coeff[i][j][2]/68,3)])
            plt.scatter(i, p+yplacer , s=800, marker='o', c=tonpere[k])
            k = k +1
    
    plt.savefig('unfolding.png')
    plt.show()
    return color_center
    """
    plt.scatter(x, y, s=800, marker='s', c=color)
    plt.title('Rubik\'s cube unfolding')
    plt.axis('off')
    plt.savefig('trunerunfolding.png')
    plt.show()    
    """
    
def comparaisonStat(data1, data2):
    compt = 0
    for i in range(0, len(data)):
        print "\n valeur de data base"
        print data1[i]
        print "valeur de data apres algo \n "
        print data2[i]
    return compt     

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
#comparaisonStat(data_turned,data2)
""" 

[52, 60, 62]
[24, 29, 40]
[15, 41, 40]

"""
