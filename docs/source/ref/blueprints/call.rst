==============
Call Blueprint
==============

Overview
========

The ``call`` blueprint handles all the call related features.
Join a session, create a room and call room. It is registered under the ``/call`` URL prefix.

Routes
======

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - URL
     - Method
     - Description
   * - ``call/call``
     - GET, POST
     - Renders using the join form. Allows a user to join using the room code.
   * - ``/call/join``
     - GET
     - Renders using the CreateRoom form. Allows a user to create a new room, which redirects users to the waiting room. 
   * - ``call/call.html``
     - POST
     - Redirects users to the call room. 
   

Forms
=====

* ``JoinForm`` — user_name, room_code, submit
* ``CreateRoomForm`` — submit

Templates
=========

* ``call/call.html``
* ``call/join.html``

Security Notes
==============
