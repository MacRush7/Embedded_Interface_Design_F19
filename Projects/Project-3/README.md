# ECEN 5783 EID PROJECT-3 (Fall-2019)

**Project Collaborators/Developers:**

1. **Rushi James Macwan**
2. **Poorn Mehta**

# Repository Overview

This repository is fully owned by **Rushi James Macwan** and **Poorn Mehta**. All content on this repository is solely the work of **Rushi James Macwan** and **Poorn Mehta**. However, all external support and guidance taken in completing the work available on this repository has been clearly cited and credited wherever necessary as per the course guidelines.

For references, please visit the References.pdf file available in the main directory which contains an exhaustive list of all the external resources that were utilized and resourceful in completing this project.

**Please Note:** This repository has been built around the same design as the one created for Project-2 submission which was authored by the same collaborators/developers and the said repository can be found here: https://github.com/MacRush7/ecen5783-eid-project2-f19-rushi-poorn.git

Previous project repositories will be added as submodules to keep a consistent track on the project development. Thanks.

# Installation Instructions

For this project, a few basic elements have been touched and added to construct and deliver the requirements. The elements that go into building this project are as below:

1. Python Data Push Handler
2. AWS IoT
3. AWS Lambda (Python supported)
4. AWS SQS Queue Support
5. AWS SNS Messaging Support
6. Modified HTML Client with Browser support
7. Cellphone Text Messaging / E-mail support

**Python Data Push Handler**

For this part, a python script has been created that would incorporate the use of MQTT protocol to communicate with the AWS IoT Core for communicating the data information gathered from the sensor (DHT22) via the Python application.

**AWS IoT Core**

This is the first entry point in the AWS Cloud where the data acquired by the python application running on a Raspberry Pi from the DHT22 sensor is fed to the AWS IoT element using MQTT. The AWS IoT Core is interfaced with AWS Lambda functions such that one of the them is able to communicate with the AWS SQS Queue support element while the other one is able to communicate with the AWS SNS Messaging support.

**AWS Lambda (Python supported) - Connected with AWS SQS Queue & AWS SNS Messaging support**

This is the second element in the AWS Cloud where the the AWS IoT core transfers all the acquired events from the Python Data Push Handler to the AWS Lambda. The supported language for AWS Lambda used in this project is Python. AWS Lambda runs the underlying API gateway and CloudWatchLog for monitoring the events. Alert events triggered by the AWS IoT Core and that are sent to the AWS Lambda functions is directed towards the AWS SNS messaging support for flushing out alert data to a user via both a text message and an e-mail support. Normal data events acquired from the AWS IoT Core by the AWS Lambda function is fed to the AWS SQS Queue support for data storage and retrieval when the HTML client seeks the data. 

**Modified HTML Client**

The modified HTML client performs all the functions and offers all the original features from the previous projects. In addition to that, the HTML Client communicates with the AWS SQS Queue support via HTTP means. Given that, an extra credit effort has been accomplished where the HTML Client has the ability to receive the total number of data that is present inside the AWS SQS Queue.

**Cellphone Text Messaging / E-mail support**

This is the end point where the alert data triggered by the AWS Lambda function is sent to AWS SNS and from there data is fed to the cellphone as a text message with an additional e-mail support.

**General AWS Project Work Installation Instructions**

For the AWS elements, appropriate configurations have been made to the **AWS Educate Student Account** to include IAM Roles, API Gateway Policies, SQS & Lambda function support, and SNS messaging/e-mailing support. The major development has been done in **Python 3.7** for the Lambda function development. However, for the HTML Client, modifications have been made using JS & HTML resources.

# Project Work

For the project work, the breakup of the content was made into the following segments that involved different design and development goals:

**1.	MQTT integrated Python support for AWS IoT Core**

Design and development of the MQTT interface between Python application (Python Data Push Handler) and the AWS IoT Core was done here.

**2. AWS Lambda Function Support**

The AWS Lambda functions were created appropriately so that it can interact with events coming from the Python Data Push Handler through the AWS IoT Core.

**3.	AWS Lambda-SQS/SNS Support**

The AWS Lambda support for AWS SQS and AWS SNS has been built around the philosophy focused on alert data and usual sensor data acquired by the Python application on a Raspberry Pi. Appropriate functionalities as previously mentioned in the Installation instructions have been added to the AWS elements.

**4.	HTML Client Additions**

The HTML Client is responsible for handling client requests and reading / processing information stored in the AWS SQS using HTTP support.

**5.	Code commenting & Integration**

Code commenting and integration was done using the AWS Educate Student Account and Python Applications created for other elements to run the project cohesively with all the new and original elements up and running.

**6.	Integrated testing**

Final tests performed to ensure that the Project goals are met for Project-3 requirement and that the original requirements for previous projects are still supported.

**7.	GitHub and documentation management**

Structuring GitHub repository for ease and clear-concise information delivery with the addition of this ReadMe file for detailed explanation on the efforts.

**8.  AWS/Google Cloud Cost Estimation**

Exhaustive analysis of cost estimation for AWS/Google cloud storage services for a period of one month based on the available parameters to be set for an accurate cost estimation and comparison.

***The above tasks were performed as a team by the contributors using efforts sourced from references presented in class and the resources available online. All references have been added in the appropriate source files. Thanks.***

# Project Additions

The project addition involves an extra-credit effort that ensures that the HTML Client is able to display the amount of data stored/available in the AWS SQS that is directly interfaced with the HTML Client via HTTP.

In addition to that, as an extra credit effort, the HTML client is provided with the ability to furnish display cleanup while also guaranteeing that accurate degrees C to degrees F and vice-versa transformations are enabled for the data that is being read from the AWS SQS.

Error handling features have been incorporated pertaining to the events arising on the AWS Lambda function and otherwise where the client has the ability to look for errors with the project deliverables.

# Project Issues

There were multiple issues throughout the project development and those issues have been exhaustively provided below:

1. There were issues with the interfacing of AWS Lambda with AWS SQS. There is a lack of critical information on implementing the same while there is a significant amount of documentation for AWS Lambda triggering enabled through SQS events - which is the reverse of the Project requirements expect.

2. Amazon AWS documentation does provide support on the AWS Lambda - AWS SQS interface. However, that information is related with JS development around which the Lambda function has been generated. The project requirements specified Python as an alternative to the AWS Lambda function and AWS SQS communication and a lack of sufficient documentation was experienced. However, BOTO3 (Amazon AWS SDK for Python) provided appreciable support on the same through which the implementation was made possible.

3. The data objects that the HTML client was receiving from the AWS SQS was in a format other than JSON and it was difficult to figure out a workaround for easy string generation on the HTML end. It required a lot of effort to convert the acquired information to absolute string on the HTML Client side using multiple nested object referencing.

4. There were issues with data deletion in the AWS SQS using the HTML Client end.

5. The data that was acquired on the HTML Client end from the AWS SQS using a standard queue (instead of a FIFO queue), was often out of order and repeated. There was a lack of one-to-one correspondence between the nested object referencing that was made on the HTML Client side and the data objects that were being shared with the Client by the AWS SQS.

6. Issues have been identified with the communication between AWS IoT Core and AWS Lambda function where occasionally, the AWS Lambda function triggers more than one instances of the same data to the downlink AWS SQS channel which may account for data repetition.
