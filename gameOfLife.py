import numpy as np
import cv2
import matplotlib.pyplot as plt

def gameOfLife(path, generations):

    """ Runs Conway's Game of Life on a binary grayscale (single channel) image.

    Args:
        path (str): Path to the image. The image will be generation zero.
        generations (int): How many generations you want to run, not including the zero generation.
            
    Returns:
        life (list): All of the generations for this image. (zero -> generations)
                     Each element in this list will be a 2D numpy array that is
                     the same size as the image that was ingested.
                     Element zero will be generation zero, element one will be
                     the first generation, etc...
                     Each of these images will also be binary and have 
                     range [0:1].

    """

    #read in image as grayscale
    src = cv2.imread(path, cv2.IMREAD_GRAYSCALE) 

    #normalize image to range [0:1] (assuming 8-bit image)
    src_norm = src / 255

    #get the rows, cols, chans in the image
    rows = np.shape(src)[0]
    cols = np.shape(src)[1]

    #instantiate storage for life
    life = []

    #append generation zero (the original image)
    life.append(src_norm)

    for g in range(0,generations):

        print(g)

        #create empty array to store the next generation in
        next_generation = np.zeros((rows, cols))

        #if generation zero, the current generation must be the original
        if (g == 0):

            current_generation = src_norm

        #else, the current generation will be the previous generation
        else:

            current_generation = previous_generation

        for r in range(1,rows-1):
            
            for c in range(1,cols-1):
                
                #get the current pixel value
                current_value = current_generation[r,c]

                #catch nonbinary issue
                if (current_value != 1 and current_value != 0):

                    print("ERROR: PLEASE PROVIDE A BINARY IMAGE")
                    return -1

                #get neighbor information
                n1 = current_generation[r-1, c-1]
                n2 = current_generation[r-1, c  ]
                n3 = current_generation[r-1, c+1]
                n4 = current_generation[r  , c-1]
                n5 = current_generation[r  , c+1]
                n6 = current_generation[r+1, c-1]
                n7 = current_generation[r+1, c  ]
                n8 = current_generation[r+1, c+1]
                neighbors = [n1, n2, n3, n4, n5, n6, n7, n8]
                
                #get the number of neigbors that are alive
                living_neighbors = int(sum(neighbors))

                #if the cell is alive
                if (current_value == 1):

                    #account for death by underpopulation
                    if (living_neighbors < 2):
                
                        fate = 0.0

                    #account for the survival case
                    elif (living_neighbors == 2 or living_neighbors == 3):

                        fate = 1.0

                    #account for death by overpopulation
                    elif (living_neighbors > 3):

                        fate = 0.0


                #if the cell is dead
                elif (current_value == 0):


                    #account for revivial case
                    if (living_neighbors == 3):

                        fate = 1.0

                    #else, remain dead
                    else:

                        fate = 0.0


                next_generation[r,c] = fate

        #append this generation to life
        life.append(next_generation)

        #store the recently updated generation as previous to operate on in the next generation
        previous_generation = next_generation

    return life
