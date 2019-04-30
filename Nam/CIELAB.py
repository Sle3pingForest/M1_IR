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
    print color_solve
    centreRef = []
    color_res= []
    for i in range (0, 6):
        centreRef.append([round(color_center[i][0])/max_reading,  round(color_center[i][1]) / max_reading, round(color_center[i][2])/max_reading] )
         
    k = 0;
    for i in range(0,6):
        plt.scatter(i, 0, s=800, marker='s', c=centreRef[i])
        p = 5
        for j in range(0, len(color_center)):
            yplacer = j+10
            p +=10
            color_res.append([round(color_solve[i][j][0]/max_reading,3), round(color_solve[i][j][1]/max_reading,3), round(color_solve[i][j][2]/max_reading,3)])
            plt.scatter(i, p+yplacer , s=800, marker='o', c=color_res[k])
            k = k +1
    plt.savefig('LAB_damien_solve.png')
    plt.show()
    

    plt.scatter(x, y, s=800, marker='s', c=color)
    plt.title('Rubik\'s cube unfolding')
    plt.axis('off')
    plt.savefig('LAB_Init.png')
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
[[146, 207, 150],[221, 255, 200],[209, 255, 182],[214, 255, 189],[252, 255, 217],[218, 255, 192],[211, 255, 185],[220, 255, 200],[208, 255, 184],
],[[39, 117, 103],[61, 212, 145],[57, 207, 134],[61, 207, 140],[70, 242, 164],[62, 209, 142],[58, 198, 133],[60, 213, 145],[56, 198, 130],
],[[78, 34, 20],[123, 61, 23],[116, 61, 23],[134, 65, 24],[148, 72, 28],[128, 61, 25],[120, 66, 23],[118, 62, 23],[121, 60, 23],
],[[13, 25, 30],[22, 44, 46],[18, 38, 37],[21, 41, 41],[25, 50, 49],[21, 42, 41],[22, 46, 39],[21, 45, 42],[22, 47, 39],
],[[126, 198, 169],[143, 247, 173],[145, 248, 169],[156, 255, 187],[189, 255, 226],[154, 255, 185],[138, 238, 165],[139, 241, 170],[151, 255, 175],
],[[130, 193, 181],[167, 255, 200],[169, 255, 197],[171, 255, 204],[222, 255, 250],[175, 255, 202],[161, 252, 189],[165, 255, 197],[170, 255, 192],
],]

data_scan_correct_damien = [
[[68, 106, 59],[65, 100, 57],[63, 101, 56],[66, 103, 58],[67, 102, 57],[65, 100, 58],[63, 100, 56],[66, 102, 58],[62, 99, 56],
],[[8, 21, 22],[32, 12, 7],[8, 45, 13],[44, 27, 9],[45, 27, 9],[44, 28, 8],[43, 28, 9],[43, 27, 8],[43, 27, 9],
],[[46, 29, 9],[9, 45, 14],[9, 45, 13],[9, 47, 14],[9, 45, 13],[9, 45, 14],[9, 45, 13],[9, 46, 14],[10, 48, 13],
],[[34, 13, 7],[33, 13, 7],[31, 12, 6],[33, 12, 7],[34, 12, 7],[33, 12, 7],[31, 12, 6],[45, 28, 9],[31, 12, 6],
],[[8, 21, 22],[8, 20, 21],[42, 27, 9],[8, 20, 21],[9, 21, 22],[9, 21, 22],[8, 20, 21],[8, 21, 21],[8, 20, 21],
],[[62, 59, 12],[61, 59, 12],[57, 57, 11],[59, 57, 12],[63, 59, 13],[61, 59, 12],[58, 57, 11],[60, 58, 12],[59, 58, 12],
],]
    
draw(data_scan_correct_damien)
