import numpy as np
import color
import cv2
import matplotlib.pyplot as plt

def abstractLines(path, reach, line_color, bkrd_color, canny_kernal_size, lines):

    """ Draws some lines, or something like that. 

    Args:
        path (str): Path to the image.
        reach (float): The minimum for how far the origin of a line will search for an endpoint in pixel space.
        line_color (str): {'white', 'black', 'color'} What color the lines should be.
                          For grayscale images, line_color should be 'white' or 'black'.
                          If 'color' is requested, lines will be draw by choosing and looping 
                          through the top three colors in the image's color palette.
        bkrd_color (str): {'white', 'black'} What color the background should be.
        canny_kernal_size (int): square kernal size for canny edge detection. 50 is recommended value.
                                 The higher the number the stricter the lines will be.
                                 For more "line points" make the number lower.
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
    pointmap = cv2.Canny(src, canny_kernal_size, canny_kernal_size) #returns points either 0 or 255
    pointmap = pointmap / np.max(pointmap) #makes points either 0 or 1

    #pick an origin to start on
    origin = []
    while (len(origin) == 0):

        r_rand = np.random.randint(0, rows)
        c_rand = np.random.randint(0, cols)
        my_origin = (r_rand, c_rand)

        my_chosen_point = pointmap[r_rand, c_rand]

        if (my_chosen_point == 1):

            origin.append(my_origin)

        else:

            continue

    #begin the lines loop
    for l in range(0, lines):

        #get the source for this line
        if (l == 0):

            source_of_line = origin[0]

        else:

            source_of_line = last_endpoint

        #establish endpoint storage for this line
        jump_to_this_endpoint = []

        #restrict reach of endpoint in a square region around the source
        search_block_left_column_index = int(source_of_line[1] - (reach/2))
        search_block_right_column_index = int(source_of_line[1] + (reach/2))
        search_block_upper_row_index = int(source_of_line[0] - (reach/2))
        search_block_lower_row_index = int(source_of_line[1] + (reach/2))

        #catch any core dump errors that have the potential to occur
        if (search_block_left_column_index < 0):

            search_block_left_column_index = 0
        
        if (search_block_right_column_index >= cols):

            search_block_right_column_index = int(cols - 1)

        if (search_block_upper_row_index < 0):

            search_block_upper_row_index = 0

        if (search_block_lower_row_index >= rows):

            search_block_lower_row_index = int(rows-1)

        #while we haven't found an endpoint, look for one
        while (len(jump_to_this_endpoint) == 0):
            
            #get random coord in the search block region
            random_row_coordinate = np.random.randint(search_block_upper_row_index, search_block_lower_row_index)
            random_col_coordinate = np.random.randint(search_block_left_column_index, search_block_right_column_index)
            
            #create random coord tuple
            my_random_endpoint_coordinate = (random_row_coordinate, random_col_coordinate)

            #get the value of that point at that random coord (should be 0 or 1)
            pointmap_value = pointmap[random_row_coordinate, random_col_coordinate]

            #if it is 1, choose it
            if (pointmap_value == 1):

                jump_to_this_endpoint.append(my_random_endpoint_coordinate)

            #else, look for another point that is equal to 1
            else:

                continue

        #store that endpoint for the next line's source
        last_endpoint = jump_to_this_endpoint[0]




