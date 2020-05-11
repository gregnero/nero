#import dependencies
import networkx as nx
import numpy as np

def SIR(N, k, p, h_0, i, r, b, T):

    '''
    Author: Gregory M. Nero (gmn8357@rit.edu)

    Description: Runs a probabilistic SIR epidemic model on a network

    Parameters:
        N (int): the total number of nodes in the network
        k (int): each node is initially connected to its k nearest neighbors
        p (float): the Watts-Strogatz rewiring probability; low values of p represent more clustering
        h_0 (float): the initial health of the population
        i (float): the probability of infection
        r (float): the probability of recovery
        b (float): the probability of of an edge breaking and rewiring
        T (int): max amount of dimensionless time you want to simulate for

    Returns:
        t (int): dimensionless time to termination condition
    '''

    #TODO: implement b parameter

    '''
    LEGEND FOR NODE LABELS:
    SUSCEPTIBLE = -1
    INFECTED = 0
    RECOVERED = 1
    '''

    #get the number of initially susceptible and infected people
    initially_susceptible = int(((h_0) * N) / (1 + h_0))
    initially_infected = int(N - initially_susceptible)

    #create and shuffle labels for population
    labels_for_initial_population = np.zeros(N, dtype = int)
    labels_for_initial_population[0:initially_susceptible-1] = -1
    np.random.shuffle(labels_for_initial_population)

    #create the network
    G = nx.watts_strogatz_graph(N, k, p)

    #convert the array of states to dictionary to assign attributes later
    labels_for_initial_population_dict = {}
    for idx, node in enumerate(G.nodes()):
        labels_for_initial_population_dict[node] = labels_for_initial_population[idx]

    #assign the status of the initial population to the nodes
    nx.set_node_attributes(G, name = 'status', values = labels_for_initial_population_dict)

    for time in range(0,T):

        #for t = 0, set previous to initial population
        if (time == 0):

            previous_status_dict = labels_for_initial_population_dict

        else:

            previous_status_dict = new_status_dict

        #instantiate storage for this time
        new_status_dict = {}

        #perform this round of infection, recovery, and breaking
        for n in range(0, N):

            #get the status of this current node
            node_status = previous_status_dict[n]

            #get the neighbors of the current node
            neighbors = list(G[n])

            #instantiate storage for neighbor status
            status_of_neighbors = []

            #for all of the neighbors
            for s in range(0,len(neighbors)):

                #get neighbor number
                neighbor = neighbors[s]

                #get neighbor status
                neighbor_status = previous_status_dict[neighbor]

                #append that status to the list
                status_of_neighbors.append(neighbor_status)

            #if they are susceptible, give chance to be infected
            if (node_status == -1):

                #get the infection decision
                infection_decision = np.random.binomial(1, i)

                #get condition for if at least one neighbor is infected
                is_neighbor_infected = (0 in status_of_neighbors)

                #if infection was successful
                if (infection_decision == 1 and (is_neighbor_infected == True)):

                    #update status to infected
                    new_status_dict[n] = 0

                #else, the new status is just the old status
                else:

                    new_status_dict[n] = node_status

            #if they are infected, give chance to recover
            elif (node_status == 0):

                #get the recovery decision
                recovery_decision = np.random.binomial(1, r)

                #if recovery was successful
                if (recovery_decision == 1):

                    #update status to recovered
                    new_status_dict[n] = 1

                #else, the new status is just the old status
                else:

                    new_status_dict[n] = node_status

            #if they are recovered let them be
            #TODO: implement breaking functionality
            elif (node_status == 1):

                #if they are recovered, let them stay recovered
                new_status_dict[n] = node_status

        #if there are no more infected nodes (of state 0) in the population, terminate
        if ((0 in new_status_dict.values()) == False):

            return time
