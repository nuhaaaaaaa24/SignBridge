==============
Errors Blueprint
==============

Overview
========

The ``errors`` blueprint handles all error pages and HTTP errors. It is registered under the ``/errors`` URL prefix.

Routes
======

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - URL
     - Method
     - Description
   * - ``/errors/404``
     - 
     - Displays the 404 Not Found error page.
   * - ``/errors/500``
     - 
     - Displays the 500 Internal Server Error page.


Templates
=========

* ``errors/404.html``
* ``errors/500.html``
