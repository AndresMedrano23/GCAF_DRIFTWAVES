Here you will find all the codes needed for runing GCAF on a cluster, 
if running local you will have to avoid the queues.

The MANDATORY files for running are:
    field.cpp -> Here is the numerical calculation of the fields including the electrict potential
    functions.cpp -> Here are the special functions not included in any package, 
                like distributions and random seeds generators.
    initial.cpp -> Here is where the inital conditions are set for each type of simualtion.
    read.cpp-> Read all the inputs of the data in and assign them to the actual code. Basicly the translator.
    record.cpp-> Saves all the numerical data in .dat files for each type of simulation
                If you want to add more information or avoid some, here you can control that.
    step.cpp-> Here there are the set of  GC equations and also the RK4 integrator.
    collisions.cpp-> Simulates collisions between particles. 
    main.cpp -> The main loop which calls all the programs acording to type of simulation.
    Makefile-> Create the executable gcafpp
        data.in-> Where you can control the type of simulation, the type of device and dimensions.
    err.log and out.log -> where you find your logs.
    define.h-> Here we define all the type of variables needed.
    shared.h-> The bounds, constants and common names that will be shared globally.
    gcafpp.slurm-> The slurm file to queue in a cluster (also useful to see how to run it locally)


The extra files (Shell), not needed for running but useful for automated sweep runs.
    Data_Generator.sh-> Will create everything needed for queue a sweep.
                        It will create all the data.in files for each initial conditions.
                        It will create folder named after the initial conditions.
                        It will create slurm files for submitting the jobs.
    Job_Sender-> It will send all the slurm files to the desired queue.
    queue_change-> To change all the pending files to another queue.
