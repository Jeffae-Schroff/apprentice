#saves the data in many_tunes, the values used to create it, and the current commands in bash script run_many used to generate it
#also saves inputdata.h5 generated from the MC folder now
#takes the name of a folder to store them in (as subfolder of results folder)


import os
import sys
import shutil



if len(sys.argv) != 2:
    print('invalid arguments to save_results.py')

save_folder = 'results/'+sys.argv[1]
print("saving all tuning data to " + save_folder)
if(os.path.isdir(save_folder)):
    shutil.rmtree(save_folder) 
shutil.copytree("many_tunes", save_folder)
shutil.copy("run_many.sh", save_folder+"/run_many.sh")
shutil.copy("inputdata.h5", save_folder+"/inputdata.h5")


