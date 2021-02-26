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
esac
done

#-- Paths
camp_root="/camp/lab/bentleyk/home/shared/$user/APSingleCodebase/session_$id"
ROOT=$(cd $(dirname "${BASH_SOURCE[0]}")/../../.. && pwd)     # Thanks to https://codefather.tech/blog/bash-get-script-directory/ for this line of code
# session_dir="session_$id"

result="calibration/output/calibrationResults/result_$id.res"
result_camp="$camp_root/$result"
result_local="$ROOT/$result"

log="calibration/logs/log_$id.log"
log_camp="$camp_root/$log"
log_local="$ROOT/$log"

slurmerr="calibration/output/slurm/err/slurm_$id.err"
slurmerr_camp="$camp_root/$slurmerr"
slurmerr_local="$ROOT/$slurmerr"


#-- Copy files from remote to local
camp_server="$user@login.camp.thecrick.org"

# Result
scp $camp_server:$result_camp $result_local
# Log
scp $camp_server:$log_camp $log_local
# Slurmerr
scp $camp_server:$slurmerr_camp $slurmerr_local
chmod +r $slurmerr_local
