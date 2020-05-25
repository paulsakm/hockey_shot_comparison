import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

##
# Data file paths
## 
ama_w = './dati/akmentins_wrist.csv'
ama_s = './dati/akmentins_slap.csv'
ama2_w = './dati/potapovs_wrist.csv'
ama2_s = './dati/potapovs_slap.csv'
ama3_w = './dati/bisnieks_wrist.csv'
ama3_s =  './dati/bisnieks_slap.csv'
pro1_w = './dati/dzierkals_wrist.csv'
pro1_s = './dati/dzierkals_slap.csv'


##
# Function for importing data,
# rounding floats and smoothing
# each linear acceleration
##
def getData(filename):
    data = pd.read_csv(filename)
    df = pd.DataFrame(data, columns = ['acc_x,', 'acc_y', 'acc_z'])
    df['acc_z'] = df['acc_z'].astype('float64')
    acc_z_arr = df['acc_z'].values
    acc_z_arr = np.round(acc_z_arr, 2)
    return acc_z_arr

##
# Function call and save
# returned array in a variable
##
ama_w_data = getData(ama_w)
ama_s_data = getData(ama_s)
ama2_w_data = getData(ama2_w)
ama2_s_data = getData(ama2_s)
ama3_w_data = getData(ama3_w)
ama3_s_data = getData(ama3_s)
pro1_w_data = getData(pro1_w)
pro1_s_data = getData(pro1_s)


min_prctg = 0.2
top_peak_count = 5

##
# Function for evaluating and 
# finding the amount of
# hockey shots asked in parameter
##
def getTopPeaks(min_prctg, top_peak_count, shot_data):
    tmp_height = min_prctg * max(shot_data)
    tmp_data_peaks, _ = find_peaks(shot_data, height=tmp_height)
    i = 0
    while i < len(tmp_data_peaks)-1:
        tmp_data_peaks[i] = tmp_data_peaks[i+1] - tmp_data_peaks[i]
        i += 1
    i = 0
    tmp_arr = []
    tmp_max = max(tmp_data_peaks[0:len(tmp_data_peaks)-1])
    while i < tmp_data_peaks.size-1:
        if min_prctg * tmp_max < tmp_data_peaks[i]:
            tmp_arr.append(tmp_data_peaks[i])
        i += 1
    tmp_data_peaks, _ = find_peaks(shot_data, height=tmp_height, distance=min(tmp_arr))
    tmp_arr = []
    i = 0
    while i < len(tmp_data_peaks):    
        tmp_arr.append(shot_data[tmp_data_peaks[i]])
        i += 1
    tmp_arr = np.sort(tmp_arr)[::-1]
    if len(tmp_arr) > top_peak_count:
        tmp_arr = tmp_arr[0:top_peak_count]
    tmp_arr2 = []
    j = 0
    while j < len(tmp_arr):   
        i = 0
        while i < len(tmp_data_peaks):   
            if shot_data[tmp_data_peaks[i]] == tmp_arr[j]:
                tmp_arr2.append(tmp_data_peaks[i])            
            i += 1
        j += 1
    tmp_arr2 = np.sort(tmp_arr2)
    return tmp_arr2


##
# Find best 5 shots captured 
# within wrist shot data
##
ama_w_peaks = getTopPeaks(min_prctg, top_peak_count, ama_w_data)
ama2_w_peaks = getTopPeaks(min_prctg, top_peak_count, ama2_w_data)
ama3_w_peaks = getTopPeaks(min_prctg, top_peak_count, ama3_w_data)
pro1_w_peaks = getTopPeaks(min_prctg, top_peak_count, pro1_w_data)


##
# Find best 5 shots captured
# within slap shot data
##
ama_s_peaks = getTopPeaks(min_prctg, top_peak_count, ama_s_data)
ama2_s_peaks = getTopPeaks(min_prctg, top_peak_count, ama2_s_data)
ama3_s_peaks = getTopPeaks(min_prctg, top_peak_count, ama3_s_data)
pro1_s_peaks = getTopPeaks(min_prctg, top_peak_count, pro1_s_data)


##
# Calculating average shot
# from the given top peaks
##
def avgShot(shot_data, top_peaks, cut_off_first = 0.5):
    tmp_distance = top_peaks.copy()
    i = 0
    while i < len(tmp_distance)-1:
        tmp_distance[i] = tmp_distance[i+1] - tmp_distance[i]
        i += 1
    min_distance = int((1-cut_off_first) * min(tmp_distance[0:len(tmp_distance)-1]))
    j = 0
    list_arr = []
    while j < len(top_peaks):
        list_arr.append([])
        index = top_peaks[j] - min_distance
        while index <= top_peaks[j]:
            if index >= 0:
                list_arr[j].append(shot_data[index])            
            else: 
                list_arr[j].append(0)
            index += 1
        j += 1
    average_arr = []
    i = 0
    while i <= min_distance:    
        j = 0
        summ = 0
        while j < len(list_arr):
            summ += list_arr[j][i]        
            j += 1
        average_arr.append(summ/len(list_arr)) 
        i += 1
    return average_arr

##
# Find average shot of 
# 5 best shots of each hockey
# player's wrist shot data
##
ama_w_avg = avgShot(ama_w_data, ama_w_peaks)
ama2_w_avg = avgShot(ama2_w_data, ama2_w_peaks)
ama3_w_avg = avgShot(ama3_w_data, ama3_w_peaks)
pro1_w_avg = avgShot(pro1_w_data, pro1_w_peaks)

##
# Find average shot of 
# 5 best shots of each hockey
# player's slap shot data
##
ama_s_avg = avgShot(ama_s_data, ama_s_peaks)
ama2_s_avg = avgShot(ama2_s_data, ama2_s_peaks)
ama3_s_avg = avgShot(ama3_s_data, ama3_s_peaks)
pro1_s_avg = avgShot(pro1_s_data, pro1_s_peaks)


##
# Function for making
# all hockey shot data
# array with equal index
# length
##
def makeEvenArrays(arr1, arr2):
    if len(arr1) > len(arr2):
        tmp1 = arr1.copy()
        tmp2 = arr2
    else:
        tmp1 = arr2.copy()
        tmp2 = arr1        
    i = 0
    j = len(tmp1) - len(tmp2)
    while i < len(tmp1):
        if i >= j: 
            tmp1[i] = tmp2[i - j]
        else:
            tmp1[i] = 0
        i += 1  
    return tmp1

##
# Get max value for
# each hockey player's
# wrist shot average 
##
print("Wrist shot's max linear acceleration values in avg shots")
ama_w_max = max(ama_w_avg)
print(ama_w_max)
ama2_w_max = max(ama2_w_avg)
print(ama2_w_max)
ama3_w_max = max(ama3_w_avg)
print(ama3_w_max)
pro1_w_max = max(pro1_w_avg)
print(pro1_w_max)

##
# Calculate how much
# amateur's avg wrist shot 
# corresponds with 
# professionals shot
#
print("How close to professional's wrist shot")
ama_w_prc = (ama_w_max / pro1_w_max) * 100
print(ama_w_prc)

ama2_w_prc = (ama2_w_max / pro1_w_max) * 100
print(ama2_w_prc)

ama3_w_prc = (ama3_w_max / pro1_w_max) * 100
print(ama3_w_prc)


#
# Get max value for
# each hockey player's
# slap shot average 
##
print("Slap shot's max linear acceleration values in avg shots")
ama_s_max = max(ama_s_avg)
print(ama_s_max)
ama2_s_max = max(ama2_s_avg)
print(ama2_s_max)
ama3_s_max = max(ama3_s_avg)
print(ama3_s_max)
pro1_s_max = max(pro1_s_avg)
print(pro1_s_max)

##
# Calculate how much
# amateur's avg wrist shot 
# corresponds with 
# professionals shot
##
print("How close to professional's slap shot")
ama_s_prc = (ama_s_max / pro1_s_max) * 100
print(ama_s_prc)
ama2_s_prc = (ama2_s_max / pro1_s_max) * 100
print(ama2_s_prc)
ama3_s_prc = (ama3_s_max / pro1_s_max) * 100
print(ama3_s_prc)

##
# Make arrays with the
# same amount of data
##
tmp_arr = makeEvenArrays(ama_w_avg, ama2_w_avg)
if len(ama_w_avg) > len(ama2_w_avg):
    ama2_w_avg = tmp_arr
else:
    ama_w_avg = tmp_arr

tmp_arr = makeEvenArrays(ama2_w_avg, ama3_w_avg)
if len(ama2_w_avg) > len(ama3_w_avg):
    ama3_w_avg = tmp_arr
else:
    ama2_w_avg = tmp_arr

##
# Make arrays with the
# same amount of data
##
tmp_arr = makeEvenArrays(ama_s_avg, ama2_s_avg)
if len(ama_s_avg) > len(ama2_s_avg):
    ama2_s_avg = tmp_arr
else:
    ama_s_avg = tmp_arr

tmp_arr = makeEvenArrays(ama2_s_avg, ama3_s_avg)
if len(ama2_s_avg) > len(ama3_s_avg):
    ama3_s_avg = tmp_arr
else:
    ama2_s_avg = tmp_arr










            

    

