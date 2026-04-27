.. SignBridge documentation master file, created by
   sphinx-quickstart on Mon Apr 27 11:56:40 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==========================
SignBridge Documentation
==========================

Everything you need to know about SignBridge.

.. _index-first-steps:

First steps
===========

Are you new to SignBridge or to the stack it runs on? This is the place
to start!

* **From scratch:**
  :doc:`Overview <intro/overview>` |
  :doc:`Installation <intro/installation>` |
  :doc:`Requirements <intro/requirements>`

* **Configuration:**
  :doc:`config.py reference <intro/config>` |
  :doc:`Environment variables <intro/env>` |
  :doc:`extensions.py overview <intro/extensions>`

* **Tutorial:**
  :doc:`Part 1: Running your first call <intro/tutorial01>` |
  :doc:`Part 2: Models & the database <intro/tutorial02>` |
  :doc:`Part 3: Blueprints & routing <intro/tutorial03>` |
  :doc:`Part 4: The sign language model <intro/tutorial04>` |
  :doc:`Part 5: Testing <intro/tutorial05>`

* **Advanced tutorials:**
  :doc:`Customising the ML pipeline <intro/custom-ml>` |
  :doc:`Writing your first SignBridge plugin <intro/plugins>`

Getting help
============

Having trouble? We'd like to help!

* Try the :doc:`FAQ <faq/index>` — it has answers to many common questions
  about setup, sign recognition, and real-time calling.
* Looking for specific information? Try the :ref:`genindex`,
  or the :doc:`detailed table of contents <contents>`.
* Not found anything? See :doc:`FAQ: Getting Help <faq/help>` for information
  on getting support and asking questions.
* Report bugs with SignBridge in our
  `issue tracker <https://github.com/nuhaaaaaaa24/SignBridge/issues>`_.

How the documentation is organised
===================================

A high-level overview of how our documentation is
organised will help you know where to look for certain things:

* :doc:`Tutorials <intro/index>` take you by the hand through a series of
  steps to run a working SignBridge instance. Start here if you're new to the
  project. Also look at the ":ref:`index-first-steps`".
* :doc:`Topic guides <topics/index>` discuss key topics and concepts — the
  blueprint architecture, the Socket.IO event bus, the SLSL model pipeline —
  at a fairly high level and provide useful background information and
  explanation.
* :doc:`Reference guides <ref/index>` contain technical reference for the REST
  API, model schemas, configuration keys, and Socket.IO events. They describe
  how things work and how to use them, but assume that you have a basic
  understanding of key concepts.
* :doc:`How-to guides <howto/index>` are recipes. They guide you through the
  steps involved in addressing key problems and use-cases, such as swapping the
  ML model, adding a new blueprint, or deploying with gunicorn and nginx. They
  are more advanced than tutorials and assume some knowledge of how SignBridge
  works.


The model layer
===============

SignBridge uses Flask-SQLAlchemy with a single ``models.py`` to define the
data layer, and Flask-Migrate to manage schema evolution against a PostgreSQL
database.

* **Models:**
  :doc:`Introduction to models <topics/db/models>` |
  :doc:`ERD diagram <ref/erd>` |
  :doc:`Field reference <ref/models/fields>` |
  :doc:`Relationships <ref/models/relationships>`

* **Migrations:**
  :doc:`Introduction to Flask-Migrate <topics/migrations>` |
  :doc:`Running migrations <howto/run-migrations>` |
  :doc:`Writing migration scripts <howto/write-migrations>`

* **Queries:**
  :doc:`Making queries with SQLAlchemy <topics/db/queries>` |
  :doc:`Query optimisation <topics/db/optimisation>`

* **Database:**
  :doc:`PostgreSQL configuration <ref/databases/postgres>` |
  :doc:`SQLite for local development <ref/databases/sqlite>` |
  :doc:`Seeding initial data <howto/initial-data>`


The blueprint layer
===================

SignBridge has the concept of *blueprints* to encapsulate the logic
responsible for processing a user's request and returning a response. The
application is divided into the following blueprints: ``main``, ``auth``,
``call``, ``user``, ``admin``, ``help``, and ``errors``.

* **The basics:**
  :doc:`Blueprint registration <topics/blueprints>` |
  :doc:`Route functions <topics/routing>` |
  :doc:`Context processors (core/context_processors.py) <ref/context-processors>` |
  :doc:`Decorators & login_required <topics/auth/decorators>`

* **Blueprint reference:**
  :doc:`main <ref/blueprints/main>` |
  :doc:`auth <ref/blueprints/auth>` |
  :doc:`call <ref/blueprints/call>` |
  :doc:`user <ref/blueprints/user>` |
  :doc:`admin <ref/blueprints/admin>` |
  :doc:`help <ref/blueprints/help>` |
  :doc:`errors <ref/blueprints/errors>`

* **Services:**
  :doc:`call/services.py <ref/call/services>` |
  :doc:`Room management <topics/call/rooms>` |
  :doc:`Session utilities <topics/call/sessions>`

* **Error handling:**
  :doc:`errors/handlers.py <ref/errors/handlers>` |
  :doc:`Custom 404 & 500 pages <howto/custom-error-pages>`

* **Navigation:**
  :doc:`core/nav.py <ref/core/nav>` |
  :doc:`Dynamic navbar generation <topics/nav>`


The template layer
==================

The template layer provides a Jinja2-based syntax for rendering the
information to be presented to the user. SignBridge templates are organised
around a shared ``base.html`` and blueprint-specific subdirectories.

* **The basics:**
  :doc:`Template overview <topics/templates>` |
  :doc:`base.html & template inheritance <topics/templates/inheritance>` |
  :doc:`Partials — navbar & footer <topics/templates/partials>`

* **By blueprint:**
  :doc:`main <ref/templates/main>` |
  :doc:`auth <ref/templates/auth>` |
  :doc:`call <ref/templates/call>` |
  :doc:`user <ref/templates/user>` |
  :doc:`admin <ref/templates/admin>` |
  :doc:`help <ref/templates/help>` |
  :doc:`Email templates <ref/templates/email>`

* **For designers:**
  :doc:`Jinja2 language overview <ref/templates/language>` |
  :doc:`styles.css reference <ref/static/css>` |
  :doc:`Custom filters <howto/custom-template-filters>`


Forms
=====

SignBridge uses Flask-WTF for all form handling, with form classes defined in
each blueprint's ``forms.py`` module.

* **The basics:**
  :doc:`Flask-WTF overview <topics/forms>` |
  :doc:`CSRF protection <topics/forms/csrf>` |
  :doc:`Custom validators (core/validators.py) <ref/core/validators>`

* **Form class reference:**
  :doc:`auth/forms.py <ref/forms/auth>` |
  :doc:`call/forms.py <ref/forms/call>` |
  :doc:`user/forms.py <ref/forms/user>` |
  :doc:`main/forms.py <ref/forms/main>` |
  :doc:`admin/forms.py <ref/forms/admin>`

* **Advanced:**
  :doc:`Dynamic form rendering <howto/dynamic-forms>` |
  :doc:`Client-side validation with register.js <topics/forms/client-validation>`


Authentication
==============

SignBridge provides full user lifecycle management — registration, login, and
email-based password reset — alongside a token-based REST API authentication
system.

* **Overview:**
  :doc:`Authentication overview <topics/auth>` |
  :doc:`Login & registration flows <topics/auth/flows>` |
  :doc:`Password reset by email <topics/auth/password-reset>`

* **Tokens:**
  :doc:`api/tokens.py <ref/api/tokens>` |
  :doc:`Token generation & revocation <topics/auth/tokens>` |
  :doc:`Protecting API routes <howto/protect-api-routes>`

* **Email:**
  :doc:`auth/email.py <ref/auth/email>` |
  :doc:`core/email.py <ref/core/email>` |
  :doc:`Email template reference <ref/templates/email>`

* **User profiles:**
  :doc:`user/routes.py <ref/blueprints/user>` |
  :doc:`Dashboard <ref/templates/user/dashboard>` |
  :doc:`Edit profile <ref/templates/user/edit-profile>`


The REST API
============

SignBridge exposes a REST API under the ``api/`` blueprint for programmatic
access to users, rooms, and tokens.

* **Endpoint reference:**
  :doc:`Users — api/users.py <ref/api/users>` |
  :doc:`Rooms — api/rooms.py <ref/api/rooms>` |
  :doc:`Tokens — api/tokens.py <ref/api/tokens>`

* **Authentication:**
  :doc:`api/auth.py <ref/api/auth>` |
  :doc:`Bearer token usage <topics/api/auth>` |
  :doc:`Rate limiting <topics/api/rate-limiting>`

* **Error responses:**
  :doc:`api/errors.py <ref/api/errors>` |
  :doc:`Error response schema <ref/api/error-schema>`

* **How-to:**
  :doc:`Consuming the API from JavaScript <howto/api-js-client>` |
  :doc:`Adding a new endpoint <howto/add-api-endpoint>`


Real-time & calling
===================

Video calling in SignBridge is powered by WebRTC signalling over Socket.IO.
Room management logic lives in ``call/sockets.py`` and the client-side
implementation in ``static/js/call.js``.

* **Socket.IO events:**
  :doc:`call/sockets.py reference <ref/call/sockets>` |
  :doc:`Server-emitted events <ref/call/server-events>` |
  :doc:`Client-emitted events <ref/call/client-events>`

* **Rooms:**
  :doc:`call/services.py <ref/call/services>` |
  :doc:`Creating & joining rooms <topics/call/rooms>` |
  :doc:`Room lifecycle <topics/call/lifecycle>`

* **Client JavaScript:**
  :doc:`call.js <ref/static/js/call>` |
  :doc:`chat.js <ref/static/js/chat>` |
  :doc:`WebRTC signalling flow <topics/call/webrtc>`

* **Advanced:**
  :doc:`Scaling with a TURN server <howto/turn-server>` |
  :doc:`Multi-party calling <howto/multi-party>`


The sign language model
=======================

SignBridge ships with a MobileNet-based Sri Lanka Sign Language (SLSL)
classifier that runs client-side via TensorFlow.js. Model files live in
``static/models/mobilenet-slsl-1/``.

* **Overview:**
  :doc:`How the model works <topics/model/overview>` |
  :doc:`model.js walkthrough <ref/static/js/model>` |
  :doc:`class_names.json reference <ref/model/class-names>`

* **Architecture:**
  :doc:`MobileNet model architecture <topics/model/architecture>` |
  :doc:`Input preprocessing <topics/model/preprocessing>` |
  :doc:`Inference & confidence thresholds <topics/model/inference>`

* **Customisation:**
  :doc:`Swapping the model weights <howto/swap-model>` |
  :doc:`Adding new sign classes <howto/add-sign-classes>` |
  :doc:`Retraining guide <howto/retrain>`

* **Help pages:**
  :doc:`SLSL chart <ref/templates/help/slslchart>` |
  :doc:`Video tutorial page <ref/templates/help/video-tutorial>`


The admin
=========

SignBridge includes a hand-built admin dashboard (the ``admin/`` blueprint)
for managing users, rooms, and application health. It is distinct from the
REST API.

* :doc:`Admin dashboard <ref/admin/dashboard>`
* :doc:`Access control & admin-only routes <topics/admin/access>`
* :doc:`admin/utils.py <ref/admin/utils>`
* :doc:`admin/forms.py <ref/admin/forms>`


The development process
=======================

Learn about the various components and tools that support local development of
SignBridge.

* **Configuration:**
  :doc:`config.py overview <ref/config>` |
  :doc:`Environment-specific configs <topics/settings>` |
  :doc:`Full settings reference <ref/settings>`

* **App factory:**
  :doc:`app/__init__.py <ref/app-factory>` |
  :doc:`extensions.py <ref/extensions>` |
  :doc:`Blueprint registration order <topics/blueprints/registration>`

* **Logging:**
  :doc:`Logging setup <topics/logging>` |
  :doc:`Log rotation (app/logs/) <ref/logging/rotation>` |
  :doc:`Log levels & configuration <ref/logging/levels>`

* **Static files:**
  :doc:`CSS overview <ref/static/css>` |
  :doc:`JS module overview <ref/static/js>` |
  :doc:`Serving model shards <howto/serve-model-shards>`


Testing
=======

SignBridge's test suite is built with pytest, covering models, authentication
flows, the REST API, room logic, and end-to-end Selenium tests.

* **Introduction:**
  :doc:`Running the test suite <topics/testing/overview>` |
  :doc:`pytest.ini configuration <ref/testing/pytest-ini>` |
  :doc:`conftest.py <ref/testing/conftest>`

* **Test module reference:**
  :doc:`test_models.py <ref/testing/test-models>` |
  :doc:`test_auth.py <ref/testing/test-auth>` |
  :doc:`test_api.py <ref/testing/test-api>` |
  :doc:`test_rooms.py <ref/testing/test-rooms>` |
  :doc:`test_selenium.py <ref/testing/test-selenium>`

* **Advanced:**
  :doc:`Mocking Socket.IO events <howto/mock-socketio>` |
  :doc:`Testing the ML model integration <howto/test-ml>` |
  :doc:`CI pipeline setup <howto/ci>`


Deployment
==========

* **Overview:**
  :doc:`Deployment overview <howto/deployment/index>` |
  :doc:`Pre-deployment checklist <howto/deployment/checklist>`

* **WSGI:**
  :doc:`wsgi.py reference <ref/wsgi>` |
  :doc:`Gunicorn configuration <howto/deployment/gunicorn>` |
  :doc:`Nginx as reverse proxy <howto/deployment/nginx>`

* **Socket.IO:**
  :doc:`Deploying with eventlet / gevent <howto/deployment/async>` |
  :doc:`Sticky sessions behind a load balancer <howto/deployment/sticky-sessions>`

* **Static assets:**
  :doc:`Serving model shards efficiently <howto/serve-model-shards>` |
  :doc:`CDN configuration <howto/deployment/cdn>`

* **Database:**
  :doc:`PostgreSQL setup <howto/deployment/postgres>` |
  :doc:`Running migrations in production <howto/deployment/migrations>`


Security
========

Security is highly important in a real-time video application, and
SignBridge provides several layers of protection.

* :doc:`Security overview <topics/security>`
* :doc:`CSRF protection with Flask-WTF <topics/security/csrf>`
* :doc:`Password hashing <topics/security/passwords>`
* :doc:`Token expiry & revocation <topics/security/tokens>`
* :doc:`Secure WebRTC signalling <topics/security/webrtc>`
* :doc:`Protecting the admin blueprint <topics/security/admin>`


The SignBridge open-source project
===================================

Learn about the development process for SignBridge itself and how you can
contribute.

* **Community:**
  :doc:`Contributing to SignBridge <internals/contributing>` |
  :doc:`Code of conduct <internals/conduct>` |
  :doc:`Security policy <internals/security>` |
  `GitHub repository <https://github.com/nuhaaaaaaa24/SignBridge>`_

* **Design:**
  :doc:`Architecture overview <internals/architecture>` |
  :doc:`ERD diagram <ref/erd>` |
  :doc:`Design philosophy <misc/design-philosophy>`

* **Documentation:**
  :doc:`About this documentation <internals/contributing/writing-documentation>`

* **SignBridge over time:**
  :doc:`API stability <misc/api-stability>` |
  :doc:`Release notes <releases/index>` |
  :doc:`Changelog <releases/changelog>`


Contents
--------

.. toctree::
   :maxdepth: 1

   installation
   info
   dataset
   security