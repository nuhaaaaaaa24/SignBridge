================
Admin Blueprint
================

Overview
========

The ``admin`` blueprint handles all the admin related functionality including user management. It is registered under the ``/admin`` URL prefix.

Routes
======

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - URL
     - Method
     - Description
   * - ``admin/admin-dashboard``
     - GET, POST
     - Renders the dashboard form. Shows all the users registered with options to toggle admin, unblock user and delete user.
   * - ``/user/<int:id>/toggle-admin``
     - POST
     - Allows the admin to add an admin or remove an admin. Cannot be used on yourself.
   * - ``/user/<int:id>/delete``
     - POST
     - Allows admins to delete users registered in the system. Cannot be used on yourself
   * - ``/user/<int:id>/unblock``
     - POST
     - Unblocks a user and resets their failed login attempts.

Access Control
==============

All routes require ``@login_required`` and ``@admin_required``.

Forms
=====

* ``ToggleAdminForm`` — submit
* ``DeleteUserForm`` — submit
* ``UnblockUserForm`` — submit

Templates
=========

* ``admin/admin-dashboard.html``

Security Notes
==============
