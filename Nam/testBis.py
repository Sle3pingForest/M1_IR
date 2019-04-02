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

    plt.scatter(x, y, s=800, marker='s', c=color)
    plt.title('Rubik\'s cube unfolding')
    plt.axis('off')
    plt.savefig('out.png')
    plt.show()    
    
    
def comparaisonStat(data1, data2):
    compt = 0
    for i in range(0, len(data)):
        print "\n valeur de data base"
        print data1[i]
        print "valeur de data apres algo \n "
        print data2[i]
    return compt

data = [
[[9, 11, 8],[28, 38, 21],[37, 55, 26],[30, 40, 22],[13, 20, 11],[35, 47, 25],[44, 64, 32],[33, 47, 24],[44, 65, 32],
],[[1, 2, 4],[2, 4, 6],[3, 6, 5],[2, 5, 6],[1, 2, 3],[2, 3, 5],[5, 9, 7],[2, 3, 6],[1, 3, 4],
],[[31, 33, 40],[37, 48, 41],[51, 67, 57],[38, 42, 45],[41, 42, 52],[46, 59, 52],[49, 61, 58],[34, 42, 39],[48, 64, 53],
],[[7, 33, 24],[13, 45, 30],[14, 50, 31],[12, 38, 27],[3, 20, 17],[10, 34, 23],[11, 43, 27],[9, 28, 24],[8, 37, 25],
],[[22, 4, 2],[28, 9, 3],[40, 13, 3],[38, 12, 4],[28, 5, 2],[33, 8, 3],[40, 14, 4],[32, 10, 3],[35, 12, 3],
],[[19, 21, 25],[39, 50, 41],[48, 60, 51],[46, 57, 47],[36, 35, 42],[37, 44, 42],[53, 63, 52],[35, 46, 39],[43, 60, 49],
],]

data_turned =[
[[17, 17, 25],[33, 38, 39],[43, 59, 49],[34, 42, 37],[37, 38, 44],[36, 48, 40],[46, 61, 48],[44, 54, 44],[12, 48, 29],
],[[32, 31, 42],[38, 42, 45],[44, 58, 50],[39, 51, 44],[43, 45, 55],[33, 41, 39],[6, 10, 9],[44, 58, 51],[52, 66, 58],
],[[3, 4, 9],[3, 6, 7],[51, 65, 53],[3, 5, 7],[0, 2, 4],[4, 8, 7],[4, 8, 7],[3, 6, 6],[4, 8, 7],
],[[1, 1, 3],[37, 11, 4],[51, 61, 48],[32, 11, 3],[26, 5, 2],[31, 9, 3],[33, 10, 3],[35, 9, 3],[40, 13, 4],
],[[4, 12, 16],[9, 36, 24],[10, 40, 26],[12, 41, 27],[3, 18, 15],[10, 40, 27],[35, 12, 4],[11, 35, 24],[12, 44, 28],
],[[9, 9, 13],[30, 42, 23],[29, 43, 21],[37, 55, 28],[9, 13, 7],[26, 36, 19],[38, 56, 28],[30, 43, 22],[38, 55, 27],
],]

draw(data)
#draw(data_turned)
#comparaisonStat(data_turned,data2)
""" 

[52, 60, 62]
[24, 29, 40]
[15, 41, 40]

"""
