import numpy as np
import cv2
import matplotlib.pyplot as plt

def scramble(path, k, S):

    """ Scrambles a square image according to a single-parameter (k) toral automorphic family.
        Consult Voyatzis & Pitas (1996) for more information.
        Periodicity is a property of this automorphism.
        Visual cryptography!

    Details: By scrambling an NxN image S times with parameter k, you are "chaotically" 
             rearranging the pixels. After some number of scrambles T the image will
             exactly re-arrange itself. T is the period of this automorphism for image
             of size NxN and free paramater k. Period depends on both k and N. Therefore,
             the metrics T, k, and N form an ensemble of "secret keys." T is a function of
             k and N and has no closed-form solution; it's chaotic. T can be experimentally 
             determined. If you have an NxN image and know its period T, you choose free
             parameter k to act as the single "secret key."

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

    #read in image as grayscale
    src = cv2.imread(path, cv2.IMREAD_GRAYSCALE) 

    #get the rows, cols, chans in the image
    rows = np.shape(src)[0]
    cols = np.shape(src)[1]

    #ensure input image is square
    if (rows != cols):

        print("ERROR: Please provide a square image to scramble.")
        return -1
