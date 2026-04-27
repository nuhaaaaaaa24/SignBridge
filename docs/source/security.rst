Security
========


1. Executive Summary
--------------------

This document presents a detailed description of the security architecture established within the SignBridge web application.

It consists of techniques such as rate limiting, input validation, password encryption, and end-to-end encryption of video streams. These mechanisms ensure the confidentiality of user data, provide safeguards against unauthorized access, and help maintain overall system integrity.


2. Threat Protection: Brute Force Attacks
------------------------------------------


2.1 Risk Assessment
~~~~~~~~~~~~~~~~~~~

Brute force attacks are a considerable threat to the security of user accounts. Unauthorized individuals may attempt to gain access by repeatedly trying multiple username and password combinations.


2.2 Mitigation Control: Rate Limiting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Tool used:** Flask-Limiter

Global Rate Limit Configuration:

- Maximum 200 requests per minute per IP address  
- Request tracking mechanism: Client IP address  
- Enforcement: in-memory storage with minute-based resets  

Each IP address is limited to 200 requests within 60 seconds. If this limit is exceeded, all incoming requests from that IP are automatically blocked until the reset period ends.

This helps prevent attackers from sending hundreds or thousands of rapid requests.


Endpoint-Specific Rate Limits
-----------------------------

+-------------+----------------------+--------------------------------------------------------------+----------------------+--------------------------------------------------------------+
| Endpoint    | Rate Limit           | Description                                                  | Detection Mechanism  | Security Response                                            |
+=============+======================+==============================================================+======================+==============================================================+
| Login       | 5 requests/minute    | Prevents credential brute force attacks                      | Client IP based      | HTTP 429 "Too many requests. Please slow down."              |
+-------------+----------------------+--------------------------------------------------------------+----------------------+--------------------------------------------------------------+
| Registration| 5 requests/minute    | Prevents automated bots creating fake accounts               | Client IP based      | HTTP 429 "Too many requests. Please slow down."              |
+-------------+----------------------+--------------------------------------------------------------+----------------------+--------------------------------------------------------------+
| Create Room | 10 requests/minute   | Prevents abuse or overload from excessive room creation      | Client IP based      | HTTP 429 "Too many requests. Please slow down."              |
+-------------+----------------------+--------------------------------------------------------------+----------------------+--------------------------------------------------------------+
| Join Room   | 10 requests/minute   | Prevents brute force room ID attacks and unauthorized access | Client IP based      | HTTP 429 "Too many requests. Please slow down."              |
+-------------+----------------------+--------------------------------------------------------------+----------------------+--------------------------------------------------------------+