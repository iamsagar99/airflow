
source /Users/sagarpoudel/airflow/bash_scripts/credentials.sh

directory=$DUMP_DIR

cd "$directory" || exit

#sort files wrt time ie. newest first
files=($(ls -p -t | grep -v /))

#length of files
num_files=${#files[@]}

if [ "$num_files" -gt 2 ]; then
    for (( i=2; i<num_files; i++ )); do
        rm "${files[$i]}"
    done

    export deleteStatus=true
    export deleteMsg="Delete complete."
else
    export deleteStatus=false
    export deleteMsg="File length < 2. Nothing deleted."
fi

echo $deleteStatus
echo $deleteMsg
