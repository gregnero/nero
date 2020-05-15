import numpy as np
import matplotlib.pyplot as plt
import math

def bessel(n, m, vis):

    """ Generates a Bessel function of the n'th kind.

    Note: returns only the positive values (because of even symmetry)

    Args:
        n (int): The kind of Bessel function
        m (int): The closed-form solution for a Bessel function of the n'th kind
                 is given by an infinite series. Because we can't go out to infinity,
                 this argument gives the user the option to expand out to the 
                 m'th term. The larger, the more accurate.
        vis (boolean): Option to display the function
            
    Returns:
        bessel_function (numpy.ndarray): an array containing the requested Bessel function
                     
    """
    #TODO: FIX IT (it's late, it doesn't work yet, i'm going 2 bed)

    #establish private variables
    array_resolution = 0.01
    maximum_x_value = 100

    #get the x values
    x_values = np.arange(0,maximum_x_value+array_resolution, array_resolution)

    #instantiate return array
    bessel_function = np.zeros(len(x_values))

    for x in range(0,len(x_values)):

        x_value = x_values[x]

        my_summation_value = 0

        for m in range(0,m+1):

            current_value = (np.power(-1, m) * np.power(x_value, 2*m)) / (np.power(2, (2*m)+n) * math.factorial(m) * math.factorial(n + m))

            my_summation_value = my_summation_value + current_value

        my_bessel_value = np.power(x_value, n) * my_summation_value

        bessel_function[x] = my_bessel_value

    if (vis == True):

        fig, ax = plt.subplots(1, 1, figsize = (5,5))

        ax.plot(x_values, bessel_function)
        ax.set_title("Bessel Function of Kind " + str(n))
        
        plt.show()

    return bessel_function
