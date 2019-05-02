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

matrixConversion = [[0.412453, 0.357580, 0.180423],
                    [0.212671, 0.715160, 0.072169],
                    [0.019334, 0.119193, 0.950227]]

def func(t):
    if(t > 0.008856):
        return np.power(t,1/3.0);
    else:
        return 7.787 * t +16/116.0;

def ecart_delta_E(cVar,cRef):
    delta_b_p2=(cVar[0] - cRef[0])**2
    delta_a_p2=(cVar[1] - cRef[1])**2
    delta_L_p2=(cVar[2] - cRef[2])**2
    delta_E = (delta_b_p2+delta_a_p2+delta_L_p2)**1/2
    return delta_E
    
# given a side index and a facet index, return x,y coordinates of the corresponding unfolding
def coord2(s,f):
    x,y = [[0,0],[0,30],[-30,0],[0,-30],[30,0],[60,0]][s]
    x += (f% 3)*10
    y -= (f//3)*10
    return x,y


# assemble x,y coordinates and sticker colors into three arrays
def donnees(data):
    x, y, color, color_scan,color_center = [], [], [], [],[]
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
            if(f == 4):
                color_center.append([r,g,b])
            else:
                color_scan.append([r, g, b])
    return x,y,color, color_scan,color_center, max_reading

# draw the unfolding
def draw(data):
    x, y, color, color_scan, color_center, max_reading = donnees(data)
    n = 9
    m = 6
   
    color_solve = []
    tab_LAB = []
    tab_LAB_center = []
    for k in range(0,6):
      color_solve.append([])


      
    compteur = 0
    #CALCUL LAB
    for s, side in enumerate(data):
        for f, (r,g,b) in enumerate(side):
            cie = np.dot(matrixConversion, [r,g,b])
            cie[0] = cie[0]/0.950456
            cie[2] = cie[2]/1.088754
            #calcule L
            L = round(116 * np.power(cie[1], 1/3.0) - 16.0 if cie[1] > 0.008856 else 903.3 * cie[1],3)
            #calcule a
            a = round(500*(func(cie[0]) - func(cie[1])),3)
            #calcul b
            b = round(200*(func(cie[1]) - func(cie[2])),3)
            if(f == 4):
                tab_LAB_center.append([b,a,L])
            else:
                tab_LAB.append([b,a,L])
    

    for i in range (0,len(tab_LAB)):
        var = 0;
        min_ecart = 10000000
        for j in range (0,len(tab_LAB_center)):
            ecart_E = ecart_delta_E(tab_LAB[i],tab_LAB_center[j])
            if(min_ecart > ecart_E):
                min_ecart = ecart_E
                var = j     
        color_solve[var].append(color_scan[i])
        
    for j in range (0,len(tab_LAB_center)):
        color_solve[j].append(color_center[j])
    print color_solve
    centreRef = []
    color_res= []
    for i in range (0, 6):
        centreRef.append([round(color_center[i][0])/max_reading,  round(color_center[i][1]) / max_reading, round(color_center[i][2])/max_reading] )
         
    k = 0;
    for i in range(0,6):
        plt.scatter(i, 0, s=800, marker='s', c=centreRef[i])
        p = 5
        for j in range(0, len(color_solve[i])):
            yplacer = j+10
            p +=10
            color_res.append([round(color_solve[i][j][0]/max_reading,3), round(color_solve[i][j][1]/max_reading,3), round(color_solve[i][j][2]/max_reading,3)])
            plt.scatter(i, p+yplacer , s=800, marker='o', c=color_res[k])
            k = k +1
    plt.savefig('LAB_data_init_prof_solve.png')
    plt.show()
    

    plt.scatter(x, y, s=800, marker='s', c=color)
    plt.title('Rubik\'s cube unfolding')
    plt.axis('off')
    plt.savefig('LAB_Init_data_prof.png')
    plt.show()    
    return color_center
    
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

data_scan_correct_damien = [
[[68, 106, 59],[65, 100, 57],[63, 101, 56],[66, 103, 58],[67, 102, 57],[65, 100, 58],[63, 100, 56],[66, 102, 58],[62, 99, 56],
],[[8, 21, 22],[32, 12, 7],[8, 45, 13],[44, 27, 9],[45, 27, 9],[44, 28, 8],[43, 28, 9],[43, 27, 8],[43, 27, 9],
],[[46, 29, 9],[9, 45, 14],[9, 45, 13],[9, 47, 14],[9, 45, 13],[9, 45, 14],[9, 45, 13],[9, 46, 14],[10, 48, 13],
],[[34, 13, 7],[33, 13, 7],[31, 12, 6],[33, 12, 7],[34, 12, 7],[33, 12, 7],[31, 12, 6],[45, 28, 9],[31, 12, 6],
],[[8, 21, 22],[8, 20, 21],[42, 27, 9],[8, 20, 21],[9, 21, 22],[9, 21, 22],[8, 20, 21],[8, 21, 21],[8, 20, 21],
],[[62, 59, 12],[61, 59, 12],[57, 57, 11],[59, 57, 12],[63, 59, 13],[61, 59, 12],[58, 57, 11],[60, 58, 12],[59, 58, 12],
],]

draw(data)
#draw(data_turned)
#draw(data_scan_correct_damien)
