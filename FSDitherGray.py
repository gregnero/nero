import numpy as np
import cv2
import matplotlib.pyplot as plt

def FSDitherGray(path, levels):

    """ Performs Floyd-Steinberg dithering for a grayscale (single channel) image

    Args:
        path (str): Path to the image
        levels (int): The number of ditherable gray levels
            
    Returns:
        dst (numpy.ndarray): Floyd-Steinberg dithered image

    """

    #argcheck to make sure levels is valid
    if (levels <= 1 or levels > 256):

        print("PLEASE ENTER A VALID LEVEL PARAMETER")
        return -1

    #read in image as grayscale
    src = cv2.imread(path, cv2.IMREAD_GRAYSCALE) 

    #normalize image to range [0:1] (assuming 8-bit image)
    src_norm = src / 255

    #get the rows, cols, chans in the image
    rows = np.shape(src)[0]
    cols = np.shape(src)[1]

    #instantiate storage for FS dithered image 
    dst = np.zeros((rows,cols))

    #create array of available grayscale values that we can quantize to
    my_available_values = np.linspace(0,1,levels)

    for r in range(0,rows-1): #nb range limits to prevent core dump

        for c in range(1,cols-1): #nb range limits to prevent core dump
           
            current_value = src_norm[r,c]

            #perform quantization (rounding)
            absolute_distance_array = np.abs(my_available_values - current_value)
            my_index = np.argmin(absolute_distance_array)
            rounded_value = my_available_values[my_index]

            dst[r,c] = rounded_value

            error = current_value - rounded_value

            src_norm[r,   c+1] = src_norm[r,   c+1] + (error * 7/16)
            src_norm[r+1, c+1] = src_norm[r+1, c+1] + (error * 1/16)
            src_norm[r+1, c  ] = src_norm[r+1, c  ] + (error * 5/16)
            src_norm[r+1, c-1] = src_norm[r+1, c-1] + (error * 3/16)

    return dst
