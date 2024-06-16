
source /Users/sagarpoudel/airflow/bash_scripts/credentials.sh

CURRENT_DATETIME=$(date +"%Y%m%d_%H%M%S")

DUMP_FILE="$DUMP_DIR/${DB_NAME}_${CURRENT_DATETIME}.sql"
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME > "$DUMP_FILE"

if [ $? -eq 0 ]; then
        export dumpStatus=true
        export dumpMsg="Database successfully dumped to $DUMP_FILE"
else    
        export dumpStatus=false
        export dumpMsg="Failed to dump the database"
fi

echo $dumpStatus
echo $dumpMsg
