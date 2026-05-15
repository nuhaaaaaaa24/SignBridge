Security
========


1. Executive Summary
--------------------

This document presents a detailed description of the security architecture that has been established within the Sign Bridge web application. It details our threat model, privacy protections, and the specific technical controls implemented to guarantee the **confidentiality**, **integrity**, and **availability** **(CIA)** of the system and user data.

2. Threat Model & Mitigation Strategies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Potential security risks affecting the application's authentication and data management components were determined. The following countermeasures have been implemented to reduce the chance and impact of these threats.

+------------------------------------------+---------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Threat                                   | Risk Scenario                                     | Applied Mitigation                                                                                                                                                           |
+==========================================+===================================================+==============================================================================================================================================================================+
| Unauthorised Access (Brute-Force)        | Attacker guessing user credentials (Passwords)    | Strict password complexity to prevent entering insecure passwords, moving-window rate limiting, and automated account lockouts after specified number of failed login        |
|                                          | or spamming logins.                               | attempts. Integration of Google reCAPTCHA v2 on all authentication forms to block automated bot scripts.                                                                     |
+------------------------------------------+---------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Stream Interception (Man-in-the-Middle)  | Unwanted third parties spying on the real-time    | WebRTC end-to-end encryption, with DTLS & SRTP built-in.                                                                                                                     |
|                                          | video or audio stream between users.              |                                                                                                                                                                              |
+------------------------------------------+---------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Database Breaches & Credential Leaks     | Database breaches revealing user passwords        | One-way cryptographic hashing (Flask-Bcrypt) with unique salting.                                                                                                            |
+------------------------------------------+---------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Forged Requests                          | Malicious sites tricking users into executing     | Unique CSRF tokens on all state-changing forms.                                                                                                                              |
|                                          | actions                                           |                                                                                                                                                                              |
+------------------------------------------+---------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Denial of Service                        | Malicious scripts/bots overwhelming server        | Endpoint-specific rate limiting mechanism                                                                                                                                    |
|                                          | resources                                         |                                                                                                                                                                              |
+------------------------------------------+---------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

*Table 1 - Threat Model and Mitigation strategies*


3. Privacy Impact Assessment (PIA)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

User privacy is a core architecture design principle of the system as regards the processing of video stream information and user accounts.

**AI Processing at the Edge**: The Sign Language detection model (MobileNetV2 CNN) is processed locally in the browser using TensorFlow.js. The video is processed on the client side and is not shared with or stored on our servers.

**Data Minimisation**: The application collects only the necessary information such as username, email-address, and hashed password. No biometric or video data is stored.

**Session Integrity**: A timeout period of 30 minutes is automatically set to protect users who might leave their devices unattended.


4. Implemented Security Controls
---------------------------------

The following technical controls and policies have been implemented to enforce the security architecture and protect user data.

4.1 Rate Limiting
~~~~~~~~~~~~~~~~~~
The system implements a moving-window based rate limiting on critical endpoints to reduce the risk of brute-force attacks and resource exhaustion. This allows request to be monitored over a rolling time period to allow for accurate control, and grants endpoint-specific limits based on the expected usage of each feature and the security requirements of that feature (Rate Limiting Strategies, n.d.).

+-------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| Endpoint                            | Rate Limit          | Description                                                                                                          | Detection Mechanism and Method               | Security Response                                                                                                                                 |
+=====================================+=====================+======================================================================================================================+==============================================+===================================================================================================================================================+
| Login (/login)                      | 5 requests/minute   | Slowdown repeated login attempts, reducing the effectiveness of brute-force attacks on user credentials and          | Detection Mechanism – Username-based         | The system automatically denies the request and prevents subsequent login requests/attempts for that specific username during the rest of the     |
|                                     |                     | lowering server load.                                                                                                | Method - POST                                | minute without any credential being processed.                                                                                                    |
+-------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| Register (/register)                | 5 requests/minute   | Slowdown repeated registration attempts, reducing automated bot account creation and lowering server load.           | Detection mechanism - Client IP address      | The system automatically denies the request and prevents subsequent registration requests/attempts from that specific IP address during the rest  |
|                                     |                     |                                                                                                                      | Method - POST                                | of the minute without creating any account.                                                                                                       |
+-------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| Create Room (/create-room)          | 5 requests/minute   | Slowdown frequent room creation requests to prevent unnecessary room creations that may cause system overload.       | Detection mechanism – User ID                | The system automatically denies the request and prevents subsequent room creation requests from that specific user ID during the rest of the      |
|                                     |                     |                                                                                                                      | Method - POST                                | minute.                                                                                                                                           |
+-------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| Join Room (/join)                   | 10 requests/minute  | Slowdown repeated join attempts to discourage automated attempts to join chat rooms and guess room IDs through       | Detection mechanism – User ID                | The system automatically denies the request and will not allow any other attempts of join for that user ID for the rest of the minute.            |
|                                     |                     | brute force.                                                                                                         | Method - POST                                |                                                                                                                                                   |
+-------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| Meeting Room Access (/call)         | 10 requests/minute  | Slowdown repeated loading of the active meeting room, avoiding attackers from overloading the server by rapidly      | Detection mechanism - User ID                | The system automatically denies requests and prevent subsequent loads of the meeting room interface from that user ID during the rest of the      |
|                                     |                     | refreshing the video call interface.                                                                                 | Method: GET                                  | minute.                                                                                                                                           |
+-------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| Password Reset Requests             | 5 requests/minute   | Slowdown password reset requests to avoid attackers from spamming user inboxes and exhausting the server's email     | Detection mechanism - Client IP address      | The system rejects the requests and stop further reset emails from being sent from that IP address for the rest of the minute.                    |
| (/reset_pasword_request)            |                     | limits.                                                                                                              | Method - POST                                |                                                                                                                                                   |
+-------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| Reset Password (Tokens)             | 3 requests/minute   | Slowdown the submission speed of new passwords to protect the server CPU from heavy Bcrypt (cryptographic) hashing   | Detection mechanism – Client IP address      | The system refuses the request and prevents subsequent password changes from that IP for the rest of the minute.                                  |
| (/reset_password/<token>)           |                     | operations.                                                                                                          | Method - POST                                |                                                                                                                                                   |
+-------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| Edit Profile                        |                     | Slowdown frequent, automated changes to account details, avoiding scripts from maliciously altering user profiles.   | Detection Mechanism – User ID                |                                                                                                                                                   |
| (/your-account/edit_profile)        | 5 requests/minute   |                                                                                                                      | Method - POST                                | The system refuses the profile update request for the rest of the minute.                                                                         |
|                                     |                     |                                                                                                                      |                                              |                                                                                                                                                   |
+-------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+

*Table 2: Endpoint specific Rate Limits*


4.2 Password Policy
~~~~~~~~~~~~~~~~~~~~~

The Sign Bridge application incorporates a strong password policy to securely authenticate users and protect the system. These policies prevent weak passwords to be set, thus preventing unauthorised access through the guessing of passwords, dictionary attacks, and automated brute-force attacks.

+-----------------------------+------------------------------------------------------------------+
| Requirements                | Description                                                      |
+=============================+==================================================================+
| Minimum Character Length    | Password must be at least 12 characters long.                    |
+-----------------------------+------------------------------------------------------------------+
| Uppercase Letters           | At least one uppercase letter (A-Z) is mandatory.                |
+-----------------------------+------------------------------------------------------------------+
| Lowercase Letters           | At least one lowercase (a-z) is mandatory.                       |
+-----------------------------+------------------------------------------------------------------+
| Digits                      | At least one numeric digit (0-9) is mandatory.                   |
+-----------------------------+------------------------------------------------------------------+
| Special Characters          | At least one special character from the set (!@#$%^&*) is        |
|                             | mandatory.                                                       |
+-----------------------------+------------------------------------------------------------------+

*Table 3: Password Policies*


4.3 Account Lockout Policy
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Sign Bridge application uses an automatic lockout policy to help prevent sophisticated brute-force and credential-stuffing attacks that circumvent regular rate limits.

+-----------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Feature                     | Description                                                                                                                                                                  |
+=============================+==============================================================================================================================================================================+
| Failed Attempt Threshold    | The system logs all the unsuccessful login attempts on the dataset. If there are 10 successive failures, the user's account will be automatically flagged as "blocked".      |
+-----------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Admin Protection Rule       | To guard against "Denial of Service" attacks against system recovery, the admin accounts are excluded from the automatic locking process.                                    |
+-----------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Manual Unblocking           | A blocked user will automatically be unblocked after 30 minutes. Additionally, administrator can also manually unblock any user's account via the admin dashboard at any     |
|                             | time.                                                                                                                                                                        |
+-----------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

*Table 4 - Account Lockout and Administrative Controls*


4.4 Password Protection (Hashing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sign Bridge makes sure that raw user passwords are not stored in the database. The application instead relies on the Flask-Bcrypt hashing algorithm to ensure a high degree of security of the credentials stored. This is in line with Open Worldwide Application Security Project (OWASP) recommendations on proper password storage methods, providing strong security on user data (passwords).

+----------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Capability           | Description                                                                                                                                                                                          |
+======================+======================================================================================================================================================================================================+
| One-Way Hashing      | Bcrypt is a one-way hashing function, that is used for password protection. The original plaintext password cannot be easily recovered from the hash value. When users register, passwords,          |
|                      | are hashed using bcrypt.generate_password_hash(password), and when users reset their passwords, the new one is hashed using the same function.                                                       |
+----------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Salting technique    | Automatically adds a unique random salt (random sequence of characters) to each password before hashing. This guarantees that even if two or more users use the identical passwords, then the hash   |
|                      | values of these passwords in the database will be different, helping prevent Rainbow Table attacks and making password cracking harder (Paquiao & Bajao, 2025).                                      |
+----------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Work Factor          | Flask-Bcrypt uses bcrypt's work factor (cost parameter) which increases the computational effort required to hash passwords. SignBridge uses the default Bcrypt work factor when creating the hash,  |
|                      | which is 12, meaning it hashes the password 2\ :sup:`12` (4096) times. This helps to slow down brute force attacks and makes it harder for threat actors to recover original password from stolen    |
|                      | hashes (Paquiao & Bajao, 2025).                                                                                                                                                                      |
+----------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Security             | When a user is signed in, the Flask-Bcrypt calls the ``bcrypt.check_password_hash()`` function to check the password by hashing the user's password and comparing it to the one stored in the        |
| Verification         | database. Salt and cost factor is already included in the stored hash. System does internal verification and returns True/False without revealing or storing plaintext password (Flask-Bcrypt, n.d). |
+----------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

*Table 5: Password Protection (Hashing) with Flask-Bcrypt*


4.5 Inactive Session Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The application has an automated session time out as a security mechanism against users who might leave their accounts unattended to in a device. This makes sure that inactive sessions are killed and the chance of unauthorised physical access to an account of a user are minimised.

**Session Policy Details**

**Session Lifetime:** The application implements a strict 30-minute inactive user logging timeout. If the user does not interact with the application within this time frame, the session cookies expire, and the user is logged out.

**Rolling Expiration:** Timeout period is dynamically calculated. Each action on the site resets the timer back to 30 minutes.


4.6 Browser-Level Security (HTTP Headers)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The application ensures that security instructions are automatically injected into each HTTP response. These headers instruct the user's browser on how to securely handle content to protect against many of the most prevalent web vulnerabilities.

+------------------------------------+--------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------+
| Security Header                    | Policy Detail                                                                                                | Mitigation (Prevents)                                                 |
+====================================+==============================================================================================================+=======================================================================+
| Strict-Transport-Security (HSTS)   | Creating a secure communication connection by directing browsers to establish connection only using HTTPS    | Prevents SSL stripping and Man-in-the-Middle (MitM) attacks.          |
|                                    | for one year (31,536,000 seconds) (Ahmad, 2025).                                                             |                                                                       |
+------------------------------------+--------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------+
| X-Frame-Option                     | Initialised to **SAMEORIGIN**, which restricts the application from being embedded inside hidden frames on   | Prevents Clickjacking attacks.                                        |
|                                    | malicious third-party websites (Ahmad, 2025).                                                                |                                                                       |
+------------------------------------+--------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------+
| X-Content-Type-Options             | Initialised to **nosniff**, which tells the browser to rigorously follow the declared content type and       | Prevents MIME type sniffing problems that can cause Cross-Site        |
|                                    | disables attempts to guess or sniff the MIME type (Ahmad, 2025).                                             | Scripting (XSS) attacks.                                              |
+------------------------------------+--------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------+

*Table 6 - Browser Level security headers*

4.7 Secure Real-Time Communication (WebRTC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The primary functionality of the Sign Bridge web application, the call functionality, is implemented using the WebRTC framework, which provides secure real-time communication for media exchange and signaling. 
All media streams in a WebRTC connection are encrypted. The video and audio stream between participants are encrypted using Secure Real-Time Transport Protocol (SRTP), and the data channels are secured using Datagram Transport Layer Security (DTLS) (A Study of WebRTC Security, n.d.). This guarantees that communication is confidential and cannot be intercepted by third parties.

4.8 Protection Against Cross-Site Request Forgery (CSRF)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The application implements Cross-Site Request Forgery protections using the built-in mechanisms provided by WTForms (through Flask-WTForms). Forms are configured to include per-request CSRF tokens that are validated on submission. Data is processed server-side (enforced through the *novalidate* method in client-side HTML forms) to ensure WTForms' CSRF protections are not hampered.

**WTForms' CSRF Protection Details**

WTForms generates 64 cryptographically random bytes using the SHA-1 algorithm to use as its per-session CSRF token. This is embedded within each form. Upon submission, the server verifies the presence and validity of this token before processing the request. If the token is missing or invalid, the request is rejected.


4.9 Secure Token Management (JWT)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The password reset flow uses a Signed JSON Web Token (JWT) for authentication. The token payload carries two claims: the user ID of the user who requested it and a standard expiry time stamp set to 600 seconds (10 minutes) after generation. This token is signed with HMAC-SHA256 using the application's secret key. Additionally, this token is not stored in the database. Verification is performed by decoding the JWT and confirming its signature.

As the algorithm used is symmetric, the same key is used to both sign and verify the token. The secret key must therefore be kept confidential.

4.10 Rest API Token Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The Sign Bridge application has a secure bearer token authentication mechanism for its RESTful API, which is to support programmatic access and potentially future integrations (mobile application). This system keeps all the API-Endpoints protected and only lets authenticated users access them. The aim of devolved token management is security and developer experience.

+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| Capability                         | Description                                                                                                  |
+====================================+==============================================================================================================+
| Secure Token Generation            | If login or registration is successful, a unique 32 character cryptographically secure random token is       |
|                                    | generated for the user (via python secrets module). This token is kept in the database with user’s record.   |
+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| Token Expiration                   | API tokens each have a lifetime (1 hour). On every API call to the server, the server checks the expiry      |
|                                    | time of the token and rejects any service requests made with expired tokens to prevent indefinite access.    |
+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| Automatic Token Renewal            | The system includes an automatic token renewal mechanism which designed to improve user experience by        |
|                                    | ensuring that there are no unexpected session terminations for active users. When a token is valid and       |
|                                    | used within 60 seconds of its expiration, a new token with a fresh 1-hour lifetime is automatically          |
|                                    | generated and committed to that user.                                                                        |
+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| Token Revocation                   | The system includes a way to revoke a user’s API token right away. This is done by placing the token’s       |
|                                    | expiration timestamp to a time in the past. This important process is applied in security related scenarios  |
|                                    | including when a user schedules for deletion of their account.                                               |
+------------------------------------+--------------------------------------------------------------------------------------------------------------+

Table 7: RESTful API Token Managements

4.11 Roles Based Access Control (RBAC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This web application follows the Role-Based Access Control (RBAC) model and thus provides features and functions that are separated between normal users and admin users. This ensures that normal users only have access to the specific feature necessary for their assigned role:

**Standard Users**: Limited to core application functionalities, such as updating their personal profile, viewing their dashboard, and accessing standard video call interface.

**Administrators:** Entrusted with controlling the administration routing subsystem. This gives the ability to manage users' accounts, including the ability to unblock profiles that have been locked due to brute-force protection mechanism.


4.12 Automated Bot Protection (reCAPTCHA v2)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Google reCAPTCHA v2 is integrated into the authentication process in an effort to prevent automated scripts and spam account creation. The "I'm not a robot" verification will be strictly required for both registration (sign up) and login forms. This prevents automated bots from even starting to try and access or create accounts, and in effect stops the brute force attack bots before it can reach the rate limiters.

Conclusion
----------

In conclusion, the Sign Bridge application was developed using a layer of Defence in Depth approach, where several different types of security controls were implemented to protect user data along with the overall system integrity. Authentication strengthening, secure session management, encrypted real-time communication, and bot prevention each control addresses a particular threat identified in the threat model. All of these security controls work together to ensure confidentiality, integrity, and availability of both the system and user’s data.

3. References
--------------
A Study of WebRTC Security. (n.d.). https://webrtc-security.github.io/

Ahmad. (2025). *Flask security best practices 2025*. Corgea. https://corgea.com/learn/flask-security-best-practices-2025

Flask-Bcrypt. (n.d.). *Flask-Bcrypt*. https://flask-bcrypt.readthedocs.io/en/1.0.1/

Paquiao, L. I. M., & Bajao, Z. E. (2025). The role of hashing libraries in Flask application security: A focus on password protection. *International Journal of Advances in Computer Science and Technology, 14(7)*, 30–34. https://doi.org/10.30534/ijacst/2025/011472025

Rate limiting strategies. (n.d.). *Flask-Limiter.*
 	https://flask-limiter.readthedocs.io/en/stable/strategies.html
