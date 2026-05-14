Testing Overview
================

This report presents the testing procedures and results for the SignBridge project, a real-time Sri Lankan Sign Language (SLSL) detection and translation web application. 
The purpose of testing was to evaluate the functionality, reliability, usability, performance, and security of the system. The SignBridge application uses machine learning 
and computer vision technologies to recognize hand gestures through webcam input and convert them into text in real time. Since the system combines frontend, backend, machine 
learning, and real-time communication components, comprehensive testing was required to ensure system stability and usability.
The testing process involved:

* Functional testing
* Security testing
* performance testing
* Accuracy testing
* Usability testing
* Automated testing
* Manual testing



Objectives of Testing
---------------------

The primary objectives of testing were:

* To verify that all functional requirements work correctly
* To identify system errors and bugs 
* To validate reliability of the machine learning model
* To evaluate real-time system performance
* To ensure the system handles invalid inputs securely 
* To confirm that the application provides an acceptable user experience

Testing Environment
-------------------

Operating system

* Windows 10/11

Backend Framework

* Flask 

Frontend Technologies

* HTML, CSS, JavaScript

Machine Learning Framework

* TensorFlow

Testing Framework

* pytest

Browser Automation

* Selenium

Database

* SQLite

Hardware

* Standard laptop with a webcam

Browsers used 

* Google Chrome/Brave

Testing Methodologies
---------------------

The testing process was divided into two major categories:

Manual Testing
``````````````

Manual testing was conducted to validate:

* Real-time webcam functionality
* Gesture recognition
* User interface responsiveness
* System userbility
* Real-world performance

Automated Testing
`````````````````

Automated testing was conducted using pytest and Selenium to validate:

* Backend functionality
* API responses 
* Authentication features
* Route handling
* Error handling
* User interface behavior
