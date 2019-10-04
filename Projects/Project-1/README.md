# ECEN 5783 EID PROJECT-1 (Fall-2019)

**Project Collaborators/Developers:**

1. **Rushi James Macwan**
2. **Poorn Mehta**

# Repository Overview

This repository is fully owned by **Rushi James Macwan** and **Poorn Mehta**. All content on this repository is solely the work of **Rushi James Macwan** and **Poorn Mehta**. However, all external support and guidance taken in completing the work available on this repository has been clearly cited and credited wherever necessary as per the course guidelines.

For references, please visit the References.pdf file available in the main directory which contains an exhaustive list of all the external resources that were utilized and resourceful in completing this project.

# Installation Instructions

This project involves the use of the following elements:

1.	Raspberry Pi 3B setup
2.	DHT22 sensor library installation
3.	Python development libraries including MatPlotLib
4.	Qt and PyQt Installation
5.	MySQL Database Setup

The explanation below dives deep into setting up the Raspberry Pi 3B to run each of the above elements in a gradual manner. Please, go through the below points for a detailed explanation:

**Raspberry Pi 3B setup – installation of Raspbian Buster OS & VNC:**

•	The first step to begin with this project is to install the Raspbian Buster OS on the Raspberry Pi 3B. To do so, we must first download the “Raspbian Buster with desktop and recommended software” OS zipped image file on the host machine (e.g. a dedicated Windows/Mac computer). Link for downloading: https://www.raspberrypi.org/downloads/raspbian/

•	The second step is to unzip the file and use a software that can flash the image file to an SD card (that is already formatted). The software required to do this task is available here: https://www.balena.io/etcher/ 

•	The third step is to download the “balenaEtcher” software, load the image file and flash the image file to the SD card. Once that is done, we simply need to load the SD card into the Pi and attach the peripherals (i.e. an HDMI screen and a USB keyboard & mouse).

•	The fourth step is to set up the Pi by entering a username and password to login every time.

•	An fifth step here is to install the VNC server on the raspberry Pi – but is not explained thoroughly here but the explanation for setting it up can be found here - https://www.raspberrypi.org/documentation/remote-access/vnc/ 

•	The final step is to update the Pi with the recent distributions of the Raspbian Buster OS and the same can be done by running the following commands on the terminal:

sudo apt-get update

sudo apt-get upgrade

sudo apt-get install realvnc-vnc-server realvnc-vnc-viewer

**DHT22 sensor library installation:**

•	To install the DHT22 sensor library, please refer to the link: https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/ 

•	The first step in this section is to set up the python3 and pip tools so that the sensor can be run through a python script while the pip tool is a packet management system that installs and manages python packages for the project. Please, run the below commands:

sudo apt-get install python3-dev python3-pip

sudo python3 -m pip install --upgrade pip setuptools wheel

sudo pip3 install Adafruit_DHT

**Python development & libraries:**

•	Since we already installed python3 and pip tools in the previous section, here, we will install other important python libraries that can come handy. Please, execute the below commands so that the libraries are installed:

sudo pip3 install Requests

sudo pip3 install Pillow

sudo pip3 install beautifulsoup4

sudo pip3 install Twisted

sudo pip3 install NumPy

sudo pip3 install SciPy

sudo pip3 install SymPy

sudo pip3 install matplotlib

**Qt & PyQt Installation:**

•	To install the Qt and PyQt libraries, please run the below commands on the Pi CLI:

sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools

sudo apt-get install qttools5-dev-tools

sudo apt-get install python3-tk

Running these commands will install the Qt and PyQt tools on the Pi. Also, the third command will install the Tkinter python application for GUI development natively on the Pi.

**MySQL Database:**

•	To set up the MySQL database for quick storage and acquisition of the voluminous data, we use the MySQL database tool. The first step to use the MySQL database would be to create a database on the target before the Python script is actually run. Please, follow the below commands to set up the MySQL database on the Pi:

sudo apt-get install python-mysqldb

sudo apt-get install mariadb-server

•	Once the above commands are successfully run, the next step would be to secure the MySQL server using the below command:

sudo mysql_secure_installation

Please note, for the above command, the user should answer ‘Y’ to all the questions and a password will be required to be set up for the MySQL server.

•	The next step is to create a MySQL database on the Pi and to do that, please run the below commands on the CLI (terminal):

sudo mysql –u root –p	# user will be prompted to enter the password

CREATE DATABASE <name of the database you want to create>;

CREATE USER ‘root’@’localhost’ IDENTIFIED BY ‘root’;

GRANT ALL PRIVILEGES ON <database name>.* TO ‘root’@’localhost’;

FLUSH PRIVILEGES;

The resource for the above commands can be found here - https://pimylifeup.com/raspberry-pi-mysql/

•	The last step under this section then would be to run the main.py script that will by itself modify the MySQL database tables as required for data storage and acquisition.

# Project Work

For the project work, the breakup of the content was made into the following segments that involved different design and development goals:

1.	Interfacing of DHT22 with the Pi
2.	Design and integration of Matplotlib algorithm to create appropriate graphs
3.	Design and integration of QT GUI
4.	Design and integration of the MySQL database
5.	Addition of required/additional features to the project
6.	Code commenting & Integration
7.	Integrated testing
8.	GitHub and documentation management

**Interfacing of DHT22 with the Pi:**

•	This task was performed as a team by **both the contributors** in the team. Initially, the design and development of this segment was done individually but it was later merged into one working piece.

**Design and integration of the Matplotlib algorithm:**

•	This task was performed as a team by **both the contributors** in the team. The Matplotlib tool was explored on both ends and was later brought into one piece.

**Design and integration of the QT GUI:**

•	This task was performed individually by **Poorn Mehta** and was later merged with the project.

**Design and integration of the MySQL database:**

•	This task was performed individually by **Rushi Macwan** and was later merged with the project.

**Addition of required/additional features to the Project:**

•	This task was performed as a team by **both the contributors** in the team. However, the contribution breakup was also dependent on the above contributions.

**Code Commenting & Integration:**

•	This task was performed as a team by **both the contributors** in the team. However, the contribution breakup was also dependent on the above contributions.

**Integrated testing:**

•	This task was performed as a team by **both the contributors** in the team. However, the contribution breakup was also dependent on the above contributions.

**GitHub documentation management:**

•	This task was performed as a team by **both the contributors** in the team. However, the contribution breakup was also dependent on the above contributions.

# Project Additions

As part of an extended effort for this project, the following additions were above the project requirements:

1.	The user has the ability to specify a desired period at which the system would request the sensor to provide data samples. Ideally, as per the requirement specifications, the system would acquire samples from the DHT22 sensor at an interval of every 15 seconds. However, this additional feature allows the user to change that interval.

2.	In alignment with the previous addition, the UI provides an interactive display to the user with which the user can either use the pre-set 15 seconds sensor data sample acquisition rate, or the user can provide a desirable rate of their own.

3.	The UI has an additional main status text box that provides critical system updates occurring over the execution cycle of the system. Plus, the UI has also has a database status line that reports the condition of the database to the user. For more detailed info into this additional features, please refer to the below points.

4.	The additional main status text box reports to the user with the “PERIODIC UPDATE” or the “IMMEDIATE UPDATE” based on the user’s requests. Whenever the system successfully acquires data samples from the DHT22 sensor, the UI main status text box spits out the data in degrees C or degrees F as per the user request with title “PERIODIC UPDATE”. However, if the user requests an immediate response from the system, the system provides instantaneous data sample from the sensor with the title “IMMEDIATE UPDATE”.

5.	The main status text box will also report the number of seconds the system would let the UI run after the last requested data sample has been successfully acquired and integrated into the database. This additional seconds for reading data samples or interacting with the UI has been provided based on the periodic update time that the user is required to set or use the pre-set value of 15 seconds.

6.	The main status text box also reports if the number of requested data samples from the sensor has been acquired successfully.

7.	The main status line text box on the UI provides an interactive feedback to the user. For example, keeping in mind the limitations of the DHT22 sensor, if the user sends multiple requests for an instantaneous data sample (i.e. temperature and humidity) to the sensor, the UI status line would report the error since the sensor can collect data samples at the highest rate of only one sample per every 2 seconds.

8.	An additional database status line is added to the project features. This database status line reports appropriate success/fail entries to the database. A success entry is shown whenever an acquired data sample from the sensor is integrated into the MySQL database at a synchronized periodic update rate. However, if otherwise, the database status line does report an error in case if the value that the sensor feeds to the system is flawed or unacceptable (e.g. a NULL input from the sensor). Additionally, such flawed values are not accepted by the database to prevent the existing database from any form of corruption. Moreover, the database status line will showcase a statement where nth reading from the sensor data samples is added to the database (e.g. Reading 4th written to database).

9.	The two status segments (i.e. main status text box and the additional database status line) will provide an efficient way to avoid data corruptions into the database system. In addition to these features, when data samples are not available from the sensor (as requested by the user), the main status text box will report that error and eventually keep the system synchronized. By synchronized, it is meant that the system won’t add those flawed values to the database and therefore the numbering of the database won’t be affected (i.e. increment in the numbering of the database readings won’t take place).

10.	The system is designed such that it would terminate both the interactive UI and the code execution after the user-specified number of data samples are successfully acquired by the system from the DHT22 sensor. This means that if the user requests for 30 samples, the system will allow the UI to showcase that 30 readings are acquired and are added to the database. Beyond that point, the system would provide the user a small adjustment time (that is equivalent to one periodic time set by the user) to read the UI updates before the system terminates it as previously mentioned.

11.	An extended feature has been added that produces a graph of the last 10 data samples that are available in the MySQL database. However, in addition to the requirement, the graph would still display 10 data samples even though the database table may contain less than 10 data samples. In such cases, the algorithm will append the remaining unavailable data samples with a 0 value in the graph.

12.	An extra credit feature of conversion from degrees C to degrees F and vice-versa has been added to the algorithm for a more responsive and interactive UI. Moreover, an additional interactive UI button has been added which allows the user to switch the data sample representation from degrees C to degrees F and vice-versa. Plus, the graphs provided on the UI would also represent and switch between degrees C and degrees F as the user sees it fit. 
