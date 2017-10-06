# -*- coding: utf-8 -*-
"""
Created on Tue May 17 16:18:15 2016
Function to generate the aggregate values of the pivot table
Can be modified to generate it by state, divison or reigon.

Inputs:  Which aggregate method to use
         Which category is being summarised

Outputs: A list of lists of summarised data (summary)

@author: Tin Bao (760391), Tony Nguyen and Ming Yau Liang 
INFO20002 University of Melbourne
"""
import csv

# Constants
DATA = 11
STATE = 2
DIVISON = 1
REGION = 0
TYPE = NAME = 0
NUMFRG = 7
RES = 6
YEARBIN = 5
CLIMATE = 4
HOUSE = 3
NUMTV = 8
EMPLOY = 9
SPOUSE = 10

# Makes a new list of lists of the columns of data
def make_new_list(head_list):
    num_cols = len(head_list)
    stats = []
    for column in range(num_cols):
        stats.append([])
    return stats
    
# Gives a type for the data set (either integer, float or string)
def append_type(stats, data, column):
    flag = True
    try:
        # check if the data is a string
        float(data)
    except ValueError:
        stats[column].append(data)
        if not isinstance(stats[column][TYPE], type):
            stats[column].insert(TYPE, str)
        flag = False
        
    if flag:
        try:
            # check if the data is an integer
            stats[column].append(int(data))
            if not isinstance(stats[column][TYPE], type):
                stats[column].insert(TYPE, int)
        except ValueError:
            # if not all of the above, the data is a float
            stats[column].append(float(data))
            if not isinstance(stats[column][TYPE], type):
                stats[column].insert(TYPE, float)
    
    return stats

# Returns the average value of the data
def average(values):
    if len(values) == 0 or sum(values) == 0:
        return '-'
    size = count_of(values)
    return sum(values) / size

# Returns the sum of the data 
def sum_of(values):
    return sum(values)

# Returns the smallest data point 
def minimum(values):
    if len(values) == 0 or sum(values) == 0:
        return '-'
    mini = max(values)  # Will always be above zero if data is valid
    for data in values:
        # Zero data doesn't count as minimums
        if data != 0 and data < mini:
            mini = data
    return mini

# Returns the largest data point 
def maximum(values):
    if len(values) == 0 or sum(values) == 0:
        return '-'
    return max(values)

# Returns the mode(s) of the data
def find_modes(void_list):
    if len(void_list) == 0:
        return '-'
    mode_dict = {}
    modes = []
    for item in void_list:
        if item not in mode_dict:
            mode_dict[item] = 1
        else:
            mode_dict[item] += 1
    max_count = max(mode_dict.values())
    for element, count in mode_dict.items():
        if count == max_count:
            modes.append(element)
    return sorted(modes)

# Returns the total number legitimate data 
def count_of(values):
    if len(values) == 0:
        return '-'
    count = 0
    for data in values:
        if data != 0:
            count += 1  
    return count

# Generates a 2D-array with the number of elements of size
def make_empty_2dlist(size):
    return [list('') for _ in xrange(size)]

# Filters the numerical data based on the filter selection
def pre_process(stats, filt):
    filtrd_stats = stats[0:DATA]
    filtrd_stats.append(stats[filt+DATA])
    return filtrd_stats

# Summarises data based on user selction
def aggregate_data(stats, column, row, agg_func, fil):
    # Sorts either by STATE, DIVISON or REGION
    if column == REGION:
        size = 4
    elif column == DIVISON:
        size = 10
    else:
        size = 27

    if row == RES:
        innersize = 14
    elif row == CLIMATE or row == HOUSE:
        innersize = 5
    elif row == YEARBIN:
        innersize = 8
    elif row == NUMTV:
        innersize = 16
    elif row == NUMFRG:
        innersize = 11
    elif row == EMPLOY:
        innersize = 3
    else:
        innersize = 2

    # Filters the data
    fil_stats = pre_process(stats, fil)

    # Creates a list of column data of selections
    static_list = make_empty_2dlist(size)
    for i in range(size):
        static_list[i] = [list('') for _ in xrange(innersize)]

    depth = 1
    for data in fil_stats[DATA][1:]:
        pos = fil_stats[row][depth]
        static_list[fil_stats[column][depth]-1][pos-1].append(data)
        depth += 1

    # Summarises the data based on the agg_func selected
    count = 0
    agg_list = make_empty_2dlist(size)
    for group in static_list:
        for data in group:
            agg_list[count].append(agg_func(data))
        count += 1

    return agg_list

### MAIN FUNCTION ###
def calc_agg(agg_method, yaxis, xaxis, filter_select):
    fp = open('datar.csv')
    data = csv.reader(fp)
    # keeps the first row of names for the column names
    head = next(data)
    stats = make_new_list(head)

    # Appends a type to the front of the data
    for row in data:
        num = 0
        for entry in row[:]:
            stats = append_type(stats, entry, num)
            num += 1

    fp.close()

    if agg_method == 1:
        summary = aggregate_data(stats, yaxis, xaxis, average, filter_select)
    elif agg_method == 2:
        summary = aggregate_data(stats, yaxis, xaxis, sum_of, filter_select)
    elif agg_method == 3:
        summary = aggregate_data(stats, yaxis, xaxis, minimum, filter_select)
    elif agg_method == 4:
        summary = aggregate_data(stats, yaxis, xaxis, maximum, filter_select)
    elif agg_method == 5:
        summary = aggregate_data(stats, yaxis, xaxis, find_modes, filter_select)
    elif agg_method == 6:
        summary = aggregate_data(stats, yaxis, xaxis, count_of, filter_select)

    return summary

