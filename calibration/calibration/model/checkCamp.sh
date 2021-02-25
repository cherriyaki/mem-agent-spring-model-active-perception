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
camp_server="$user@login.camp.thecrick.org"


#-- Check job status
status=$(ssh $camp_server "cd $camp_root; sacct --format=User,JobID,Jobname,state,time,start,end,elapsed")
echo $?