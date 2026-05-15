==================
JS Module Overview
==================

Overview
========

The SignBridge frontend uses modular JavaScript files to manage real-time
communication, machine learning inference, user interaction, and frontend
behaviour within the browser.

The JavaScript architecture separates functionality into independent modules
to improve maintainability, readability, and scalability.

The frontend JavaScript system is responsible for:

* WebRTC communication
* Socket.IO real-time messaging
* TensorFlow.js model inference
* MediaPipe hand landmark detection
* transcript updates
* chat functionality
* webcam and microphone controls
* frontend interaction logic

Module Structure
================

The primary JavaScript modules are located in:

.. code-block:: text

   static/js/
   ├── call.js
   ├── chat.js
   ├── model.js
   ├── privacy-notice.js
   └── register.js

Each module is responsible for a specific frontend feature.

call.js
=======

Overview
--------

``call.js`` manages the core real-time communication workflow within
the SignBridge application.

Responsibilities
----------------

The module handles:

* WebRTC peer-to-peer communication
* Socket.IO signaling
* webcam and microphone access
* call session management
* transcript updates
* gesture recognition control
* mute and camera toggling
* cleanup and disconnect handling

WebRTC Communication
--------------------

The module creates and manages ``RTCPeerConnection`` instances to establish
peer-to-peer video communication between users.

ICE server configuration is used to support NAT traversal and connection
establishment.

Socket.IO Integration
---------------------

Socket.IO is used for signaling communication between clients.

The module handles events such as:

* joining rooms
* exchanging offers and answers
* ICE candidate exchange
* peer disconnect handling
* transcript synchronization

Gesture Recognition Integration
-------------------------------

The module integrates with ``model.js`` to perform sign language inference.

Detected letters are:

* displayed in the transcript
* synchronized between participants
* appended to the transcript interface

Frontend Interaction
--------------------

The module also manages frontend interaction logic including:

* call state updates
* recognition timers
* transcript rendering
* microphone toggling
* camera toggling
* session cleanup

chat.js
=======

Overview
--------

``chat.js`` manages real-time text communication within active
communication sessions.

Responsibilities
----------------

The module handles:

* chat message sending
* chat message rendering
* chat history loading
* real-time message synchronization
* message UI rendering

Socket.IO Integration
---------------------

The chat system shares the Socket.IO connection initialized by ``call.js``.

Incoming chat messages are synchronized between participants in real time.

Frontend Features
-----------------

The module dynamically renders:

* sender labels
* chat bubbles
* timestamps
* system messages
* previous message separators

The module also supports Enter-key message submission.

model.js
========

Overview
--------

``model.js`` manages client-side machine learning inference for
Sri Lankan Sign Language gesture recognition.

Responsibilities
----------------

The module handles:

* MediaPipe hand landmark detection
* TensorFlow.js model loading
* gesture preprocessing
* landmark normalization
* sign classification
* confidence threshold handling

MediaPipe Integration
---------------------

The module uses MediaPipe Hand Landmarker to detect hand landmarks directly
within the browser.

The detected landmarks are normalized before inference.

TensorFlow.js Integration
-------------------------

The trained machine learning model is loaded using TensorFlow.js.

The model performs client-side inference without transmitting video frames to
external servers.

Inference Pipeline
------------------

The inference workflow includes:

1. capture webcam frame
2. detect hand landmarks
3. normalize landmark coordinates
4. create TensorFlow input tensor
5. run classification inference
6. apply confidence threshold
7. return predicted sign letter

Confidence Threshold
--------------------

The module applies a confidence threshold before displaying predictions.

Predictions below the threshold are ignored to reduce incorrect gesture
classification.

privacy-notice.js
=================

Overview
--------

``privacy-notice.js`` manages the privacy notice modal displayed
before a communication sessions begin.

Responsibilities
----------------

The module handles:

* displaying the privacy notice popup
* storing user acknowledgement
* managing local browser persistence

Local Storage Usage
-------------------

The module uses ``localStorage`` to remember whether the user previously
accepted the privacy notice.

This prevents the notice from repeatedly appearing on the same browser or
device.

register.js
============

Overview
--------

``register.js`` provides frontend password validation feedback on
the registration page.

Responsibilities
----------------

The module dynamically validates password requirements including:

* minimum password length
* uppercase characters
* lowercase characters
* numeric characters
* special characters

Frontend Interaction
--------------------

Password requirements are visually updated in real time while the user types.

The module improves usability by helping users understand password
requirements before form submission.

Modular Architecture
====================

The JavaScript system follows a modular frontend architecture where each file
handles a specific responsibility.

Benefits include:

* improved maintainability
* easier debugging
* reusable frontend logic
* simplified feature expansion
* better separation of concerns