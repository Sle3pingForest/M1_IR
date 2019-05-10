import math

def moyenneRGB(c1, c2):
    r1, g1, b1 = diffRGB(c1,c2)

    return round( (r1+g1+b1)/3 , 2)

def rgb255to01(c1,div):
    c1[0] = round(c1[0])/div
    c1[1] = round(c1[1])/div
    c1[2] = round(c1[2])/div
    return c1

def distance(c1, c2):

    somme = 0
    for i in range(0, len(c1)):
        somme += math.pow( (c1[i] - c2[i]), 2)
    return math.sqrt(somme)


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

#valeur peuvent etre negatives
def diffRGB_2(c1, c2): 
    r1 = c1[0] - c2[0]

    g1 = c1[1] - c2[1]

    b1 = c1[2] - c2[2]

    return r1,g1,b1

def compare2Couleur(c1 , c2):
    r1, g1, b1 = diffRGB(c1,c2)

    return round(math.sqrt(r1*r1+g1*g1+b1*b1) , 2)




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

def sameColor(c1, c2):
    check = False
    if (c1[0] == c2[0]) and (c1[1] == c2[1]) and (c1[2] == c2[2]):
        check = True
    return check


def distance_hsv(hsv1, hsv2):
    dist = 0
    if hsv1[0] > hsv2[0]:
        dist = ( 1 - hsv1[0] ) + hsv2[0]
    else:
        dist = ( 1 - hsv2[0] ) + hsv1[0]

    
    if dist > abs(hsv1[0] - hsv2[0]):
        dist = abs(hsv1[0] - hsv2[0])
        
    r = math.pow(dist, 2)
    g = math.pow(hsv1[1] - hsv2[1], 2)
    b = math.pow(hsv1[2] - hsv2[2], 2)

    dist =  math.sqrt( float(r) +float(g) + float(b) )
    return dist



def distance_hue(hsv1, hsv2):
    dist = 0
    if hsv1[0] > hsv2[0]:
        dist = ( 1 - hsv1[0] ) + hsv2[0]
    else:
        dist = ( 1 - hsv2[0] ) + hsv1[0]

    
    if dist > abs(hsv1[0] - hsv2[0]):
        dist = abs(hsv1[0] - hsv2[0])
        
    r = math.pow(dist, 2)
    return math.sqrt( float(r))


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


def ecart_delta_E(cVar,cRef):
    delta_b_p2=(cVar[0] - cRef[0])**2
    delta_a_p2=(cVar[1] - cRef[1])**2
    delta_L_p2=(cVar[2] - cRef[2])**2
    delta_E = (delta_b_p2+delta_a_p2+delta_L_p2)**1/2
    return delta_E
