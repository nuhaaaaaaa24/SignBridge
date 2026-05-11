=================
Template Overview
=================

Overview
========

SignBridge uses Flask's Jinja2 templating to render dynamic HTML pages for the web application.

The template layer is responsible for displaying the user interface shown in the browser, 
including authentication pages, profile pages, video call interfaces, help resources and system messages.

Templates are organised into blueprint-specific directories to improve 
maintainability and scalability.

Template Structure
==================

The application templates are organised as follows:

.. code-block:: text

     templates/
   ├── admin/
   ├── auth/
   ├── call/
   ├── email/
   ├── errors/
   ├── help/
   ├── main/
   ├── partials/
   ├── user/
   ├── base.html
   └── error.html

Each directory contains templates related to a specific feature of the application.

Basic Template
==============

The ``base.html`` template acts as the shared layour used throughout the application.
It contains:

* page structure
* linked CSS and Javascript files
* navigation bar
* footer
* reusable content blocks
Other templates extend ``base.html`` using Jinja2 template inheritance.

**Example:**

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
        <h1>Welcome to SignBridge</h1>
    {% endblock %}

This reduces duplicated code and helps maintain interface consistency.

Reusable Components
===================

Reusable interface components are stored inside the ``partials`` directory.

**Example:**

* ``navbar.html``
* ``footer.html``

These partial templates are included inside other templates using Jinja2.

**Example:**

.. code-block:: html

    {% include "partials/navbar.html" %}

Using reusable components improves maintability and ensures a consistent user 
interface throughout the application.

Template Rendering
==================

Templates are rendered through Flask routes using the ``render_template()`` function.

**Example:**

.. code-block:: python

    return render_template("main/index.html")

Jinja2 also allows dynamic data to be inserted directly into templates.

**Example:**

.. code-block:: html

    <h1>Hello, {{ current_user.username }}</h1>

The template layer provides the frontend interface of SignBridge and supports a 
modular, reusable and maintainable application structure.
    
