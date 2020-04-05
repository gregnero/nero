import numpy as np
import color
import cv2
import matplotlib.pyplot as plt
from progressbar import ProgressBar

def abstractLines(path, min_reach, max_reach, line_color, line_flexibility, max_number_of_line_colors, max_line_thickness, bkrd_color, canny_kernal_size, lines, view_pointmap):

    """ Draws some lines, or something like that. 

    Args:
        path (str): Path to the image.
        min_reach (float): The minimum for how far the origin of a line will search for an endpoint in pixel space.
        max_reach (float): The maximum for how far the origin of a line will search for an endpoint in pixel space.
        line_color (str): {'white', 'black', 'color'} What color the lines should be.
                          For grayscale images, line_color should be 'white' or 'black'.
                          If 'color' is requested, lines will be draw by choosing and looping 
                          through the top three colors in the image's color palette.
        line_flexibility (float): Acceptable range (-1, 1). If positive, next line choice will be in same general "direction."
                                  If negative, will allow for lines to "backtrack." Based on simple dot product theory.
        max_number_of_line_colors (int): The maximum possible number of line colors you want to cycle through.
        max_line_thickness (int): The maximum thickness of the line in units of pixels. Lines are drawn with random thickness
                                  between [1, max_line_thickness].
        bkrd_color (str): {'white', 'black'} What color the background should be.
        canny_kernal_size (int): square kernal size for canny edge detection. 50 is recommended value.
                                 The higher the number the stricter the lines will be.
                                 For more "line points" make the number lower.
        lines (int): The number of lines that should be drawn.
        view_pointmap (bool): Option to see the binary pointmap of the image.
            
    Returns:
        frames (list): Collection of all of the frames, one after another. Each frame is a 2D
                       single channel numpy array. The length of this list will be equal to the integer
                       value of lines.
    """

    #TODO: add color option for bkrd_color
    #TODO: double check color accuracy of lines...
    #TODO: auto-re-run to reassign max_number_of_line_colors if max desired can't be found
    #TODO: catch kernal size if too large right off the bat ??
    #TODO: add option to touch every point in pointmap before completion

    #read in image as grayscale
    src = cv2.imread(path, cv2.IMREAD_GRAYSCALE) 

    #get the rows, cols, chans in the image
    rows = np.shape(src)[0]
    cols = np.shape(src)[1]

    #set up the background canvas that will be drawn on
    if (bkrd_color == 'white'):

        canvas = np.ones((rows,cols, 3), np.uint8) 
    
    elif (bkrd_color == 'black'):

        canvas = np.zeros((rows, cols, 3), np.uint8)

    else:

        print("ERROR: PLEASE ENTER A VALID BACKGROUND COLOR.")
        print("BACKGROUND COLOR REQUESTED:", bkrd_color)
        return -1

    #instantiate return object and append blank canvas
    frames = []

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

        #because choosing a line "parallel" with the line previous is just unreasonable
        print("ERROR: PLEASE ENTER A VALID LINE FLEXIBILITY")
        return -1
    
    #choose the line color(s) that will be drawn with
    if (line_color == 'white'):

        line_colors = (1, 1, 1)

    elif (line_color == 'black'):

        line_colors = (0, 0, 0)

    elif (line_color == 'color'):

        hue_separation = 8
        sq = 0.7
        vq = 0.7
        space = 'bgr'
        line_colors = color.colorPalette(path, False, max_number_of_line_colors, hue_separation, sq, vq, space)

        if (len(line_colors) != max_number_of_line_colors):

            print("ERROR: YOU DUMMY, YOU ARE (PROBABLY) REQUESTING LINE COLOR FOR A GRAYSCALE IMAGE!")
            print("OR, THE COLOR PALETTE HELPER COULDN'T FIND", max_number_of_line_colors, "COLORS IN YOUR IMAGE!")
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
    pointmap = pointmap.astype(int)

    #see how many points are possible
    number_of_available_points = int(np.sum(pointmap))

    if (lines > number_of_available_points):

        print("ERROR: NOT ENOUGH AVAILABLE POINTS TO COMPLETE LINE REQUEST.")
        print("TRY DECREASING KERNAL SIZE OR DECREASING NUMBER OF LINES REQUESTED.")
        return -1


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

    #set up counter for color looping
    color_counter = 0

    #set up pbar
    pbar = ProgressBar()

    #instantiate storage to store points that have been visited
    forbidden_points = []

    #begin the lines loop
    for l in pbar(range(0, lines)):

        #reset triplet counter when it reaches limit
        if (color_counter == max_number_of_line_colors):

            color_counter = 0

        #choose source for this line
        if (l == 0):

            source_of_line = origin[0]


        else:

            source_of_line = previous_endpoint

        #append to forbid
        forbidden_points.append(source_of_line)

        #if we have visitied all posible points in the image
        #could also just compare sum of pointmap to # of lines requested right off the bat?
        if (len(forbidden_points) == np.sum(pointmap)):

            print("YOU TOUCHED ALL OF THE LINES, KID. BETTER LUCK NEXT TIME.")
            print("DECREASE YOUR KERNAL SIZE YA GOOF.")

            return -1

        #establish endpoint storage for this line
        jump_to_this_endpoint = []

        ticker = 0 #set up for case where an endpoint can't be found
        #while we haven't found an endpoint, look for one
        while (len(jump_to_this_endpoint) == 0):

            ticker = ticker + 1

            #if we search for time == size of the image, pick a new startin point elsewhere in image
            if (ticker == (rows*cols)):

                #pick a new source
                source_of_line_storage = []
                while (len(source_of_line_storage) == 0):
                    
                    r_rand = np.random.randint(0, rows)
                    c_rand = np.random.randint(0, cols)
                    my_source_of_line = (r_rand, c_rand)

                    my_chosen_point = pointmap[r_rand, c_rand]

                    if (my_chosen_point == 1):

                        source_of_line_storage.append(my_source_of_line)
                        source_of_line = source_of_line_storage[0]

                    else:

                        continue

            #get random coord
            upper_row_coord = source_of_line[0] - max_reach
            lower_row_coord = source_of_line[0] + max_reach
            
            if (upper_row_coord < 0):

                upper_row_coord = 0

            if (lower_row_coord > rows):

                lower_row_coord = rows

            left_col_coord = source_of_line[1] - max_reach
            right_col_coord = source_of_line[1] + max_reach

            if (left_col_coord < 0):

                left_col_coord = 0

            if (right_col_coord > cols):

                right_col_coord = cols

            random_row_coordinate = np.random.randint(upper_row_coord, lower_row_coord)
            random_col_coordinate = np.random.randint(left_col_coord, right_col_coord)

            #create random coord tuple
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
                
                #get the value of that point at that random coord (should be 0 or 1)
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

                #catch for divide by zero error... this shouldn't happen but it keeps happening so I'll just put this here for now
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

        #put the current state of the canvas into the list
        frames.append(np.copy(canvas))

        #if the line is black or white
        if (line_color == 'white' or line_color == 'black'):

            #draw the line and reassign canvas
            cv2.line(canvas, (source_of_line[1], source_of_line[0]), (jump_to_this_endpoint[0][1], jump_to_this_endpoint[0][0]), line_colors, thickness = np.random.randint(1, max_line_thickness))

        #if we want to cycle through the colors 
        elif (line_color == 'color'):

            bgr_value = line_colors[color_counter]

            #draw the line and reassign canvas
            cv2.line(canvas, (source_of_line[1], source_of_line[0]), (jump_to_this_endpoint[0][1], jump_to_this_endpoint[0][0]), bgr_value, thickness = np.random.randint(1, max_line_thickness))

        #++ the triplet counter
        color_counter = color_counter + 1

    
    return frames
