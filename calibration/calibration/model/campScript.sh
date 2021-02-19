
#-- Default variables
user=$USER

#-- Set variables from args
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    --user) 
    user="$2"
    shift # past argument
    shift # past value
    ;;
    --id)
    id="$2"
    shift # past argument
    shift # past value
    ;;
    --analysis)
    analysis="$2"
    shift # past argument
    shift # past value
    ;;
    --email)
    email="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done

#-- Paths
camp_home="/camp/lab/bentleyk/home/shared/$user"
session_dir="APSingleCodebase/session_$id"
calibration_dir="calibration"
slurm_out_camp="$camp_home/$session_dir/$calibration_dir/output/slurm"
log_file="$camp_home/$session_dir/$calibration_dir/logs/log_$id.log"

#-- For debugging
echo "
user $user, id $id, analysis $analysis, email $email
camp home $camp_home, session dir $session_dir, calibration dir $calibration_dir, slurm out $slurm_out_camp
"

#-- Error handling function
# Thanks to https://stackoverflow.com/a/50265513 for this code
exit_if_error() {
  local exit_code=$1
  shift
  [[ $exit_code ]] &&               # do nothing if no error code passed
    ((exit_code != 0)) && {         # do nothing if error code is 0
      printf 'ERROR: %s\n' "$@" > $log_file  # save to log
      exit "$exit_code"             
    }
}

# TODO add file extensions
rsync -r --include='*.'{sh,cpp,h,py,npy,pyc,log,out,err,csv} --include="makefile" --include="requirements" --exclude="*" --delete-excluded ./ $user@login.camp.thecrick.org:$camp_home/$session_dir/ \
|| exit_if_error $? "rsync failed: Failed to move files to CAMP"

# TODO add pip installs
ssh $user@login.camp.thecrick.org \
"
cd $camp_home/APSingleCodebase;
ml Python/3.8.2-GCCcore-9.3.0;
python3 -m venv env;
source env/bin/activate;
pip install numpy scipy pymoo;
cd ../$session_dir;
./buildSpringAgent.sh --analysis $analysis;
sbatch --job-name=calibration_$id \\
--output=$slurm_out_camp/out/slurm_$id.out \\
--error=$slurm_out_camp/err/slurm_$id.err \\
--mail-type=END,FAIL \\
--mail-user=$email \\
--exclusive \\
PYTHONPATH=calibration python3 -m calibration.model.calibrate $id;
exit;
" \
|| exit_if_error $? "ssh failed: Failed to ssh into CAMP"

# sbatch $calibration_dir/$calib_model_dir/calibrateScript.sh --id $id --email $email;
