
#-- Default variables
user=$USER

#-- Set variables from args
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    --id)
    id="$2"
    shift # past argument
    shift # past value
    ;;
    --user)
    user="$2"
    shift # past argument
    shift # past value
    ;;
    --email)
    email="$2"
    shift # past argument
    shift # past value
    ;;
    --analysis)
    analysis="$2"
    shift # past argument
    shift # past value
    ;;
esac
done

#-- Paths
THIS_FILE=$(basename "${BASH_SOURCE[0]}")
ROOT=$(cd $(dirname "${BASH_SOURCE[0]}")/../../.. && pwd)     # Thanks to https://codefather.tech/blog/bash-get-script-directory/ for this line of code
log_file="$ROOT/calibration/logs/log_$id.log"
result_file="$ROOT/calibration/output/calibrationResults/result_$id.res"

camp_home="/camp/lab/bentleyk/home/shared/$user"
session_dir="APSingleCodebase/session_$id"
slurm_out_camp="\/camp\/lab\/bentleyk\/home\/shared\/$user\/APSingleCodebase\/session_$id\/calibration\/output\/slurm"
# slurm_out_camp="/camp/lab/bentleyk/home/shared/$user/APSingleCodebase/session_$id/calibration/output/slurm"

#-- For debugging
# echo "
# user $user, id $id, analysis $analysis, email $email
# agent $ROOT, this $THIS_FILE, camp home $camp_home, session dir $session_dir, slurm out $slurm_out_camp, log $log_file,  result $result_file
# "

#-- Functions
#- Log function:
# Arguments: $1 - type, $2 - line number, $3 - message
write_log() {
  local log_type=$1
  local line=$2
  shift; shift;
  local message=$(printf '%s' "$@")
  PYTHONPATH=$ROOT/calibration python3 -m calibration.model.logWriter --id $id --line $log_type $THIS_FILE $line "$message"
}

#- Error handling function
# Adapted from https://stackoverflow.com/a/50265513
exit_if_error() {
  local exit_code=$1
  local line=$2
  local trace=$3
  shift; shift; shift;
  if [ $exit_code != 0 ]
  then
    write_log "ERROR" $line "$(printf '%s' "$@")"  # save to log
    PYTHONPATH=$ROOT/calibration python3 -m calibration.model.logWriter --id $id --exc "$trace"
    exit "$exit_code"     
            # TODO NEW how to handle this exit status in the python viewcontroller?
  fi
}

#-- Create files
touch $log_file
write_log "INFO" $LINENO "Session $id started. Input file: calibration/data/inputHistory/input_$id.json"
touch $result_file
write_log "INFO" $LINENO "Result file created: calibration/output/calibrationResults/result_$id.res"

#-- Main activity
cd $ROOT
# TODO NEW add file extensions
trace=$(rsync -r \
--include='calibration/' --include='calibration/*/' --include='calibration/**/' --include='calibration/***/' --include='calibration/****/' \
--include='*.'{sh,cpp,h,py,npy,pyc,log,out,err,csv,json,res} \
--include="makefile" --include="requirements" --exclude="*" --delete-excluded ./ \
$user@login.camp.thecrick.org:$camp_home/$session_dir/ 2>&1) \
|| exit_if_error $? $LINENO "$trace" "rsync: Failed to move files to CAMP" 
write_log "DEBUG" $LINENO "Finished rsync files to CAMP"

slurmcmd=$(echo "PYTHONPATH=calibration python3 -m calibration.model.calibrate ID" \
| sed -e 's/ID/'$id'/g' -e 's/OUTDIR/'$slurm_out_camp'/g' -e 's/EMAIL/'$email'/g')

# TODO NEW test ssh part
# TODO NEW add pip installs
trace=$(ssh $user@login.camp.thecrick.org \
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
--wrap=$slurmcmd
# PYTHONPATH=calibration python3 -m calibration.model.calibrate $id;
# slurm_calibrate_$id.sh;
exit;
" 2>&1)  \
|| exit_if_error $? $LINENO "$trace" "ssh: Failed to run commands on CAMP" 
write_log "DEBUG" $LINENO "Finished ssh to CAMP"

