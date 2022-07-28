This code uses run_many.sh to run apprentice many times on a dataset. It will store a results folder in an experiments folder,
with graphs that compare the preformance of covariance matrix method of handling error with apprentice's older methods.
It can also generate mock target data and Monte Carlo runs for apprentice.

Basic Instructions:
How to reproduce the graphs of the 2_exp mock data (two exponential observables):
Set up your environment to run apprentice, then execute "bash run_many.sh" in this folder (examples/dummy_data).
Once the code has finished running, the most important graphs are stored in experiment/2_exp_linear(timestamp)/results/important_graphs

How to run a new mock data experiment:
Use the 2_exp.py file as a template, create your own .py file and fill in the needed information. Set experiment_name in run_many.sh to the name of your .py file, then execute bash run_many.sh

run_many.sh Bash Script Walkthrough:
This is the main driver script that will run an experiment automatically if the setup is correct. First, we create a new folder in /experiments to hold all our data and results.

Apprentice requires two sets of information to run a tune: the target data(Data folder), and the Monte Carlo runs(MC folder). These are the DATADIR and INPUT dir from this tutorial: https://iamholger.gitbook.io/apprentice/5-minute-tuning-tutorial

This code can either generate mock data using observable functions and other parameters from a preset file, or it can copy MC and Data folders from the same directory as run_many.sh. This behavior depends on the mock_data boolean. When generating mock data, mk_data.py generates many random points under an observable function under given ranges and bins them to make the Monte Carlo runs and target data. mk_data.py also takes an observable_error function, typically a percentage between 5 and 20%. It will change the height of each bin using a normal distribution with nominal height as mean and the error function times the height as std. After the MC data is collected into inputdata.h5, add_err changes the errors in h5 file to reflect the change that mk_data has been made. 

Regardless of the dataset's source, apprentice uses app-datadirtojson to combine Data into data.json, and app-yoda2h5 to combine the MC folder into inputdata.h5. We then use mc_envelope.py to make envelope graphs of the MC runs. Apprentice will probably fail if the target data does not fall mostly within the MC envelope.

![mc_envelope example](examples/dummy_data/experiments/2_exp_linear_07-28-2022_00:20:56/results/important_graphs/observable_envelopes/func0.pdf)
An example with the 2_exp mock data.

Now that our dataset is prepared, we will run many similar tunes on this data to evaluate the preformance of the covariance method of handling error versus two of apprentice's existing methods. Each loop, apprentice will calculate the covariance matrix and fit functions of the form given by --order to each indiviual value bin and error bin across observables. If the --sample option is used, it will sample that number of MC runs to fit with. Then, the fits are used to tune the target parameters, with each of the three methods. Every file generated in this process is in a numbered tune folder in /experiments/(experiment name and time)/tunes. 

After all of these tunes are completed, we can analyse how covariance preformed against the other methods. Here is an overiew of important results:

![chi_2 graph example](examples/dummy_data/experiments/2_exp_linear_07-28-2022_00:20:56/results/important_graphs/2_exp_every_offbound_chi2.pdf)
Over many tunes, we record the chi2/ndf that apprentice gets, and graph by method of error handling. We also throw out tunes where apprenteice hits the boundary parameters when tuning and gets stuck (OFFBOUND).

![boundary_contour example](examples/dummy_data/experiments/2_exp_linear_07-28-2022_00:20:56/results/important_graphs/boundary_contour.pdf)
For this example with two parameters, we can run a contour to find the area around a tune parameter result that is within a certain chi2 margin. There is also a elipse generated using the eigenvectors as axes; when the contour cannot be calculated, the ellipse will likely be a good approximation. Both scripts use the first tune in the tunes folder where none of the three methods resulted in OFFBOUND

![validation example](examples/dummy_data/experiments/2_exp_linear_07-28-2022_00:20:56/results/important_graphs/tune_validations/2_exp_obs0_tune_validation.pdf)
To make sure that apprentice has tuned well, we can plug the results of each tune into the surrogate functions, and graph the results with the target data.
