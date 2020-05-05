import numpy as np
import cv2
import matplotlib.pyplot as plt

def scramble(path, k, S, c):

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
        k (int): Free parameter in the automorphism that acts as a "secret key"
        S (int): The number of scrambles that you want to perform
        c (boolean): Choice between color or grayscale input image. Color is experimental.
                     True -> color image input
                     False -> grayscale image input
            
    Returns:
        dst (numpy.ndarray): The scrambled input image

    """

    #TODO: experiment/troubleshoot dtype things
    #TODO: consider "non-unified" scrambling of color channels...
           # this could be cool because each channel could have a differnt free parameter
           # right now, though, the channels are being scrambled in "unison"

    #establish parameters for this toral automorphic family
    a1 = 1
    a2 = 1
    a3 = k
    a4 = k + 1

    #for grayscale images
    if (c == False):

        #read in image as grayscale
        src = cv2.imread(path, cv2.IMREAD_GRAYSCALE) 

        #get the rows, cols in the image
        rows = np.shape(src)[0]
        cols = np.shape(src)[1]

        #ensure input image is square
        if (rows != cols):

            print("ERROR: Please provide a square image to scramble.")
            return -1

        #instantiate blank array for the scrambled image
        scrambled = np.zeros((rows, cols), dtype = np.uint8)

        #create a copy of the source to manipulate
        src_copy = np.copy(src)

        for s in range(1, S+1):
            
            for r in range(0, rows):

                for c in range(0, cols):

                    #get the new coordinate
                    new_row_coordinate = ((a1 * r) + (a2 * c)) % rows
                    new_col_coordinate = ((a3 * r) + (a4 * c)) % cols

                    #place the code value at the new coordinate
                    scrambled[new_row_coordinate, new_col_coordinate] = src_copy[r,c]

            #pass along most recent scramble for the next scramble
            src_copy = np.copy(scrambled)

        return scrambled 

    #for color images
    elif (c == True):

        #read in image as color
        src = cv2.imread(path, cv2.IMREAD_COLOR) 

        #get the rows, cols, chans in the image
        rows = np.shape(src)[0]
        cols = np.shape(src)[1]
        chans = np.shape(src)[2]

        #ensure input image is square
        if (rows != cols):

            print("ERROR: Please provide a square image to scramble.")
            return -1
        
        #get the image channels
        blue_channel = src[:,:,0]
        green_channel = src[:,:,1]
        red_channel = src[:,:,2]

        #instantiate blank arrays for the scrambled color channels
        blue_channel_scrambled = np.zeros((rows, cols), dtype = np.uint8)
        green_channel_scrambled = np.zeros((rows,cols), dtype = np.uint8)
        red_channel_scrambled = np.zeros((rows, cols), dtype = np.uint8)

        #get copies of the image channels
        blue_channel_copy = np.copy(blue_channel)
        green_channel_copy = np.copy(green_channel)
        red_channel_copy = np.copy(red_channel)

        for s in range(1, S+1):
            
            for r in range(0, rows):

                for c in range(0, cols):

                    #get the new coordinate
                    new_row_coordinate = ((a1 * r) + (a2 * c)) % rows
                    new_col_coordinate = ((a3 * r) + (a4 * c)) % cols

                    #place the code value for each channel at the new coordinate
                    blue_channel_scrambled[new_row_coordinate, new_col_coordinate] = blue_channel_copy[r,c]
                    green_channel_scrambled[new_row_coordinate, new_col_coordinate] = green_channel_copy[r,c]
                    red_channel_scrambled[new_row_coordinate, new_col_coordinate] = red_channel_copy[r,c]

            #pass along most recent scrambles for the next scrambles
            blue_channel_copy = np.copy(blue_channel_scrambled)
            green_channel_copy = np.copy(green_channel_scrambled)
            red_channel_copy = np.copy(red_channel_scrambled)

        #TODO: scheme for easy channel switching and selection
        reconstruction_list = [red_channel_scrambled, green_channel_scrambled, blue_channel_scrambled]
        
        #bring the channels together
        reconstructed = cv2.merge(reconstruction_list)

        return reconstructed
