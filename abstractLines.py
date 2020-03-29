import numpy as np
import color
import cv2
import matplotlib.pyplot as plt

def abstractLines(path, reach, line_color, bkrd_color, lines):

    """ Draws some lines, or something like that. 

    Args:
        path (str): Path to the image.
        reach (float): The minimum for how far the origin of a line will search for an endpoint in pixel space.
        line_color (str): {'white', 'black', 'color'} What color the lines should be.
                          For grayscale images, line_color should be 'white' or 'black'.
                          If 'color' is requested, lines will be draw by choosing and looping 
                          through the top three colors in the image's color palette.
        bkrd_color (str): {'white', 'black'} What color the background should be.
        lines (int): The number of lines that should be drawn.
            
    Returns:
        frames (list): Collection of all of the frames, one after another. Each frame is a 2D
                       single channel numpy array. The length of this list will be equal to the integer
                       value of lines.
    """

    #read in image as grayscale
    src = cv2.imread(path, cv2.IMREAD_GRAYSCALE) 

    #get the rows, cols, chans in the image
    rows = np.shape(src)[0]
    cols = np.shape(src)[1]

    #set up the background canvas that will be drawn on
    if (bkrd_color == 'white'):

        canvas = np.ones((rows,cols)) 
    
    elif (bkrd_color == 'black'):

        canvas = np.zeros((rows, cols))

    else:

        print("ERROR: PLEASE ENTER A VALID BACKGROUND COLOR.")
        print("BACKGROUND COLOR REQUESTED:", bkrd_color)
        return -1

    #choose the line color(s) that will be drawn with
    if (line_color == 'white'):

        line_colors = (255,255,255)

    elif (line_color == 'black'):

        line_colors = (0, 0, 0)

    elif (line_color == 'color'):

        max_number_of_colors = 3
        hue_separation = 10
        sq = 0.7
        vq = 0.6
        space = 'rgb'
        line_colors = color.colorPalette(path, False, max_number_of_colors, hue_separation, sq, vq, space)

        if (len(line_colors) != 3):

            print("ERROR: YOU DUMMY, YOU ARE (PROBABLY) REQUESTING LINE COLOR FOR A GRAYSCALE IMAGE!")
            print("OR, THE COLOR PALETTE HELPER COULDN'T FIND THREE COLORS IN YOUR IMAGE!")
            print("REGARDLESS, SOMETHING IS FISHY!")
            print("LENGTH OF line_colors:", len(line_colors))
            return -1
    
    else:

        print("ERROR: PLEASE ENTER A VALID LINE COLOR.")
        print("LINE COLOR REQUESTED:", line_color)
        return -1

    #get a binary pointmap for the image
    pointmap = cv2.Canny(src, 50,50)
    pointmap = pointmap / np.max(pointmap)

    #pick an origin to start on
    origin = []
    while (len(origin) == 0):

        r_rand = np.random.randint(0, rows)
        c_rand = np.random.randint(0, cols)
        my_origin = [r_rand, c_rand]

        my_chosen_point = pointmap[r_rand, c_rand]

        if (my_chosen_point == 1):

            origin.append(my_origin)

        else:

            continue

