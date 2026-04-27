Application Directory Structure
===============================

This section presents the directory structure of the SignBridge application.

Directory Structure
-------------------

.. code-block:: text

   SignBridge
   ├── app
   │   ├── __init__.py
   │   ├── admin
   │   │   ├── __init__.py
   │   │   ├── forms.py
   │   │   ├── routes.py
   │   │   └── utils.py
   │   ├── api
   │   │   ├── __init__.py
   │   │   ├── auth.py
   │   │   ├── errors.py
   │   │   ├── rooms.py
   │   │   ├── tokens.py
   │   │   └── users.py
   │   ├── auth
   │   │   ├── __init__.py
   │   │   ├── email.py
   │   │   ├── forms.py
   │   │   └── routes.py
   │   ├── call
   │   │   ├── __init__.py
   │   │   ├── forms.py
   │   │   ├── routes.py
   │   │   ├── services.py
   │   │   └── sockets.py
   │   ├── core
   │   │   ├── context_processors.py
   │   │   ├── email.py
   │   │   ├── nav.py
   │   │   └── validators.py
   │   ├── errors
   │   │   ├── __init__.py
   │   │   └── handlers.py
   │   ├── help
   │   │   ├── __init__.py
   │   │   └── routes.py
   │   ├── logs
   │   │   ├── signbridge.log.1
   │   │   ├── signbridge.log.2
   │   │   ├── signbridge.log.3
   │   │   ├── signbridge.log.4
   │   │   └── signbridge.log.5
   │   ├── main
   │   │   ├── __init__.py
   │   │   ├── forms.py
   │   │   └── routes.py
   │   ├── models.py
   │   ├── static
   │   │   ├── css
   │   │   │   └── styles.css
   │   │   ├── images
   │   │   │   ├── erd_diagram.png
   │   │   │   └── favicon.ico
   │   │   ├── js
   │   │   │   ├── call.js
   │   │   │   ├── chat.js
   │   │   │   ├── model.js
   │   │   │   └── register.js
   │   │   └── models
   │   │       └── mobilenet-slsl-1
   │   │           ├── class_names.json
   │   │           ├── group1-shard1of3.bin
   │   │           ├── group1-shard2of3.bin
   │   │           ├── group1-shard3of3.bin
   │   │           └── model.json
   │   ├── templates
   │   │   ├── admin
   │   │   │   └── admin-dashboard.html
   │   │   ├── auth
   │   │   │   ├── login.html
   │   │   │   ├── register.html
   │   │   │   ├── reset_password.html
   │   │   │   └── reset_password_request.html
   │   │   ├── base.html
   │   │   ├── call
   │   │   │   ├── call.html
   │   │   │   └── join.html
   │   │   ├── email
   │   │   │   ├── reset_password.html
   │   │   │   └── reset_password.txt
   │   │   ├── error.html
   │   │   ├── errors
   │   │   │   ├── 404.html
   │   │   │   └── 500.html
   │   │   ├── help
   │   │   │   ├── help.html
   │   │   │   ├── slslchart.html
   │   │   │   └── video-tutorial.html
   │   │   ├── main
   │   │   │   ├── about.html
   │   │   │   ├── contact.html
   │   │   │   └── index.html
   │   │   ├── partials
   │   │   │   ├── footer.html
   │   │   │   └── navbar.html
   │   │   └── user
   │   │       ├── dashboard.html
   │   │       ├── edit-profile.html
   │   │       └── user.html
   │   └── user
   │       ├── __init__.py
   │       ├── forms.py
   │       └── routes.py
   ├── migrations
   ├── tests
   │   ├── conftest.py
   │   ├── test_api.py
   │   ├── test_auth.py
   │   ├── test_models.py
   │   ├── test_rooms.py
   │   └── test_selenium.py
   ├── config.py
   ├── extensions.py
   ├── pytest.ini
   ├── signbridge.py
   └── wsgi.py