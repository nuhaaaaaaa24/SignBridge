==============
Help Blueprint
==============

Overview
========

The ``help`` blueprint has the help page, Sri Lankan Sign Language chart and a video tutorial.
It is registered under the ``/help`` URL prefix.

Routes
======

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - URL
     - Method
     - Description
   * - ``/``
     - GET, POST
     - This acts as an index for the help pages.
   * - ``slslchart``
     - POST
     - Displays the Sri Lankan Sign Language chart.
   * - ``video-tutorial``
     - POST
     - Shows the video tutorial.

Templates
=========

* ``help/help.html``
* ``slslchart.html``
* ``video-tutorial.html``
