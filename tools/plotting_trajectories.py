import numpy as np
import matplotlib.pyplot as plt

"""
DESCRIPTION
    Set of functions for fast-generation of plots from MD trajectories analysis.
    
    All functions are developed taking in mind the structure of RCBS.py (https://github.com/dynamicsUAB/RCBS.py) 
        output structure (simply arrays containing the data enclosed in dictionaries, but the input is the array)


FUNCTIONS
    - render_with_latex:    enables Matplotlib's renderisation using LaTeX.
    - simple_plot:          plots a single plot containing the plots of all the given arrays. It has also an option 
                            for generating a histogram with the data.
"""



def render_with_latex():
    plt.style.use('ggplot')
    from matplotlib import rc
    rc('font',**{'family':'serif','serif':['Computer Modern']})
    rc('text', usetex=True)


def simple_plot(
    lists,
    labels,
    invert_order=   False,  
        # [bool] Invert the order of plotting of the input arrays (useful to brind the first array to the front)
    histogram=      False,  
        # [bool] Plot the values as a histogram
    #subplots=       False,  
        # [bool] If false, plot all input arrays in a plot. If True, plot a subplot for each array.
    axis=           None,   # ["y title", "x title"]
        # [None|2-dim list of str] Define titles for axis
    xticks=         'rel',  
        # [pseudo-bool: False, absolute, relative] Convert ticks on X axis to nanoseconds
        # rel|relative: from 0 to n ns, abs|absolute (! not implemented yet): from rounded strt to rounded end
    one_ns=         10000,  
        # [int] Number of frames per ns of trajectory
    strt=           0,      
        # [int] First frame for plotting
    end=            None,   
        # [int|None] Last frame for plotting 
    bins_factor=    1,      
        # [int] One bin per Angstrom by default
    savefig=        False,  
        # [pseudo-bool] False for not saving, filename for saving as a png with a DPI of 300
):

    if savefig != False and isinstance(savefig, str):
        if savefig.find('/') != -1:
            folder  = savefig.split('/')[0]
            savefig = savefig.split('/')[1]
        
        else :
            folder = False
    
    elif savefig == False:
        pass

    else :
        print('Specify a saving filename.')
        return


    if end == None:
        end = len(lists[0]) + 1

    one_ns = round(len(lists[0][strt:end])/one_ns)

    if invert_order == True:
        lists  = lists[::-1]
        labels = labels[::-1]

    for l in range(len(lists)):
        if labels != None:
            plt.plot(range(len(lists[l][strt:end])), lists[l][strt:end], label=labels[l])
        elif labels == None:
            plt.plot(range(len(lists[l][strt:end])), lists[l][strt:end])

    if xticks.lower() in ('rel', 'relative'):
        plt.xticks(list(range(0, len(lists[0][strt:end])+1, one_ns*1000)), list(range(0, one_ns*100+1, one_ns*10)))
    
    #elif xticks.lower() in ('absolute', 'absolute'):   
        #plt.xticks(list(range(0, len(lists[0][strt:end])+1, one_ns*1000)), list(range(0, one_ns*100+1, one_ns*10)))

    else :
        pass

    plt.ylim([
        round(min([i for j in lists for i in j[strt:end]]) - 0.55),
        round(max([i for j in lists for i in j[strt:end]]) + 0.55),
        ])

    # calculating y ticks step, it is a tenth of the order of magnitude of max value rounded to oom-1
    om_y = round(np.log10(round(max([i for j in lists for i in j[strt:end]]) + 0.55)))
    ticks_y = 10**(om_y-1)
    plt.yticks(range(
        round(min([i for j in lists for i in j[strt:end]]) - 0.5),
        round(max([i for j in lists for i in j[strt:end]]) + 0.55)+1, 
        ticks_y
        ))

    if axis != None:
        plt.ylabel(axis[0])
        plt.xlabel(axis[1])

    if labels != None:
        plt.legend(bbox_to_anchor=(1, 1.01), loc="upper left")

    if savefig != False:
        if folder != False:
            plt.savefig(folder + '/plot_' + savefig + '.png', dpi=300, bbox_inches = "tight")

        elif folder == False:
            plt.savefig('plot_' + savefig + '.png', dpi=300, bbox_inches = "tight")

    plt.show()
    plt.close()


    if histogram == True:

        lists_for_hists = []
        for l in range(len(lists)):
            lists_for_hists.append(lists[l][strt:end])

        bins = round(max([i for j in lists for i in j[strt:end]]) + 0.55) - round(min([i for j in lists for i in j[strt:end]]) - 0.5)*bins_factor
                
        plt.hist(lists_for_hists, label=labels, bins=bins)

        plt.xlim([
            round(min([i for j in lists for i in j[strt:end]]) - 0.5),
            round(max([i for j in lists for i in j[strt:end]]) + 0.55),
            ])
        plt.ylim([0, end-strt])


        # calculating y ticks step, it is scalar*tenth of the order of magnitude of max value rounded to oom-1
        om_y = round(np.log10(end-strt))
        ticks_y = int(round((end-strt)/10**om_y, 1)*10**(om_y-1))
        plt.yticks(range(0, end-strt+1, ticks_y))

        # calculating x ticks step, it is a tenth of the order of magnitude of max value rounded to oom-1
        om_x = round(np.log10(round(max([i for j in lists for i in j[strt:end]]) + 0.55)))
        ticks_x = 10**(om_x-1)
        plt.xticks(range(
            round(min([i for j in lists for i in j[strt:end]]) - 0.5),
            round(max([i for j in lists for i in j[strt:end]]) + 0.55)+1, 
            ticks_x
            ))

        if axis != None:
            plt.ylabel("Number of occurences")
            plt.xlabel(axis[0])

        if labels != None:
            plt.legend(bbox_to_anchor=(1, 1.01), loc="upper left")

        if savefig != False:
            if folder != False:
                plt.savefig(folder + '/hist_' + savefig + '.png', dpi=300, bbox_inches = "tight")

            elif folder == False:
                plt.savefig('hist_' + savefig + '.png', dpi=300, bbox_inches = "tight")

        plt.show()
        plt.close()

        
