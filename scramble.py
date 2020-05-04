import numpy as np
import cv2
import matplotlib.pyplot as plt

def scramble(path, k, S):

    """ Scrambles a square image according to a single-parameter (k) toral automorphic family.
        Consult Voyatzis & Pitas (1996) for more information.
        Periodicity is a property of this automorphism.
        Visual cryptography!

    Details: By scrambling an NxN image S times with parameter k, you are "chaotically" 
             rearranging the pixel code values. After some number of scrambles T the image 
             will exactly re-arrange itself. T is the period of this automorphism for image
             of size NxN and free paramater k. Finding T is a nontrivial task because of its
             chaotic nature. It can be experimentally determined through image processing.
             I wrote a report on this if you are interested.

    Example Usage (Visual Cryptography): You have a "secret image" containing a message for 
            another party. You scramble this NxN image S times with free parameter k such 
            that S is less than T. You must know T for this to work. Then, you send this
            scrambled image to the other party. They can retrieve the secret image by
            scrambling the already scrambled image (T-S) times with the same k value. In 
            effect, they are just "completing the orbit" of the period.

    Args:
        path (str): Path to the image
        k (int): Free parameter in the automorphism that acts as the "secret key"
        S (int): The number of scrambles that you want to perform
            
    Returns:
        dst (numpy.ndarray): The scrambled input image

    """

    #TODO: experiment with color
    #TODO: experiment/troubleshoot dtype errors

    #read in image as grayscale
    src = cv2.imread(path, cv2.IMREAD_GRAYSCALE) 

    #get the rows, cols, chans in the image
    rows = np.shape(src)[0]
    cols = np.shape(src)[1]

    #ensure input image is square
    if (rows != cols):

        print("ERROR: Please provide a square image to scramble.")
        return -1

    #establish parameters for this toral automorphic family
    a1 = 1
    a2 = 1
    a3 = k
    a4 = k + 1

    #instantiate blank array for the scrambled image
    scrambled = np.zeros((rows, cols))

    #create a copy of the source to manipulate
    src_copy = np.copy(src)

    for s in range(1, S+1):
        
        for r in range(0, rows):

            for c in range(0, cols):

                #get the new coordinate
                new_row_coordinate = ((a1 * r) + (a2 * c)) % rows
                new_col_coordinate = ((a3 * r) + (a4 * c)) % cols

                #place the code value in the new coordinate
                scrambled[new_row_coordinate, new_col_coordinate] = src_copy[r,c]


        #pass along most recent scramble for the next scramble
        src_copy = np.copy(scrambled)

    return src_copy
