import os
import scipy
from scipy import io
from scipy.io import readsav
from pydl.goddard.astro import airtovac, vactoair
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

wav_sol_vacuum=io.readsav('w_l61.dat')
wav_sol_air=vactoair(wav_sol_vacuum['w'])

#data from IDL file
data = scipy.io.readsav('rl61.9142')

#sp, represents variable in dataset
sp_data = data['sp']

#putting the plots in a folder
folder_path = '9142.fit'
os.makedirs(folder_path, exist_ok=True)

# define the function for curve fitting
def poly_func(x, *coefficients):
    return np.polyval(coefficients, x)

#loop orders
for i in range (3): #(np.shape(wav_sol_air)[0]):
    fig, ax = plt.subplots(figsize=(10,6))
    
    #apply offset to get x-values
    shifted_x = wav_sol_air[i,:]   
    #get the y data
    y_data = sp_data[i,:]
    
    #set axis limits
    x_min = np.min(shifted_x)
    x_max = np.max(shifted_x)
    y_min = np.min(sp_data[i,:])
    y_max = np.max(sp_data[i,:])
    ax.set_xlim(x_min, x_max)
    
    #offset using median of y_data
    polynomial_degree = 5
    initial_guess = np.ones(polynomial_degree)
    popt, pcov = curve_fit(poly_func, shifted_x, y_data-np.median(y_data), p0=initial_guess, maxfev=2000)

    # Evaluate the fitted values at shifted_x
    fitted_curve = poly_func(shifted_x, *popt)

    print(shifted_x.shape, y_data.shape)
    
    # Plot
    #ax.plot(shifted_x, y_data, label='Original Data')
    #ax.plot(shifted_x, fitted_curve+np.median(y_data), 'r-', label='Fitted Curve')
    
  
    #divide original data by fitted curve
    ratio = y_data / fitted_curve
    ax.plot(shifted_x, ratio, 'g--', label='Ratio (Data / Fitted Curve)')
    plt.show()
    
    #save filename for changing order
    filename = 'fit.Order_{}.png'.format(i)
    
    #titling plot
    plt.title('rl61.9142 - 1695294922548180224'+ ' ' + filename)
    
    #formatting
    plt.xlabel('Wavelength (Angstrom)', fontsize = 14)  # X-axis label
    plt.ylabel('Counts', fontsize = 14)  # Y-axis label
    ax.minorticks_on() #turns on minor ticks
    ax.tick_params(axis='both', which='major', labelsize=12,direction="in",bottom=True, top=True, left=True,length=7,width=0.9)
    ax.tick_params(axis='both', which='minor', labelsize=12,direction="in",bottom=True, top=True, left=True,length=4,width=0.7)
    
    if i == 32:
        #custom y limit for problematic order
        ax.set_ylim(ymin=0, ymax=upper_percentile + 3 * std_dev)
    elif i == 40:
        #custom y limit for problematic order
        ax.set_ylim(ymin=20, ymax=upper_percentile + 2 * std_dev)
    elif i == 45:
        #custom y limit for problematic order
        ax.set_ylim(ymin=0, ymax=upper_percentile + 2 * std_dev)
    elif i == 50:
        #custom y limit for problematic order
        ax.set_ylim(ymin=0, ymax=upper_percentile + 3 * std_dev)
    else:
        lower_percentile = np.nanpercentile(sp_data[i,:], 5)  # 5th percentile
        upper_percentile = np.nanpercentile(sp_data[i,:], 95)  # 95th percentile
        std_dev = np.nanstd(sp_data[i,:])
        ax.set_ylim(ymin=lower_percentile - 2 * std_dev,ymax=upper_percentile + 3 * std_dev)
       
    plt.grid(True)  # this adds grid lines  
   
    plt.savefig(folder_path + '/' + filename, dpi=300, bbox_inches='tight', facecolor='w') #saving to folder
    
    plt.close(fig)

    
    #bin data, smooth it, then fit function
    #spline?
