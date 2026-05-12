==========
SLSL Chart
==========

Overview
========

The SLSL Chart page provides users with a visual reference for the Sri Lankan
Sign Language (SLSL) alphabet supported by the SignBridge recognition system.

The page is intended to help users:

* understand supported gesture classes
* learn the corresponding hand signs
* improve gesture recognition accuracy during communication sessions
* familiarise themselves with the system's supported alphabet subset

Purpose
=======

The chart acts as an educational and accessibility resource within
the application.

It is particularly useful for:

* first-time users
* non-signers
* testing gesture recognition
* verifying hand positioning during demonstrations

Supported Letters
=================

The current prototype supports a subset of static SLSL fingerspelling gestures.

The supported classes include:

* A
* E
* I
* O
* U
* L
* N
* R
* S
* T

The displayed chart corresponds directly to the gesture classes used by the
machine learning model.

Frontend Integration
====================

The chart is accessible through the **Help** section of the application.

The page is implemented as a frontend template and displays a visual
reference image that contains the supported gesture alphabet.

The chart is rendered through the browser and does not require backend
processing.

Design Considerations
=====================

The chart page was designed to be:

* simple
* readable
* responsive
* easy to navigate

The interface uses large visual elements and minimal text to improve usability
during live communication sessions.