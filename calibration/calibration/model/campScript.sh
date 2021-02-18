#-- VARIABLES
timestamp=$(date "+%Y.%m.%d-%H.%M")
user=$USER
# analysis
# email
# get arg user
# json id
#-- PATHS
camp_home="/camp/lab/bentleyk/home/shared/$user"
session_dir="APSingleCodebase/session_"$timestamp
calibration_dir="/calibration/calibration"
calib_model_dir="model"

# scp all other files to camp
# TODO add file extensions
rsync -r --include='*.'{sh,cpp,h,py,npy,pyc} --include="makefile" --include="requirements" --exclude="*" --delete-excluded ./ login.camp.thecrick.org:"$camp_home"/"$session_dir"/;

# ssh to camp these commnds:
# TODO add pip installs
ssh $user@login.camp.thecrick.org "
cd $camp_home/APSingleCodebase;
ml Python/3.8.2-GCCcore-9.3.0;
python3 -m venv env;
source env/bin/activate;
pip install numpy scipy pymoo;
cd ../$session_dir;
./buildSpringAgent.sh --analysis $analysis;
sbatch $calibration_dir/$calib_model_dir/calibrateScript.sh --time $timestamp --email $email;
exit;
"
# run calibration package  with id as arg
