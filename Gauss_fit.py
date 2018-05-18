import sys
import optparse
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

def main():
    '''
    Reads .csv file, fits Gauss distribution to it (optional subtraction of background), displays two graphs in one figure and saves the figure.
    The first graph is the whole energetic spectrum with removed noise channels and the second one is close up view to peak with Gauss fit.
    Takes one parameter - name of the .csv file with energy spetrum
    Set of variables (noise, X1, X2, background, figname, title) should be stated
    '''
    noise = 0 # Number of channels that are considered to be noise
    X1 = 300 # The beginning of Gauss distribution fit
    X2 = 400 # The end of Gauss distribution fit
    background = True # if True - the background is subtracted from peak \\ if False the background is not subtracted from peak
    y_scale = 'linear' # 'linear' or 'log'
    figname = "241Am.png" # The name of figure
    title = "241Am" # Title of the figure

    # Parse the .csv file
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', dest='file', help='File name')
    (options, args) = parser.parse_args()

    # Read data from .csv file and save it to variable 'data'
    data = read_csv(options.file)

    # Remove the first X channels - noise
    data = data[noise:, :]

    # Fit Gauss distribution to data - from X1 to X2
    popt, xx, peak = fit_gauss(data, X1, X2, background)

    # Create fine vector of numbers from X1 to X2
    x = np.linspace(X1, X2, 200)

    # Plot data
    plot_data(data, figname, title, popt, x, xx, peak, y_scale)

    # Shows figure
    plt.show()

def Gauss(x, amp, cen, wid):
    # Fits Gauss distribution
    return (amp/(np.sqrt(2*np.pi)*wid)) * np.exp(-(x-cen)**2 /(2*wid**2))

def read_csv(fileName):
    # Reads the .csv file and returns data as an output
    output = np.loadtxt(fileName, delimiter=',', skiprows=0)
    return output

def fit_gauss(data, X1, X2, cut):
    # Fits data (from X1 to X2) by Gauss distribution
    start = X1
    finish = X2
    xx = np.linspace(start, finish, finish - start + 1)
    xx = xx[:-1]
    x = data[:, 0]
    y = data[:, 1]
    shift = x[0]
    X1 = int(X1 - shift)
    X2 = int(X2 - shift)
    # Inicializacni odhady pro fitovani Gaussem
    amp = max(y[X1:X2])
    cen  = shift + X1 + (X2 - X1) / 2
    wid = (X2 - X1) / 4
    if (cut == True):
        delta_x = X2 - X1
        delta_y = y[X2] - y[X1]
        a = delta_y / delta_x
        b = y[X1]
        spread = np.linspace(0, X2 - X1, X2 - X1 + 1)
        spread = spread[:-1]
        background = a * spread + b
    else:
        background = 0
    peak = y[X1:X2] - background
    # Fitovani Gaussem
    popt, pcov = curve_fit(Gauss, xx, peak, p0 = [amp,cen,wid]) # fitovani Gaussem
    return popt, xx, peak

def plot_data(data, figname, title, popt, x, xx, peak, scale):
    # Plots the data including Gauss distribution
    # Creates figure
    fig = plt.figure(figsize=(18,9))
    # Creates the first subplot
    plt.suptitle(title, fontsize=16)
    ax1 = fig.add_subplot(1,2,1)
    ax1.plot(data[:, 0], data[:, 1], 'b+')
    ax1.set_xlabel("Channel [-]")
    ax1.set_ylabel("N [-]")
    ax1.set_yscale(scale)
    # Creates the second subplot
    ax2 = fig.add_subplot(1,2,2)
    ax2.plot(xx, peak, 'b+' ,label='data')
    ax2.plot(x, Gauss(x, *popt), 'r-', color='red', label = popt)
    ax2.set_xlabel("Channel [-]")
    ax2.set_ylabel("N [-]")
    ax2.legend(loc='upper right')
    # Saves the figure
    plt.savefig(figname)

if __name__ == "__main__":
    sys.exit(main())
