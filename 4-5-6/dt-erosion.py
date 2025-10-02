# -*- coding: utf-8 -*-

## Exo DT et érosion
## Marie POINT - M2 VICO

"""
Question :

Explain the link between the distance transform and mathematical morphology.


Answer :

- Mathematical morphologies are operations between a binary image (object + background) and a structuring element (SE). 
For example : erosion.

- The distance transform (DT) is an operation on a binary image (with and foreground and a background)
that computes the distance from each pixel from the object to the nearest pixel in the background

The DT can be used to perform morphological operations more easily. Having the distance from each pixel to the
background might allow to not do heavy computations with the SE on each pixels.
For example : erosion, by thresholding the image from the distance transform.
"""


def dt4(image) :
    """Algo wavefront pour la DT avec d4"""
    dt = []
    for _ in range(len(image)):
        dt.append([float('inf')] * len(image[0]))

    to_visit = []
    head = 0 # pour la file
    
    # Background :

    # On prend tous les pixels de fond, et on les met dans la liste pour pouvoir visiter leurs voisins
    for i in range(len(image)):
        for j in range(len(image[0])):
            if image[i][j] == 0:
                dt[i][j] = 0
                to_visit.append((i, j))

    while head < len(to_visit):
        i, j = to_visit[head]
        head += 1
        # On visite les 4-voisins, on met leur dt à +1 puis on les ajoute à la liste aussi
        for x, y in [(-1,0),(1,0),(0,-1),(0,1)]: # voisins haut, bas, gauche, droite
            if 0 <= i+x < len(image) and 0 <= j+y < len(image[0]):
                if dt[i+x][j+y] > dt[i][j] + 1:
                    dt[i+x][j+y] = dt[i][j] + 1
                    to_visit.append((i+x, j+y))
    return dt

def erode11(image, SE=11) :
    """Erode l'image avec un SE carré de côté 11
    -> parcourir l'image et si le DT est inférieur au rayon du carré, alors le pixel sera eroded"""
    ero = []
    for _ in range(len(image)):
        ero.append([0]*len(image[0]))
    
    r = SE//2 # rayon du carré (arrondi)
    image_dt = dt4(image)
    for i in range(len(image)):
        for j in range(len(image[0])):
            ero[i][j] = 0 if image_dt[i][j] < r else 1
    
    return ero


# test avec une grosse matrice
if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap

    # affichage des images
    def show_image(mat, binary=True):
        plt.imshow(mat, cmap=ListedColormap(['white', 'black']) if binary else 'inferno')
        plt.xticks(range(len(mat[0])))
        plt.yticks(range(len(mat)))
        plt.gca().set_xticks([i + 0.5 for i in range(len(mat[0]))], minor=True)
        plt.gca().set_yticks([i + 0.5 for i in range(len(mat))], minor=True)
        plt.grid(True, which="minor", color="gray", linestyle='--', linewidth=0.5)
        if not binary :
            for i in range(len(mat)):
                for j in range(len(mat[0])):
                    plt.text(j, i, str(mat[i][j]), ha='center', va='center', color='black')
        plt.show()

    # enorme matrice de test
    def test_matrix(height=40, width=60):
        mat = [[0]*width for _ in range(height)]
        
        # un rectangle au centre
        for i in range(10, 30):
            for j in range(15, 45):
                mat[i][j] = 1
        
        # un petit carré isolé
        for i in range(5, 10):
            for j in range(5, 10):
                mat[i][j] = 1

        # une forme diagonale
        for i in range(25, 35):
            for j in range(i-20, i-15):
                mat[i][j] = 1
                
        return mat

    enorme_matrice = test_matrix()
    print("Matrice de test :")
    show_image(enorme_matrice)
    print("Distance Transform :")
    show_image(dt4(enorme_matrice), binary=False)
    print("Erosion avec carré de  côté 11 :")
    show_image(erode11(enorme_matrice))