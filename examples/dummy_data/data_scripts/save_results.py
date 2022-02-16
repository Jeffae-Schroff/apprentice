import os
import sys
import shutil
#saves the data in many_tunes, the values used to create it, and the bash script used to generate it
#takes the name of a folder to store them in (as subfolder of results folder)


if len(sys.argv) != 2:
    print('invalid arguments to save_results.py')

save_folder = 'results/'+sys.argv[1]
print("saving all tuning data to " + save_folder)
if(os.path.isdir(save_folder)):
    shutil.rmtree(save_folder) 
shutil.copytree("many_tunes", save_folder)
shutil.copy("data_scripts/set_experiment_values.py", save_folder+"/set_experiment_values.py")
shutil.copy("run_many.sh", save_folder+"/run_many.sh")

