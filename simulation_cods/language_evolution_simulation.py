#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dissertation Project - Modelling Language Evolution using Statistical Physics

Simulation of Language Evolution using the research conducted by Henri 
Kauhanen. 

Yellow cells denote the existence of that linguistic feature and blue cells 
are communities without that feature.

Models a toroidal universe due to its periodic boundary conditions
@author: Qi Nohr Chen
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import matplotlib.collections as mc
from scipy import interpolate
#import imageio
#import os

REALIZATION = 1
GRID_SIZE = 4
NUMBER_OF_BORDERS = 2*GRID_SIZE*(GRID_SIZE-1)
TRIALS = 16
PROBABILITY_VERTICAL = 0.5 #1-q
PROBABILITY_HORIZONTAL = 0.5 #q
PROBABILITY_EGRESS_VERT = 1 # Getting the yellow feature from out of nowhere
PROBABILITY_INGRESS_VERT = 0  # Losing the yellow feature from within a community
PROBABILITY_EGRESS_HORIZONTAL = 0 # not adopting blue feature from neighbor
PROBABILITY_INGRESS_HORIZONTAL = 0 # not adopting neighbor yellow feature
p = PROBABILITY_EGRESS_VERT + PROBABILITY_INGRESS_VERT
p_prime = PROBABILITY_EGRESS_HORIZONTAL + PROBABILITY_INGRESS_HORIZONTAL

def fitting_tau_and_hash(tau_point):
    """
    Takes in a linguistic temperature and returns a H(tau) using interpolation
    """
    opened_data = pd.read_csv("tau_hash.csv", header=None)
    tau = opened_data[0]
    hash_d = opened_data[1]
    #new_tau = np.linspace(0.0000000999999999999999,1000,100000)
    #fig, ax = plt.subplots()
    fit = interpolate.interp1d(tau, hash_d, kind = 'cubic')
    #plt.plot(tau,hash_d, "o", new_tau, fit(new_tau), "-")
    #plt.show()
    return float(fit(tau_point))

def frequency_of_feature_in_stationary_distribution():
    """
    Calculates the frequency of a feature in a stationary distribution
    """
 
    top = (PROBABILITY_VERTICAL*
           PROBABILITY_INGRESS_VERT)+(PROBABILITY_HORIZONTAL*
                                      PROBABILITY_INGRESS_HORIZONTAL)
    bottom = PROBABILITY_VERTICAL*p+PROBABILITY_HORIZONTAL*p_prime
    rho = top/bottom
    return rho

def tau():
    """
    This parameter gives the relative rate
    of unfaithful transmission events (i.e., mutations) over faithful
    transmission events
    """
    top =(PROBABILITY_VERTICAL*p+PROBABILITY_HORIZONTAL*p_prime)
    bot = (PROBABILITY_HORIZONTAL*(1-p_prime))
    
    tau = top/bot
    return tau
    
def generate_initial():
    
    """
    Generates the inital grid of the system with randomly and uniformly
    distributed linguistic features.
    """
    inital_color = np.random.rand(GRID_SIZE,GRID_SIZE)
    return inital_color

def change_elements(float_map):
    """
    Takes in a map from the initially generated grid and turns the floats into
    integers.

    """
    data = float_map
    for row in range(len((data))):
        for column in range(len((data))):
            if data[row,column] > 0.5:
                data[row,column] = 1
            else:
                data[row,column] = 0
    return data

def color_map(data,filename):
    """
    Creates a color map and takes in the data from the map created earlier as
    well as a filename that is used to create an animation.
    """
    # create discrete colormap
    cmap = colors.ListedColormap(['yellow', 'blue'])
    bounds = [0,1,20]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    fig, ax = plt.subplots()
    ax.imshow(data, cmap=cmap, norm=norm)
    
    # draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='black')
    ax.set_xticks(np.arange(-.5, GRID_SIZE, 1))
    ax.set_yticks(np.arange(-.5, GRID_SIZE, 1))
    plt.title("Model of Language Evolution", fontsize=10)
    plt.Circle((0,0),2)
    ax.grid(False)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    #plt.savefig(filename, dpi=1200)
    plt.show()
    plt.close()
    
    return filename

def final_plot_with_circles(list_circles,data):
    """
    Plot of data, but it also adds circles on the boundaries.
    """
    
    sizes = len(list_circles)*[200]
    xy = list_circles
    
    patches = [plt.Circle(center, size) for center, size in zip(xy, sizes)]
    cmap = colors.ListedColormap(['blue', 'yellow'])
    bounds = [0,1,20]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    fig, ax = plt.subplots()
    ax.imshow(data, cmap=cmap, norm=norm)
    
    # draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='white')
    ax.set_xticks(np.arange(-.5, GRID_SIZE, 1))
    ax.set_yticks(np.arange(-.5, GRID_SIZE, 1))
    plt.title("Isogloss", fontsize=10)
    plt.Circle((0,0),2)
    ax.grid(True)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    collection = mc.CircleCollection(sizes, offsets=xy, transOffset=ax.transData, color='black')
    ax.add_collection(collection)
  
    plt.savefig("Language Evolution Map with Isogloss.png", dpi = 1200)
    plt.show()
   

def event():
    """
    Throws a dice to edcide whether a vertical or horizontal event happens
    """
    
    dice = np.random.rand()
    if dice > PROBABILITY_VERTICAL:
        return 1 #Int signify horizontal
    else:
        return 0 #Int signify vertical

def vertical_event_ingress():
    """
    Throws a dice to devide whether vertical ingression was successful
    """
    dice = np.random.rand()
    if dice < PROBABILITY_INGRESS_VERT:
        return True
    else:
        return False

def vertical_event_egress():
    """
    Throws a dice to determine wehter verticel egression was successful
    """
    dice = np.random.rand()
    if dice < PROBABILITY_EGRESS_VERT:
        return True
    else:
        return False
    
def horizontal_event_ingress():
    """
   Throws a dice to determine whether horizontal ingression was successful
    """
    dice = np.random.rand()
    if dice < PROBABILITY_INGRESS_HORIZONTAL:
        return True
    else:
        return False

def horizontal_event_egress():
    """
    Throws a dice to determine whether horizontal egression was successful
    """
    dice = np.random.rand()
    
    if dice < PROBABILITY_EGRESS_HORIZONTAL:
        return True
    else:
        return False
    
def horizontal_walk(boo,x_coord,y_coord): #EDIT THIS FOR PERIODIC BOUNDARY CONDITIONS
    """
    Will randomly decide on a direction that won't cause an error in the
    simulation
    """
    found = False
    while found == False:
        direction =  np.random.randint(1,5)
        if direction == 1:
            if y_coord-1 < 0:
                found = True
                y_coord = GRID_SIZE-1
                return x_coord, y_coord
            else:
                found = True
                return x_coord,y_coord-1
        elif direction == 2:
            if x_coord+1 > GRID_SIZE-1:
                found = True
                x_coord = 0
                return x_coord, y_coord
            else:
                found = True
                return x_coord+1,y_coord
        elif direction == 3:
           
            if y_coord+1 > GRID_SIZE-1:
                found = True
                y_coord = 0
                return x_coord, y_coord
            else:
                found = True
                return x_coord,y_coord+1
        else:
            if x_coord-1 < 0:
                found = True
                x_coord = GRID_SIZE-1
                return x_coord, y_coord
            else:
                found = True
                return x_coord-1,y_coord
            

def isogloss_calculator(data): #EDIT THIS FOR PERIODIC BOUNDARY CONDITIONS
    """
    Function calculates the number of blue to yellow or yellow to blue
    boundaries from which the isogloss density can be calculated. Will also
    mark the boundaries using a tuple which will then later be graphed

    """
    
    counter = 0
    border_list =[]
    
    for row in range(len((data))):
       for column in range(len((data))):
           
           #General Walk from right to left and downwards
           if row < GRID_SIZE-1 and column < GRID_SIZE-1:
               border_cen = data[row,column]
               border_right = data[row,column+1]
               border_down = data[row+1,column]
               #Check if the cell right side is equal
               if border_cen != border_right:
                   counter = counter + 1
                   dot = (0.5+column,0+row)
                   border_list.append(dot)
                   #Check if cell bottom is equal
                   if border_cen != border_down:
                       counter = counter + 1
                       dot = (0+column,0.5+row)
                       border_list.append(dot)
                #Right check
               elif border_cen != border_down:
                   counter = counter + 1
                   dot = (0+column,0.5+row)
                   border_list.append(dot)
                   #Bottom check
                   if border_cen != border_right:
                       counter = counter + 1
                       dot = (0.5+column,0+row)
                       border_list.append(dot)
           #Right check only cause of index
           elif row == GRID_SIZE-1 and column != GRID_SIZE-1:
               border_cen = data[row,column]
               border_right = data[row,column+1]
               
               if border_cen != border_right:
                   counter = counter + 1
                   dot = (0.5+column,0+row)
                   border_list.append(dot)
           #Bottom check only cause of index 
           elif column == GRID_SIZE-1 and row != GRID_SIZE-1:
               border_cen = data[row,column]
               border_down = data[row+1,column]
               if border_cen != border_down:
                   counter = counter + 1
                   dot = (0+column,0.5+row)
                   border_list.append(dot)
          
    return counter, border_list

def calculate_freq_feature(data):
    """
    Takes in the integer map and counts the frequency of features numerically.
    """
    counter= 0
    
    for row in range(len((data))):
       for column in range(len((data))):
           if data[row,column] == 0:
               counter = counter + 1
               
    return counter/(GRID_SIZE**2)

def graph_freq_feat(freq_data,time):
    
    plt.xlabel('Time (Monte Carlo Sweeps)')
    plt.axhline(y=frequency_of_feature_in_stationary_distribution(), 
                color='r', linestyle='-')
    # naming the y axis
    plt.ylabel('Frequency of Features (Average)')
    # giving a title to my graph
    plt.title('Frequency of Features (Averages) against Time')
    plt.scatter(time, freq_data)
    plt.savefig("Freq.png", dpi = 1200)
    plt.show()
    
def graph_isogloss_density(iso_data,time):
    
    t_freq = frequency_of_feature_in_stationary_distribution()
    hash_d = fitting_tau_and_hash(tau())
    isogloss = 2*hash_d * (1-t_freq)*t_freq
    plt.xlabel('Time (Monte Carlo Sweeps)')
    plt.axhline(y=isogloss, color='r', linestyle='-')
    # naming the y axis
    plt.ylabel('Isogloss density (Average)')
    # giving a title to my graph
    plt.title('Isogloss Density (Averaged) against Time')
    plt.scatter(time, iso_data)
    plt.savefig("Isogloss.png", dpi = 1200)
    plt.show()

def experiment(isogloss):

    counter = 0
    inital_color = generate_initial()
    integer_map = change_elements(inital_color)
    color_map(integer_map, str(counter))
    files= [] #File names that are used to create a GIF
    freq_feature = []
    frequency_summed = []
    isogloss = []
    isogloss_summed = []
    time_array = []
    
    for trials in range(TRIALS):
        y,x = np.random.randint(0,GRID_SIZE, size=(2))
        event_indicator = event()
        if event_indicator == 1 and integer_map[y,x] == 1:#If it is a horizontal event and it is yellow (Ingress)
            boolean = horizontal_event_ingress()
            x_new_cell, y_new_cell = horizontal_walk(boolean,x,y)
            if boolean == True:
                integer_map[y_new_cell,x_new_cell] = 0
                counter = counter + 1
            else:
                integer_map[y_new_cell,x_new_cell] = 1
                counter = counter + 1
        elif event_indicator == 1 and integer_map[y,x] == 0: #If it's horizontal and blue (egress)
            boolean = horizontal_event_egress()
            x_new_cell, y_new_cell = horizontal_walk(boolean,x,y)
            if boolean == True:
                integer_map[y_new_cell,x_new_cell] = 1
                counter = counter + 1
            else:
                integer_map[y_new_cell,x_new_cell] = 0
                counter = counter + 1
        elif event_indicator == 0 and integer_map[y,x] == 1: #If it's vertical and yellow (Ingress)
            boolean = vertical_event_ingress()
            if boolean == True:
                integer_map[y,x] = 0
                counter = counter + 1
            else:
                integer_map[y,x] = 1
                counter = counter + 1
        else: # #If it's vertical and Blue (egress)
            boolean = vertical_event_egress()
            if boolean == True:
                integer_map[y,x] = 1
                counter = counter + 1
            else:
                integer_map[y,x] = 0
                counter = counter + 1
        if counter % GRID_SIZE**2 == 0:
            name = str(counter)
            frequency = calculate_freq_feature(integer_map)
            
            freq_feature.append(frequency)
         
            freq_sum = freq_feature
            
            frequency_summed.append(freq_sum)
            count, borders = isogloss_calculator(integer_map)
            isogloss.append(count/NUMBER_OF_BORDERS)
            iso_sum = (isogloss)
            #print("Isogloss Mean,", iso_sum)
            isogloss_summed.append(iso_sum)
            print(counter)
            time_array.append(counter/GRID_SIZE**2)
            
            #GIF CREATING - START
            filename = color_map(integer_map, name)
            # filename = filename+".png"
            # files.append(filename)
            
    # with imageio.get_writer('mygif.gif', mode='I') as writer:
    #     for filename in files:
    #         image = imageio.imread(filename)
    #         writer.append_data(image)
        
    # for filename in set(files):
    #     os.remove(filename)
    #GIF CREATING - END
        
    iso_count, borders = isogloss_calculator(integer_map)
    graph_freq_feat(freq_feature,time_array)
    graph_isogloss_density(isogloss, time_array)
    if isogloss == True:
        final_plot_with_circles(borders,integer_map)
    print("Tau is theoretically:", tau())
    print("Frequency of features is theoretically:", 
          frequency_of_feature_in_stationary_distribution())
    print("Isogloss density is:", iso_count/NUMBER_OF_BORDERS)
    t_freq = frequency_of_feature_in_stationary_distribution()
    hash_d = fitting_tau_and_hash(tau())
    isogloss_t = 2*hash_d * (1-t_freq)*t_freq
    print("Isogloss density theoretically is:", isogloss_t)
    
    return freq_feature, time_array, isogloss


def _main_():

    data_in, time, iso_data_in = np.array((experiment(False)))
    
    for _ in range(REALIZATION-1):
         data, time, iso_data = (experiment(False))
         data = np.array(data)
         iso_data = np.array(iso_data)
         data_in = np.vstack((data_in,data))
         iso_data_in = np.vstack((iso_data_in,iso_data))
         
    
    iso_average = np.mean(iso_data_in, axis=0)     
    f_averages = np.mean(data_in, axis=0)
    graph_freq_feat(f_averages,time)
    graph_isogloss_density(iso_average, time)
    np.savetxt("iso_average.csv", iso_average)
    np.savetxt("frequency_average.csv", f_averages)
    

_main_()    

"""
Section Below is for Debugging
"""

# print("Tau is theoretically:", tau())
# print("Frequency of features is theoretically:", 
#       frequency_of_feature_in_stationary_distribution())

# t_freq = frequency_of_feature_in_stationary_distribution()
# hash_d = fitting_tau_and_hash(tau())
#isogloss_t = 2*hash_d * (1-t_freq)*t_freq
#print("Isogloss density theoretically is:", isogloss_t)


# inital_color = generate_initial()
# integer_map = change_elements(inital_color)
# color_map(integer_map, str(0))
# iso_count, borders = isogloss_calculator(integer_map)
# final_plot_with_circles(borders,integer_map)