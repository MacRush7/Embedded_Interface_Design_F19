# EID Project-1
# Authors: Rushi James Macwan, Poorn Mehta 
#
# MySQL Database - Python Script
#
# @Brief: This script has been written to interface the MySQL database with the python-based
# project that has been designed for Project-1. Using this test script, the main script will
# be designed that will connect to the MySQL pre-established server and create tables and
# delete them after it is used in one complete execution cycle of the main python script. This
# is done to ensure that redundant tables in the DB are not left out which can lead the script
# execution to crash unexpectedly.


# This is MySQL database script has been created with the help of many online resources. All of the
# online resources that were used to create this script have been duly credited below:


# Reference: http://www.mikusa.com/python-mysql-docs/introduction.html
# Reference: https://pythonspot.com/mysql-with-python/
# Reference: https://stackoverflow.com/questions/155054/mysql-timestamp-column
# Reference: https://stackoverflow.com/questions/15271907/python-mysql-update-working-but-not-updating-table
# Reference: https://www.a2hosting.com/kb/developer-corner/mysql/managing-mysql-databases-and-users-from-the-command-line


# INSTRUCTIONS TO RUN THIS SCRIPT:
#
# Prior to running this script, a MySQL server has to be established. Please, follow the
# below steps to create the required MySQL server on which tables can be created/deleted
# by this script.
#
# COMMANDS TO BE RUN FROM THE CLI:
#
# $ sudo mysql -u root -p
#
# ENTER YOUR ROOT PASSWORD
#
# > CREATE DATABASE mydb;
# > \q
#
# Once the above commands are run, the MySQL server is established and then this python script can be successfully executed.


#!/usr/bin/python

import MySQLdb

# Connecting to the established MySQL server

db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="mydb")

# Setting up an auto-commit feature that allows this script to commit table entries to the MySQL DB server

db.autocommit(True)

# Setting up the remote execution cursor for peforming operations under the connected DB

cur = db.cursor()

# Creating the DB table

cur.execute("CREATE TABLE eid (Readings INT UNSIGNED NOT NULL AUTO_INCREMENT, Temperature FLOAT, Humidity FLOAT, PRIMARY KEY (Readings))")

# Setting up the time-stamp feature

cur.execute("ALTER TABLE `eid` ADD `Updated` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP")


################################

# TEST VALUES (TO BE INTEGRATED)

tmp = 12.98
hmd = 21.55

for x in range(1, 35):
    tmp += 1
    hmd += 1
    cur.execute("INSERT INTO eid (Temperature, Humidity) VALUES (%s, %s)", (tmp, hmd))

################################

# Fetching recent 30 values from the DB table

cur.execute("SELECT * FROM eid WHERE Readings <= '30'")

# Displaying the acquired 30 values on the CL

for row in cur.fetchall() :
    print "Readings:\t\t", row[0], "\n", "Temperature:\t\t", row[1], "C", "\n", "Humidity:\t\t", row[2], "%", "\n", "Updated:\t\t", row[3], "\n\n\n\n"
    
# Deleting the table for consistency when the execution loop consisting of 30 iterations is re-run
    
cur.execute("DROP TABLE eid")

