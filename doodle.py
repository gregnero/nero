import numpy as np
import color
import cv2
import matplotlib.pyplot as plt
from progressbar import ProgressBar

def doodle(path, min_reach, max_reach, line_color, line_flexibility, number_of_line_colors, max_line_thickness, bkrd_color, canny_kernal_size, lines, view_pointmap):

    """ Draws some lines, or something like that. 

    Args:
        path (str): Path to the image.
        min_reach (float): The minimum distance that the origin of a line will search for an endpoint in pixel space.
        max_reach (float): The maximum distance that the origin of a line will search for an endpoint in pixel space.
        line_color (str): {'white', 'black', 'dark colors', 'light colors'} What color the lines should be. 
        line_flexibility (float): (-1, 1). Larger positive values will encourage straight lines.
        number_of_line_colors (int): The number of line colors you want to try to cycle through.
        max_line_thickness (int): The maximum thickness of the line in units of pixels. Lines are drawn with random thickness between [1, max_line_thickness].
        bkrd_color (str): {'white', 'black'} What color the background should be.
        canny_kernal_size (int): Square kernal size for canny edge detection. Larger values will "erode" image more.
        lines (int): The number of lines you would like to try and draw. 
        view_pointmap (bool): Option to see the binary pointmap of the image. Useful for canny_kernal_size decision.
            
    Returns:
        canvas (numpy.ndarray): The final drawing.

    To save images in another script, follow this guideline: cv2.imwrite(fname, canvas*255)

    """

    '''
    #TODO: automatically determine kernal size?
    #TODO: noise reduction for pointmap (or, edge enhancement?)
    '''

    #read in image as grayscale
    src = cv2.imread(path, cv2.IMREAD_GRAYSCALE) 

    #get the number of rows and cols in the image
    rows = np.shape(src)[0]
    cols = np.shape(src)[1]

    #set up the background canvas that will be drawn on
    if (bkrd_color == 'white'):

        canvas = np.ones((rows,cols, 3)) 
    
    elif (bkrd_color == 'black'):

        canvas = np.zeros((rows, cols, 3))

    else:

        print("ERROR: PLEASE ENTER A VALID BACKGROUND COLOR.")
        print("BACKGROUND COLOR REQUESTED:", bkrd_color)
        return -1

    #check reach conditions
    if (min_reach == max_reach):

        print("ERROR: PLEASE MAKE SURE min_reach < max_reach")
        return -1
    
    if (min_reach > max_reach):

        print("ERROR: PLEASE MAKE SURE min_reach < max_reach")
        return -1

    if (min_reach > rows or min_reach > cols):

        print("PLEASE MAKE SURE min_reach IS LESS THAN THE SIZE OF THE IMAGE IN EITHER DIMENSION")
        return -1


    #check flexibility conditions
    if (line_flexibility <= -1 or line_flexibility >= 1):

        #equality conditions are prohibited because choosing a line "parallel" with the line previous is just silly

        print("ERROR: PLEASE ENTER A VALID LINE FLEXIBILITY")
        return -1
    
    #choose the line color(s) that will be drawn with
    if (line_color == 'white'):

        line_colors = (1, 1, 1)

    elif (line_color == 'black'):

        line_colors = (0, 0, 0)

    elif (line_color == 'light colors' or line_color == 'dark colors'):

        #set internal private parameters for choosing colors
        view = False 
        hue_separation = 10
        space = 'bgr'

        #make decision about what "kind" of colors
        if (line_color == 'light colors'):

            sq = 0.8
            vq = 0.8

        elif (line_color == 'dark colors'):

            sq = 0.4
            vq = 0.3

        #get the line colors
        line_colors = color.colorPalette(path, view, number_of_line_colors, hue_separation, sq, vq, space)

        #if we can't find the number requested, just pick the max that could be found for these parameters 
        if (len(line_colors) != number_of_line_colors):

            #generate new palette with updated number of possible colors
            line_colors = color.colorPalette(path, view, len(line_colors), hue_separation, sq, vq, space)

            #update number of line colors
            number_of_line_colors = len(line_colors)
    
    else:

        print("ERROR: PLEASE ENTER A VALID LINE COLOR.")
        print("LINE COLOR REQUESTED:", line_color)
        return -1

    #get a binary pointmap for the image
    pointmap = cv2.Canny(src, canny_kernal_size, canny_kernal_size) #returns points either 0 or 255
    pointmap = pointmap / np.max(pointmap) #makes points either 0 or 1
    pointmap = pointmap.astype(int)

    #see how many points are possible
    number_of_available_points = int(np.sum(pointmap))

    #because of forbidden_points enforcement, catch inundation case
    if (lines >= number_of_available_points):

        print("ERROR: NOT ENOUGH AVAILABLE POINTS TO COMPLETE LINE REQUEST.")
        print("TRY DECREASING KERNAL SIZE OR DECREASING NUMBER OF LINES REQUESTED.")
        print("NUMBER OF AVAILABLE POINTS:", number_of_available_points)
        return -1

    #show the pointmap if the user wants it
    if (view_pointmap == True):

        plt.imshow(pointmap, cmap = 'gray')
        plt.title("Pointmap")
        plt.show()

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

    #set up pbar
    pbar = ProgressBar()

    #instantiate storage to store points that have been visited
    forbidden_points = []

    #instantiate storage for storing line coordinates
    edgelist = []

    #begin the lines loop
    for l in pbar(range(0, lines)):

        #choose source for this line
        if (l == 0):

            source_of_line = origin[0]

        else:

            source_of_line = previous_endpoint

        #append to forbid
        forbidden_points.append(source_of_line)

        #establish endpoint storage for this line
        jump_to_this_endpoint = []

        #look for a valid endpoint
        ticker = 0
        while (len(jump_to_this_endpoint) == 0):

            ticker = ticker + 1

            #if we search for an endpoint for t = size of max reach block, pick a new source elsewhere
            if (ticker == (max_reach * max_reach)):

                #pick a new source
                source_of_line_storage = []
                while (len(source_of_line_storage) == 0):
                    
                    #choose new random coordinate
                    r_rand = np.random.randint(0, rows)
                    c_rand = np.random.randint(0, cols)
                    my_source_of_line = (r_rand, c_rand)

                    #get pointmap value (zero or one)
                    my_chosen_point = pointmap[r_rand, c_rand]

                    #if it's one, pick it
                    if (my_chosen_point == 1):

                        source_of_line_storage.append(my_source_of_line)
                        source_of_line = source_of_line_storage[0]
                        ticker = 0 #this line is very very important, resets ticker!

                    #else, keep searching
                    else:

                        continue

            #get random coordinate limits (within max_reach range)
            upper_row_coord = source_of_line[0] - max_reach
            lower_row_coord = source_of_line[0] + max_reach
            left_col_coord = source_of_line[1] - max_reach
            right_col_coord = source_of_line[1] + max_reach

            #check conditions for saftey against core dump
            if (upper_row_coord < 0):

                upper_row_coord = 0

            if (lower_row_coord > rows):

                lower_row_coord = rows

            if (left_col_coord < 0):

                left_col_coord = 0

            if (right_col_coord > cols):

                right_col_coord = cols

            #get the random coordinate inside of that search range
            random_row_coordinate = np.random.randint(upper_row_coord, lower_row_coord)
            random_col_coordinate = np.random.randint(left_col_coord, right_col_coord)

            #create random coordinate tuple
            my_random_endpoint_coordinate = (random_row_coordinate, random_col_coordinate)

            #create storage for the random line under inspection [source -> endpoint]
            my_random_line = [source_of_line, my_random_endpoint_coordinate]

            #in the case where we don't have a previous line to worry about
            if (l == 0):

                #if we have visited this already, move on
                if (my_random_endpoint_coordinate in forbidden_points):

                    continue

                #get distance of random point from source of line
                dist = np.sqrt(np.square(source_of_line[0] - random_row_coordinate) + np.square(source_of_line[1] - random_col_coordinate))
                
                #get the value of that point at that random coordinate (zero or one)
                pointmap_value = pointmap[random_row_coordinate, random_col_coordinate]

                #if the point is one and fulfills reach requirements
                if (pointmap_value == 1 and dist >= min_reach and dist <= max_reach):

                    jump_to_this_endpoint.append(my_random_endpoint_coordinate)

                #else, keep searching
                else:

                    continue

            else:

                #if we have visited this already, move on
                if (my_random_endpoint_coordinate in forbidden_points):

                    continue

                #get bias
                my_bias_x = my_previous_line[0][0] - my_previous_line[1][0]
                my_bias_y = my_previous_line[0][1] - my_previous_line[1][1]
                my_bias = (my_bias_x, my_bias_y)

                #add bias to each of the random line coordinates to get same origin for dot product
                my_random_line_biased_source = (my_random_line[0][0] + my_bias[0], my_random_line[0][1] + my_bias[1])
                my_random_line_biased_endpoint = (my_random_line[1][0] + my_bias[0], my_random_line[1][1] + my_bias[1])
                my_random_line_biased = (my_random_line_biased_source, my_random_line_biased_endpoint)

                #set up vectors for dot product
                my_previous_line_vector = np.array([my_previous_line[1][1] - my_previous_line[0][1], my_previous_line[0][0] - my_previous_line[1][0]])
                my_random_line_biased_vector = np.array([my_random_line_biased[1][1] - my_random_line_biased[0][1], my_random_line_biased[0][0] - my_random_line_biased[1][0]])

                #max normalize each of the vectors to make them unit
                my_previous_line_vector_magnitude =  np.sqrt(np.sum(np.square(my_previous_line_vector)))
                my_random_line_biased_vector_magnitude =  np.sqrt(np.sum(np.square(my_random_line_biased_vector)))

                #catch for divide by zero error
                if (my_previous_line_vector_magnitude == 0 or my_random_line_biased_vector_magnitude == 0):

                    continue

                my_previous_line_vector_mn = my_previous_line_vector / my_previous_line_vector_magnitude
                my_random_line_biased_vector_mn = my_random_line_biased_vector / my_random_line_biased_vector_magnitude

                #find the dot product
                my_dot_product_value = np.dot(my_previous_line_vector_mn, my_random_line_biased_vector_mn)

                #get distance of random point from source of line
                dist = np.sqrt(np.square(source_of_line[0] - random_row_coordinate) + np.square(source_of_line[1] - random_col_coordinate))
                
                #get the value of that point at that random coord (should be 0 or 1)
                pointmap_value = pointmap[random_row_coordinate, random_col_coordinate]

                #if the point is one and fulfills reach requirements and fulfills dot product requirements
                if (pointmap_value == 1 and dist >= min_reach and dist <= max_reach and my_dot_product_value >= line_flexibility):

                    jump_to_this_endpoint.append(my_random_endpoint_coordinate)

                #else, keep searching
                else:

                    continue

        #store that endpoint for the next line's source
        previous_endpoint = jump_to_this_endpoint[0]

        #create storage for the next loop that keeps track of the line that was just drawn
        my_previous_line = [source_of_line, jump_to_this_endpoint[0]]

        #add the line that was just drawn to the edgelist (nb coordinate correction)
        #stored as: [(source coordinate) -> (sink coordinate)]
        edgelist.append([(source_of_line[1], source_of_line[0]), (jump_to_this_endpoint[0][1], jump_to_this_endpoint[0][0])])
        
   
    #set up counter for color looping
    color_counter = 0

    #draw the edges
    for edge in edgelist:

        #reset color counter when it reaches limit
        if (color_counter == number_of_line_colors):

            color_counter = 0

        #if the line is black or white
        if (line_color == 'white' or line_color == 'black'):

            #draw the line and reassign canvas
            cv2.line(canvas, edge[0], edge[1], line_colors, thickness = np.random.randint(1, max_line_thickness))

        #if we want to cycle through the colors 
        elif (line_color == 'dark colors' or line_color == 'light colors'):

            #get the current bgr value
            bgr_value = line_colors[color_counter]
            
            #uint8 normalize to make agreeable with cv2.line()
            b_norm = bgr_value[0] / 255
            g_norm = bgr_value[1] / 255
            r_norm = bgr_value[2] / 255
            bgr_value_norm = (b_norm, g_norm, r_norm)

            #draw the line and reassign canvas
            cv2.line(canvas, edge[0], edge[1], bgr_value_norm, thickness = np.random.randint(1, max_line_thickness))

        #++ the colorcounter
        color_counter = color_counter + 1

    #return the object :)
    return canvas
