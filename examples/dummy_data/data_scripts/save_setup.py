#saves files used to set up experiment

import shutil
import argparse
parser = argparse.ArgumentParser()

# mandatory arguments
parser.add_argument("runMany", help="path of file to save", type=str)
parser.add_argument("experimentSetValues", help="path of file to save", type=str)


args = parser.parse_args()

shutil.copy(args.runMany, "setup/run_many.sh")
shutil.copy(args.experimentSetValues, "setup/" + args.experimentSetValues.split('/')[-1] + ".py")


