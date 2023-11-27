import math
import numpy as np
from numpy import array
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.pyplot import figure, show, rc
import pandas as pd
import glob
import csv
import sklearn as sk
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")

# define useful functions

def adjacent_values(vals, q1, q3):
    upper_adjacent_value = q3 + (q3 - q1) * 1.5
    upper_adjacent_value = np.clip(upper_adjacent_value, q3, vals[-1])

    lower_adjacent_value = q1 - (q3 - q1) * 1.5
    lower_adjacent_value = np.clip(lower_adjacent_value, vals[0], q1)
    return lower_adjacent_value, upper_adjacent_value


def set_axis_style(ax, labels):
    ax.xaxis.set_tick_params(direction='out')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    ax.set_xlabel('Sample name')

n_features = 9

names =  names = ['BX (nT GSE/GSM)','BY (nT GSE)','BZ (nT GSE)','Vx Velocity (km/s)','Vy Velocity (km/s)','Vz Velocity (km/s)','Proton Density (n/cc)''Proton Temperature (eV)','Flow Pressure (nPa)']

maven_yhat_reshaped = np.loadtxt(r'D:\forecasting_study\maven_multistep_cnn_3_hour_input_before_2_hour_input_after_9_features_30_min_yhat_sigmoid.txt')
y_test_reshaped = np.loadtxt(r'D:\forecasting_study\maven_multistep_cnn_3_hour_input_before_2_hour_input_after_9_features_30_min_y_test.txt')

# X_train_times = np.loadtxt(r'D:\forecasting_study\maven_multistep_cnn_10_hour_input_9_features_x_train_times.txt',dtype='U')
# X_test_times = np.loadtxt(r'D:\forecasting_study\maven_multistep_cnn_10_hour_input_9_features_x_test_times.txt',dtype='U')
# y_train_times = np.loadtxt(r'D:\forecasting_study\maven_multistep_cnn_10_hour_input_9_features_y_train_times.txt',dtype='U')
# y_test_times = np.loadtxt(r'D:\forecasting_study\maven_multistep_cnn_10_hour_input_9_features_y_test_times.txt',dtype='U')
# y_train_reshaped = np.loadtxt(r'D:\forecasting_study\maven_multistep_cnn_10_hour_input_9_features_y_train.txt')
# X_train_reshaped = np.loadtxt(r'D:\forecasting_study\maven_multistep_cnn_10_hour_input_9_features_x_train.txt')
# X_test_reshaped = np.loadtxt(r'D:\forecasting_study\maven_multistep_cnn_10_hour_input_9_features_x_test.txt')

maven_yhat = maven_yhat_reshaped.reshape(maven_yhat_reshaped.shape[0], maven_yhat_reshaped.shape[1] // n_features, n_features)
y_test = y_test_reshaped.reshape(
    y_test_reshaped.shape[0], y_test_reshaped.shape[1] // n_features, n_features)
# y_train = y_train_reshaped.reshape(
#     y_train_reshaped.shape[0], y_train_reshaped.shape[1] // n_features, n_features)
# X_test = y_test_reshaped.reshape(
#     y_test_reshaped.shape[0], y_test_reshaped.shape[1] // n_features, n_features)
# X_train = y_train_reshaped.reshape(
#     y_train_reshaped.shape[0], y_train_reshaped.shape[1] // n_features, n_features)

print(y_test.shape,maven_yhat.shape)

maven_diff = y_test-maven_yhat
#print(maven_diff)

maven_mse = np.zeros((maven_diff.shape[1],maven_diff.shape[2]))
maven_percentage_error = np.zeros((maven_diff.shape[2]))

for n_features in range(maven_diff.shape[2]):
    maven_percentage_error[n_features] = np.mean(np.absolute(maven_diff[0:,0:,n_features]/maven_yhat[0:,0:,n_features]))*100
    for n_timesteps in range(maven_diff.shape[1]):
        maven_mse[n_timesteps][n_features] = np.sqrt(np.mean((maven_diff[0:,n_timesteps,n_features])*(maven_diff[0:,n_timesteps,n_features])))


#print(maven_mse)
# np.savetxt(r'D:\forecasting_study\maven_only_multistep_cnn_10_hour_input_9_features_spherical_mean_values.txt',mae)
# np.savetxt(r'D:\forecasting_study\maven_only_multistep_cnn_10_hour_input_9_features_spherical_standard_deviation_values.txt',std)

#
# mu = np.loadtxt(r'D:\forecasting_study\omni_multistep_cnn_6_hour_input_mean_values.txt')
# std = np.loadtxt(r'D:\forecasting_study\omni_multistep_cnn_6_hour_input_standard_deviation_values.txt')
# print(mu.shape)
# timelag = (np.arange(4)+1)*0.5
# # fig, axs = plt.subplots(3,2, tight_layout=True, sharex=True)
# #
# #
# # axs[0][0].errorbar(timelag,mu[0:,0],yerr=std[0:,1],label='B_x',c=cm.Greys(180),ls='none')
# # axs[0][0].scatter(timelag,mu[0:,0],color=cm.Greys(180))
# # axs[0][0].set_ylabel('B_x (nT)')
# # axs[1][0].errorbar(timelag,mu[0:,1],yerr=std[0:,2],label='B_y',c=cm.Greys(180),ls='none')
# # axs[1][0].scatter(timelag,mu[0:,1],color=cm.Greys(180))
# # axs[1][0].set_ylabel('B_y (nT)')
# # axs[2][0].errorbar(timelag,mu[0:,2],yerr=std[0:,3],label='B_z',c=cm.Greys(180),ls='none')
# # axs[2][0].scatter(timelag,mu[0:,2],color=cm.Greys(180))
# # axs[2][0].set_ylabel('B_z (nT)')
# #
# # axs[0][1].errorbar(timelag,mu[0:,3],yerr=std[0:,5],label='v_x',c=cm.Greys(180),ls='none')
# # axs[0][1].scatter(timelag,mu[0:,3],color=cm.Greys(180))
# # axs[0][1].set_ylabel('v_x (km/s)')
# # axs[1][1].errorbar(timelag,mu[0:,4],yerr=std[0:,6],label='v_y',c=cm.Greys(180),ls='none')
# # axs[1][1].scatter(timelag,mu[0:,4],color=cm.Greys(180))
# # axs[1][1].set_ylabel('v_y (km/s)')
# # axs[2][0].set_xlabel('Time since last measurement (hours)')
# # axs[2][1].errorbar(timelag,mu[0:,5],yerr=std[0:,7],label='v_z',c=cm.Greys(180),ls='none')
# # axs[2][1].scatter(timelag,mu[0:,5],color=cm.Greys(180))
# # axs[2][1].set_ylabel('v_z (km/s)')
# # axs[2][1].set_xlabel('Time since last measurement (hours)')
#
# fig, axs = plt.subplots(5,1, sharex=True, tight_layout=True)
#
#
# #axs[0].errorbar(timelag,mu[0:,0],yerr=std[0:,0],label='B_x',c=cm.plasma(0),ls='none',alpha=0.75)
# axs[0].scatter(timelag,maven_mse[0:,0],color=cm.plasma(0),alpha=0.99,marker='+')
# axs[0].set_ylabel('B (nT)')
# #axs[0].errorbar(timelag,mu[0:,1],yerr=std[0:,1],label='B_y',c=cm.plasma(125),ls='none',alpha=0.75)
# axs[0].scatter(timelag,maven_mse[0:,1],color=cm.plasma(125),alpha=0.99,marker='p')
# #axs[0].errorbar(timelag,mu[0:,2],yerr=std[0:,2],label='B_z',c=cm.plasma(250),ls='none',alpha=0.75)
# axs[0].scatter(timelag,maven_mse[0:,2],color=cm.plasma(250),alpha=0.99,marker='v')
# #axs[0].legend()
#
#
# #axs[1].errorbar(timelag,mu[0:,3],yerr=std[0:,3],label='v_x',c=cm.plasma(0),ls='none',alpha=0.75)
# axs[1].scatter(timelag,maven_mse[0:,3],color=cm.plasma(0),alpha=0.99,label='v_x',marker='+')
# axs[1].set_ylabel('v (km/s)')
# #axs[1].errorbar(timelag,mu[0:,4],yerr=std[0:,4],label='v_y',c=cm.plasma(125),ls='none',alpha=0.75)
# axs[1].scatter(timelag,maven_mse[0:,4],color=cm.plasma(125),alpha=0.99,label='v_y',marker='p')
#
# #axs[1].errorbar(timelag,mu[0:,5],yerr=std[0:,5],label='v_z',c=cm.plasma(250),ls='none',alpha=0.75)
# axs[1].scatter(timelag,maven_mse[0:,5],color=cm.plasma(250),alpha=0.99,label='v_z',marker='v')
# #axs[1].legend()
#
# #axs[2].errorbar(timelag,mu[0:,6],yerr=std[0:,6],label='v_z',c=cm.Greys(180),ls='none')
# axs[2].scatter(timelag,maven_mse[0:,6],color=cm.Greys(180))
# axs[2].set_ylabel('n_p (cm^-3)')
#
# axs[3].scatter(timelag,maven_mse[0:,7],color=cm.Greys(180))
# axs[3].set_ylabel('T_p (eV)')
#
# axs[4].scatter(timelag,maven_mse[0:,8],color=cm.Greys(180))
# axs[4].set_ylabel('P (nPa)')
#
# axs[4].set_xlabel('Time since last measurement (hours)')
# maven_mse = np.transpose(maven_mse)
# np.savetxt(r'D:\forecasting_study\maven_multistep_cnn_3_hour_input_before_2_hour_input_after_9_features_30_min_mse.txt',maven_mse)
# #axs[1].scatter
# #fig.suptitle('MAVEN forecasting model mean absolute error (MAE)')
# plt.show()
#
# fig, axs = plt.subplots(1, 2, tight_layout=True)
# axs[0].scatter([0,0],[0,0],color=cm.plasma(0),alpha=0.99,label='x component',marker='+')
# axs[0].scatter([0,0],[0,0],color=cm.plasma(125),alpha=0.99,label='y component',marker='p')
# axs[0].scatter([0,0],[0,0],color=cm.plasma(230),alpha=0.99,label='z component',marker='v')
# axs[0].legend()
#
# plt.show()
# # axs[0,0].hist(diff[:,0],bins=10,facecolor='grey',density=False,range=[-1,1])
# # axs[0,0].set_xlabel('Model error (nT)')
# # axs[0,0].set_ylabel('Frequency')
# # axs[0,0].text(-1,19000,'|B|')
# # axs[0,1].hist(diff[:,1],bins=10,facecolor='grey',density=False,range=[-1.5,1])
# # axs[0,1].set_xlabel('Model error (nT)')
# # axs[0,1].text(-1.5,16000,'B_x')
# # axs[1,0].hist(diff[:,2],bins=10,facecolor='grey',density=False,range=[-2,2])
# # axs[1,0].set_xlabel('Model error (nT)')
# # axs[1,0].set_ylabel('Frequency')
# # axs[1,0].text(-2,22000,'B_y')
# # axs[1,1].hist(diff[:,3],bins=10,facecolor='grey',density=False,range=[-2,1])
# # axs[1,1].set_xlabel('Model error (nT)')
# # axs[1,1].text(-2,22000,'B_z')
# # plt.show()
#
#
#
# # y_percentage_error = np.divide(abs(diff),abs(y_test))*100
# # #for i in range(y_percentage_error.shape[0]):
# # #    print(np.mean(y_percentage_error[:,i]))
# # y_percentage_error_sliced = y_percentage_error.copy()
# # y_percentage_error_sliced = np.delete(y_percentage_error_sliced,[1,2,3,5,6,7,10,11,12],axis=1)
# #
# # print(y_percentage_error_sliced.shape)
# # fig, (ax1) = plt.subplots(nrows=1, ncols=1)
# #
# # ax1.violinplot(y_percentage_error_sliced)
# # ax1.set_title('CNN forecasting accuracy (OMNI 1995-2020)')
# # ax1.set_ylabel('Percentage error')
# # plt.show()
#
# maven_only_mae_all_times = np.empty(maven_mse.shape[1])
#
# name_array = np.array(['B_x','B_y','B_z','v_x','v_y','v_z','n_p','T_p','P_sw'])
# for i in range(maven_only_mae_all_times.shape[0]):
#     maven_only_mae_all_times[i] = np.mean(maven_mse[0:,i])
#
# #fig, axs = plt.subplots(1,9,tight_layout=True)
#
# bar_colors = ['tab:grey','tab:grey','tab:grey','tab:grey','tab:grey','tab:grey','tab:grey','tab:grey','tab:grey']
# fig, axs = plt.subplots(tight_layout=True)
# axs.bar(name_array,maven_percentage_error,color=bar_colors,alpha=0.6)
# axs.set_xlabel('Parameter')
# axs.set_ylabel('MAPE')
# plt.show()

fig, axs = plt.subplots(3,3, tight_layout=True)


#axs[0].errorbar(timelag,mu[0:,0],yerr=std[0:,0],label='B_x',c=cm.plasma(0),ls='none',alpha=0.75)
axs[0][0].hist(np.absolute(maven_diff[0:,0:,0].reshape((maven_diff.shape[0]*maven_diff.shape[1]))),range=[0,20],bins=20,color=cm.Greys(140))
axs[0][0].set_xlabel('B_x error (nT)')
axs[0][0].set_ylabel('Frequency')

axs[0][1].hist(np.absolute(maven_diff[0:,0:,1].reshape((maven_diff.shape[0]*maven_diff.shape[1]))),range=[0,20],bins=20,color=cm.Greys(140))
axs[0][1].set_xlabel('B_y error (nT)')
axs[0][1].set_ylabel('Frequency')

axs[0][2].hist(np.absolute(maven_diff[0:,0:,2].reshape((maven_diff.shape[0]*maven_diff.shape[1]))),range=[0,20],bins=20,color=cm.Greys(140))
axs[0][2].set_xlabel('B_z error (nT)')
axs[0][2].set_ylabel('Frequency')

axs[1][0].hist(np.absolute(maven_diff[0:,0:,3].reshape((maven_diff.shape[0]*maven_diff.shape[1]))),range=[0,200],bins=20,color=cm.Greys(140))
axs[1][0].set_xlabel('v_x error (km/s)')
axs[1][0].set_ylabel('Frequency')

axs[1][1].hist(np.absolute(maven_diff[0:,0:,4].reshape((maven_diff.shape[0]*maven_diff.shape[1]))),range=[0,200],bins=20,color=cm.Greys(140))
axs[1][1].set_xlabel('v_y error (km/s)')
axs[1][1].set_ylabel('Frequency')

axs[1][2].hist(np.absolute(maven_diff[0:,0:,5].reshape((maven_diff.shape[0]*maven_diff.shape[1]))),range=[0,200],bins=20,color=cm.Greys(140))
axs[1][2].set_xlabel('v_z error (km/s)')
axs[1][2].set_ylabel('Frequency')

axs[2][0].hist(np.absolute(maven_diff[0:,0:,6].reshape((maven_diff.shape[0]*maven_diff.shape[1]))),range=[0,5],bins=10,color=cm.Greys(140))
axs[2][0].set_xlabel('n_p error (cm^-3)')
axs[2][0].set_ylabel('Frequency')

axs[2][1].hist(np.absolute(maven_diff[0:,0:,7].reshape((maven_diff.shape[0]*maven_diff.shape[1]))),range=[0,350],bins=35,color=cm.Greys(140))
axs[2][1].set_xlabel('T_p error (eV)')
axs[2][1].set_ylabel('Frequency')

axs[2][2].hist(np.absolute(maven_diff[0:,0:,8].reshape((maven_diff.shape[0]*maven_diff.shape[1]))),range=[0,2],bins=10,color=cm.Greys(140))
axs[2][2].set_xlabel('P_dyn error (nPa)')
axs[2][2].set_ylabel('Frequency')

plt.show()
