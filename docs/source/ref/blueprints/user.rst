==============
User Blueprint
==============

Overview
========

The ``user`` blueprint handles all user-related functionality including profile management. It is registered under the ``/your-account`` URL prefix.

Routes
======

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - URL
     - Method
     - Description
   * - ``/user/dashboard``
     -
     - Render the dashboard using Empty form
   * - ``/user/profile``
     - 
     - Render the profile page using Empty form
   * - ``/user/edit-profile``
     - GET, POST
     - Allows the user to edit their profile details

Forms
=====

* ``EditForm`` — user_name, email, current_password, new_password, repeat_new_password, submit
* ``EmptyForm`` — submit

Templates
=========

* ``user/dashboard.html``
* ``user/edit-profile.html``
* ``user/user.html``