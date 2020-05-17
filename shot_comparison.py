import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.signal import find_peaks

ama_w = './dati/akmentins_wrist.csv'
ama_s = './dati/akmentins_slap.csv'
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
    acc_z_arr = savgol_filter(acc_z_arr, 9, 3)
    return acc_z_arr

##
# Function call and save
# returned array in a variable
##
ama_w_data = getData(ama_w)
ama_s_data = getData(ama_s)
pro1_w_data = getData(pro1_w)
pro1_s_data = getData(pro1_s)

##
# Find peaks for each
# hockey player's shot
# data
##
ama_w_peaks, _ = find_peaks(ama_w_data, prominence=8)
ama_s_peaks, _ = find_peaks(ama_s_data, prominence=15)
pro1_w_peaks, _ = find_peaks(pro1_w_data, prominence=8)
pro1_s_peaks, _ = find_peaks(pro1_s_data, prominence=20)

##
# Find index for best
# peak in hockey player's
# shot data
##
def bestShotCoordinates(shot_data, peaks):
    best_shot_coordinates = peaks[0]
    for i in np.nditer(peaks):
        if shot_data[best_shot_coordinates] < shot_data[i]:
            best_shot_coordinates = i
    return best_shot_coordinates

##
# Function call and save
# each hockey player's best
# shot index in variable
##
ama_w_best_i = bestShotCoordinates(ama_w_data, ama_w_peaks)
ama_s_best_i = bestShotCoordinates(ama_s_data, ama_s_peaks)
pro1_w_best_i = bestShotCoordinates(pro1_w_data, pro1_w_peaks)
pro1_s_best_i = bestShotCoordinates(pro1_s_data, pro1_s_peaks)

##
# Get 50 values of
# linear acceleration
# from the hockey player's
# best shot
##
def bestShotArr(best_shot_coordinate, shot_data):
    i = 50
    best_shot_acc_list = []
    best_shot_coordinate = best_shot_coordinate+3
    while i >= 0:
        best_shot_acc_list.append(shot_data[best_shot_coordinate-i])
        i = i - 1
    best_shot_acc_array = np.array(best_shot_acc_list)
    return best_shot_acc_array

##
# Function call and save
# each hockey player's best
# shot data array in variable
##
ama_w_best = bestShotArr(ama_w_best_i, ama_w_data)
ama_s_best = bestShotArr(ama_s_best_i, ama_s_data)
pro1_w_best = bestShotArr(pro1_w_best_i, pro1_w_data)
pro1_s_best = bestShotArr(pro1_s_best_i, pro1_s_data)

##
# Plot each hockey player's best
# wrist shot in one graph
##
plt.plot(ama_w_best, label="Entuziasta labākais plaukstas metiens")
plt.plot(pro1_w_best, label="Profesionāļa labākais plaukstas metiens")
plt.ylabel("Lineārais paātrinājums (m/s/s)")
plt.xlabel("Indekss")
plt.legend()
plt.show()

##
# Plot each hockey player's best
# slap shot in one graph
##
plt.plot(ama_s_best, label="Entuziasta labākais šķēliens")
plt.plot(pro1_s_best, label="Profesionāļa labākais šķēliens")
plt.ylabel("Lineārais paātrinājums (m/s/s)")
plt.xlabel("Indekss")
plt.legend()
plt.show()


            

    

