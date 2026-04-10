In the Miscellaneous code section you will find mainly a bunch of codes used for graph all the data obtained by GCAF
Also you will find some shell files that help you graph in bulk.

GRAPHS:
    STATISTICAL MOMENTS AND DISTRIBUTIONS: When using the ensemble configuration you will need to visualize
                                          the spatial distributions and whatch how they evolve.
            moments_plot2.py -> Allows you to plot the evolution of : The variance (<deltar^2>), the skewness and the kurtosis making some fits.
            Ancho_plot.py-> Shows only the evolution of the variance and a linear fit.
            distribution_plot2.py-> Allows you to graph the histrograms (i.e the distributions) and a gaussian fit to the radial, poloidal and toroidal position
            Dist_Auto_Auto.sh -> Search in all the folders inside a folder the files name mome.plt and dist1-25.plt in order to graph and save the images.
    TRAJECTORY: When using the trajectory mode, we will need to plot the trajectory follow by a single particle.
            trajectory_plot-> Allows to graph a 3D trajectory or a poloidal cut from the traj.plt
            Auto_Traj.sh-> Sweep for all the files inside a specific folder generating the specific type of graphs.


DIAGNOSIS:
    Slope_Data -> When Analyzing possible configurations of chaos (In the ensemble configuration ) we want to look if a linear fit fits the evolution of the variance             over time, this programm returns a CSV file with all the slopes, R^2 and final time of simulation for all the mome.plt files inside a folder.


