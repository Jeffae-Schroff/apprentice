import os
import shutil
if(os.path.isdir('many_tunes')):
    shutil.rmtree('many_tunes') 
os.mkdir('many_tunes')