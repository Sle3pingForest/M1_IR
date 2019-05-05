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
    x, y, color, color_true, group_color,tab_inter = [], [], [], [], [],[]
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
            tab_inter.append([r,g,b])
            if f == 4:
                rateRed = (round(r)/round(max_reading)) * 100
                rateGreen =(round(g)/round(max_reading)) * 100
                rateBlue = (round(b)/round(max_reading)) * 100
                color_true.append([r, g, b])
                new_r = round(rateRed/(rateRed+rateGreen+rateBlue)*100)
                new_g = round(rateGreen/(rateRed+rateGreen+rateBlue)*100)
                new_b = round(rateBlue/(rateRed+rateGreen+rateBlue)*100)
                #print '% rouge: ', new_r , ' - % Vert: ', new_g, ' - % Bleu: ', new_b
        tab_new_rgb_centre.append([new_r,new_g,new_b])
    return x,y,color, tab_new_rgb_centre, color_true, max_reading,tab_inter

def algoPortion(data,isDraw):
    x, y, color, tab_new_rgb_centre, c, max_reading,tab_inter = donnees(data)
   

    color_center = []
    tab_coeff = []
    for k in range(0,6):
        color_center.append([])

    
    for s, side in enumerate(data):
        for f, (r,g,b) in enumerate(side):
            cfR =round(r/(r+g+b)*100,0)
            cfG =round(g/(r+g+b)*100,0)
            cfB =round(b/(r+g+b)*100,0)
            tab_coeff.append([cfR,cfG,cfB])
     
    for i in range(0,54):
        min = 25000
        for j in range(0,len(tab_new_rgb_centre)):
            difR = abs(tab_coeff[i][0]-tab_new_rgb_centre[j][0])
            difG = abs(tab_coeff[i][1]-tab_new_rgb_centre[j][1])
            difB = abs(tab_coeff[i][2]-tab_new_rgb_centre[j][2])
            moy = (difR +difG+difB)/3
            if i==24:
               print moy , "  ", j , "  ", tab_new_rgb_centre[j], "   " , tab_coeff[i]
            if(moy <= min):
                var = j
                min = moy
        color_center[var].append(tab_inter[i])
    if(isDraw):
        return x,y,color,c, max_reading,color_center
    else:
        return color_center

def draw(data,name):
    x, y, color,c, max_reading,color_center = algoPortion(data, True)
   
    test_coeff= color_center
    centre = []
    cube = []
    for i in range (0, len(c)):
        centre.append( [round(c[i][0])/max_reading,  round(c[i][1]) / max_reading, round(c[i][2])/max_reading] )
         
    k = 0;
    for i in range(0,len(c)):
        plt.scatter(i, 0, s=800, marker='s', c=centre[i])
        p = 5
        for j in range(0, len(test_coeff[i]) ):
            yplacer = j+10
            p +=10
            cube.append([round(test_coeff[i][j][0]/max_reading,3), round(test_coeff[i][j][1]/max_reading,3), round(test_coeff[i][j][2]/max_reading,3)])
            plt.scatter(i, p+yplacer , s=800, marker='o', c=cube[k])
            k = k +1
        
    plt.title('Rubik\'s Portion_data_'+name +'_solve ')
    plt.savefig('Portion_data_'+name+'_solve.png')
    plt.show()
    

    plt.scatter(x, y, s=800, marker='s', c=color)
    plt.title('Rubik data '+ name)
    plt.axis('off')
    plt.savefig('Portion_data'+ name +'.png')
    plt.show() 
    
def comparaisonStat(data1, data2):
    compt = 0
    for i in range(0,6):
        for j in range (0,9):
            if(j <> 4 and data1[i][j] in data2[i]):
                compt = compt + 1
    print compt/48 * 100 , "%"
    return compt

data = [
[[150, 20, 150],[83, 122, 73],[82, 127, 71],[85, 81, 8],[42, 62, 33],[80, 76, 8],[81, 127, 70],[86, 131, 73],[86, 133, 72],
],[[87, 26, 7],[82, 24, 4],[83, 27, 6],[10, 34, 36],[10, 35, 37],[10, 33, 36],[9, 34, 36],[9, 33, 36],[9, 31, 35],
],[[11, 73, 12],[83, 26, 6],[85, 28, 6],[11, 72, 11],[90, 27, 6],[83, 26, 6],[9, 70, 11],[85, 27, 6],[83, 27, 6],
],[[9, 71, 12],[10, 70, 11],[10, 70, 11],[10, 66, 11],[10, 73, 13],[10, 72, 11],[59, 13, 6],[61, 13, 6],[62, 14, 7],
],[[65, 13, 7],[63, 14, 6],[9, 33, 35],[62, 14, 7],[67, 12, 8],[9, 34, 36],[61, 13, 6],[62, 13, 7],[9, 32, 35],
],[[87, 84, 8],[85, 125, 73],[78, 77, 7],[81, 78, 8],[88, 83, 9],[82, 79, 8],[77, 76, 7],[84, 127, 73],[79, 78, 7],
],]


draw(data,'officiel_bruite')

"""res = algoPortion(data,False)
comparaisonStat(data,res)"""

""""
draw(data_turned_last_scan)
res = algoPortion(data_turned_last_scan,False)
comparaisonStat(data_ref_last_scan,res)

draw(data_turned_nam)
res = algoPortion(data_turned_nam,False)
comparaisonStat(data_correct_nam,res)

"""
