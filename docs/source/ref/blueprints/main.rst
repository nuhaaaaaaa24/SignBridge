==============
Main Blueprint
==============

Overview
========

The ``main`` blueprint handles the landing page and contact. 

Routes
======

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - URL
     - Method
     - Description
   * - ``/index``
     - 
     - Displays the landing page
   * - ``/about``
     - 
     - Displays the about us page
   * - ``/contact``
     - GET, POST
     - Provides users with a way to submit inquiries or report issues encountered within the system.  

Forms
=====

* ``ContactForm`` — name, email, subject, message



Templates
=========

* ``main/about.html``
* ``main/contact.html``
* ``main/index.html``
