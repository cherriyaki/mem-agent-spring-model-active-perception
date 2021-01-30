analysis="filo_lengths"
numberOfRuns=1
epsilon=0.9
vconcst=0.04
gradient=2
filconstnorm=2.0
filtipmax=15
tokenstrength=1
filspacing=2
actinmax=512 #cherry
randFilExtend=-1
randFilRetract=-1

# other_args=()
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    --filconstnorm)
    filconstnorm="$2"
    shift # past argument
    shift # past value
    ;;
    --filtipmax)
    filtipmax="$2"
    shift # past argument
    shift # past value
    ;;
    --filspacing)
    filspacing="$2"
    shift # past argument
    shift # past value
    ;;
    --actinmax) # cherry
    actinmax="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done

timestamp=$(date "+%Y.%m.%d-%H.%M.%S")
local_output_foldername="camp_output_analysis_"$analysis"_"$timestamp
camp_subfolder_name="APSingleCodebase/"$analysis"_"$timestamp
mkdir $local_output_foldername
camp_home="/camp/lab/bentleyk/home/shared/limc" #cherry
rsync -r --rsh="sshpass -p cmlss888 ssh -l limc" --include='*.'{sh,cpp,h,py,npy,pyc} --include="makefile" --include="requirements" --exclude="*" --delete-excluded ./ login.camp.thecrick.org:"$camp_home"/"$camp_subfolder_name"/

sshpass -p 'cmlss888' ssh limc@login.camp.thecrick.org ""