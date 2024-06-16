# Backup Database Using AirFlow
### Backup Recent 2 Backups of a Database Using Airflow Scheduling
This README explains how to implement an Airflow scheduling task to manage the backup of your database.

Steps to Implement
1. Check Free Space in Disk
First, we need to ensure there is enough free space available on the disk to store the database backup.

2. Check Size of the Database to Be Dumped
Next, we determine the size of the database that needs to be backed up.

3. Compare Free Disk Space with Database Size
We then compare the available free space on the disk with the size of the database.

- If freeSizeOfDisk > sizeOfDb:
     - Proceed with the database dump.
     - and on success send email.
- Else:
    Send an alert to the administrator.
    Halt the backup process.

![plot](./assets/graph.png)
![plot](./assets/email.png)

