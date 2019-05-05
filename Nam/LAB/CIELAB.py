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
def draw(data, name):
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
            print L
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

        if(i== 0 or i == 47 ):
            print tab_LAB[i]
            print tab_LAB_center[0], "   ", tab_LAB_center[5]
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
    
    plt.title('Rubik\'s LAB_data_'+name +'_solve ')
    plt.savefig('LAB_data_'+name+'_solve.png')
    plt.show()
    

    plt.scatter(x, y, s=800, marker='s', c=color)
    plt.title('Rubik data '+ name)
    plt.axis('off')
    plt.savefig('LAB_data'+ name +'.png')
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
[[150,20,150],[83, 122, 73],[82, 127, 71],[85, 81, 8],[42, 62, 33],[80, 76, 8],[81, 127, 70],[86, 131, 73],[86, 133, 72],
],[[87, 26, 7],[82, 24, 4],[83, 27, 6],[10, 34, 36],[10, 35, 37],[10, 33, 36],[9, 34, 36],[9, 33, 36],[9, 31, 35],
],[[11, 73, 12],[83, 26, 6],[85, 28, 6],[11, 72, 11],[90, 27, 6],[83, 26, 6],[9, 70, 11],[85, 27, 6],[83, 27, 6],
],[[9, 71, 12],[10, 70, 11],[10, 70, 11],[10, 66, 11],[10, 73, 13],[10, 72, 11],[59, 13, 6],[61, 13, 6],[62, 14, 7],
],[[65, 13, 7],[63, 14, 6],[9, 33, 35],[62, 14, 7],[67, 12, 8],[9, 34, 36],[61, 13, 6],[62, 13, 7],[9, 32, 35],
],[[87, 84, 8],[85, 125, 73],[78, 77, 7],[81, 78, 8],[88, 83, 9],[82, 79, 8],[77, 76, 7],[84, 127, 73],[79, 78, 7],
],]

draw(data,'officielle_bruite')
