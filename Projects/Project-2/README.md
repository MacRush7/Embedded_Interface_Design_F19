# ECEN 5783 EID PROJECT-2 (Fall-2019)

**Project Collaborators/Developers:**

1. **Rushi James Macwan**
2. **Poorn Mehta**

# Repository Overview

This repository is fully owned by **Rushi James Macwan** and **Poorn Mehta**. All content on this repository is solely the work of **Rushi James Macwan** and **Poorn Mehta**. However, all external support and guidance taken in completing the work available on this repository has been clearly cited and credited wherever necessary as per the course guidelines.

For references, please visit the References.pdf file available in the main directory which contains an exhaustive list of all the external resources that were utilized and resourceful in completing this project.

**Please Note:** This repository has been built around the same design as the one created for Project-1 submission which was authored by the same collaborators/developers and the said repository can be found here: https://github.com/MacRush7/ecen5783-eid-project1-f19-rushi-poorn.git

Previous project repositories will be added as submodules to keep a consistent track on the project development. Thanks.

# Installation Instructions

This project involves the use of the following modified/un-modified elements:

**Un-modified elements:**

1.	Raspberry Pi 3B setup
2.	DHT22 sensor library installation
3.	Python development libraries including MatPlotLib
4.	Qt and PyQt Installation
5.	MySQL Database Setup

**Major new elements:**
6.	Tornado Webserver
7.	Node.JS Webserver
8.	Websockets for HTML Client Connection

The explanation below dives deep into setting up the Raspberry Pi 3B to run each of the above elements in a gradual manner in continuation with whatever was mentioned for the Project-1. Please, go through the below points for a detailed explanation:

**Tornado Webserver:**

• To install the Tornado library for webserver development, please run the below commands:

pip install tornado

**Node.JS Webserver:**

• To install the Node.JS webserver on your raspberry pi, please run the below commands:

sudo apt-get install nodejs

**Websockets for HTML Client Connection:**

• To install websockets, please run the below command on your Rpi:

npm install websocket


# Project Work

For the project work, the breakup of the content was made into the following segments that involved different design and development goals:

1.	Python integrated Tornado webserver development
2.	MySQL integrated Node.JS webserver development
3.	HTML client development
4.	Addition of required/additional features to the project
5.	Code commenting & Integration
6.	Integrated testing
7.	GitHub and documentation management

**Python integrated Tornado webserver development:**

• This task was performed individually by Poorn Mehta and was later merged with the project.

**MySQL integrated Node.JS webserver development:**

• This task was performed individually by Rushi Macwan and was later merged with the project.

**HTML client development:**

• This task was performed as a team by both the contributors in the team. However, the contribution breakup was also dependent on the above contributions.

**Addition of required/additional features to the Project:**

• This task was performed as a team by both the contributors in the team. However, the contribution breakup was also dependent on the above contributions.

**Code Commenting & Integration:**

• This task was performed as a team by both the contributors in the team. However, the contribution breakup was also dependent on the above contributions.

**Integrated testing:**

• This task was performed as a team by both the contributors in the team. However, the contribution breakup was also dependent on the above contributions.

**GitHub documentation management:**

• This task was performed as a team by both the contributors in the team. However, the contribution breakup was also dependent on the above contributions.


# Project Additions / Error Handling Considerations

As part of an extended effort for this project, the following additions and error considerations were made around the project requirements:

1.	The HTML client has been provided with the ability to report for errors notifying the user about a lack of connection link between the Node.JS or Tornado Webservers via the Websockets and the HTML client. This takes place in many ways: the user is provided an alert window whenever a connection is opened/closed, a log message would appear on the HTML client page at all instances stating if the connection is open/close, and the reporting of the HTML client to the user whenever a client request is not serviced by any of the two servers using a prompt error message.

2.	The HTML client has the ability to handle data acquisition errors incurred by its connection with the Webservers. For example, if the Node.JS webserver is requested by the HTML client to send the last 10 entries (i.e. NET_TEST) and if the number of entries in the MySQL database is less than 10, the Node.JS webserver will append 0% values for the humidity entries beyond the ones that are available in the MySQL database that is linked with the Node.JS webserver. Eventually, the HTML client would report a humidity of 0% for entries that do not exist in the MySQL database. A similar approach is applied for the Tornado Webserver where a failed data acquisition request for an immediate data entry request results into a prompt message stating that the requested data entries are not available.

3.	Timestamps are provided to the HTML client for the execution times as well as start and end time required for the Webservers to service the critical sections of the request sent out by the client. In cases where the data entries requested by the client are not available in the database, the Node.JS Webserver for an example would append 0% value for the humidity entries that are not available in the database. Eventually, this will reduce the execution time and in case if the associated entries are all appended as 0%, the timestamp will report 0 useconds as the execution time – stating that the Webserver did not have to fetch database values to the client (as they were not available).

# ISSUES WITH PROJECT DEMONSTRATION

During the project demonstration a few minutes ago, we had an issue running the python script which contained comments as in the docstring style. The script was crashing because of this issue, in addition to the fact that the script did not run the python script in background. After due discussion with Dr. Bruce Montgomery and TA Sharanjeet Mago, we have just now removed the docstring comments and appended '#' instead of '''. Plus, we have added a '&' in the script to run the python script as a background process so that when the Node.JS script is run, the Python created database already exists and so that the code does not crash.

To summarize, please see below for the only changes we made at this time:

1. **Added '&' in the script.sh (bash script) file to run the python script as a background process.**
2. **Removed ''' docstrings in the python script and replaced it with # to run it without crashing.**

Thanks.
