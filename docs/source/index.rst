.. SignBridge documentation master file, created by
   sphinx-quickstart on Mon Apr 27 11:56:40 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==========================
SignBridge Documentation
==========================

Welcome! This is the official documentation for SignBridge.

.. _index-first-steps:

First steps
===========

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: From scratch
      :link: intro/installation
      :link-type: doc

      Get started and set up your environment.

   .. grid-item-card:: Requirements
      :link: intro/requirements
      :link-type: doc

      Learn all available settings and options.

   .. grid-item-card:: Configuration
      :link: intro/requirements
      :link-type: doc

      Learn all available settings and options.

   .. grid-item-card:: Tutorial
      :link: intro/tutorial01
      :link-type: doc

      Walk through a hands-on example step by step.

Getting help
============

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: FAQ
      :link: faq/index
      :link-type: doc

      Find answers to common questions about the application.

   .. grid-item-card:: Detailed contents
      :link: contents
      :link-type: doc

      Browse the complete documentation structure and references.

Models
======

SignBridge uses Flask-SQLAlchemy with a single ``models.py`` to define the
data layer, and Flask-Migrate to manage schema evolution against a PostgreSQL
database.

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Model Introduction
      :link: topics/db/models
      :link-type: doc

      Learn how models are structured and used in the application.

   .. grid-item-card:: ERD Diagram
      :link: ref/misc/erd
      :link-type: doc

      View the entity relationship diagram for the database schema.

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Flask-Migrate Introduction
      :link: topics/migrations
      :link-type: doc

      Learn how database migrations work with Flask-Migrate.

   .. grid-item-card:: Running migrations
      :link: howto/run-migrations
      :link-type: doc

      Step-by-step guide for creating and applying migrations. 

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: PostgreSQL Configuration
      :link: ref/databases/postgres
      :link-type: doc

      Configure PostgreSQL for production and deployment environments.

   .. grid-item-card:: SQLite for Local Development
      :link: ref/databases/sqlite
      :link-type: doc

      Use SQLite for lightweight local development and testing.

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Seeding Initial Data
      :link: howto/initial-data
      :link-type: doc

      Populate the database with default or sample application data.

   .. grid-item-card:: SQLAlchemy Queries
      :link: topics/db/queries
      :link-type: doc

      Learn how to create and execute queries using SQLAlchemy.



Blueprints
==============

SignBridge has the concept of *blueprints* to encapsulate the logic
responsible for processing a user's request and returning a response. The
application is divided into the following blueprints: ``main``, ``auth``,
``call``, ``user``, ``admin``, ``help``, and ``errors``.

* **Blueprint reference:**
  :doc:`main <ref/blueprints/main>` |
  :doc:`auth <ref/blueprints/auth>` |
  :doc:`call <ref/blueprints/call>` |
  :doc:`user <ref/blueprints/user>` |
  :doc:`admin <ref/blueprints/admin>` |
  :doc:`help <ref/blueprints/help>` |
  :doc:`error <ref/blueprints/errors>` 


Templates
=========

The template layer provides a Jinja2-based syntax for rendering the
information to be presented to the user. SignBridge templates are organised
around a shared ``base.html`` and blueprint-specific subdirectories.

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Template Overview
      :link: topics/templates
      :link-type: doc

      Learn the basics of working with templates in the application.

   .. grid-item-card:: styles.css Reference
      :link: ref/static/css
      :link-type: doc

      Explore the available CSS styles and design utilities.


Forms
=====

SignBridge uses Flask-WTF for all form handling, with form classes defined in
each blueprint's ``forms.py`` module.

* **Form class reference:**
  :doc:`auth/forms.py <ref/auth/forms>` |
  :doc:`call/forms.py <ref/call/forms>` |
  :doc:`user/forms.py <ref/user/forms>` |
  :doc:`main/forms.py <ref/main/forms>` |
  :doc:`admin/forms.py <ref/admin/forms>`

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

The REST API
============

SignBridge exposes a REST API under the ``api/`` blueprint for programmatic
access to users, rooms, and tokens.

* **Endpoint reference:**
  :doc:`API endpoint reference <ref/api/index>`

* **Authentication:**
  :doc:`Authentication <topics/api>`

* **How-to:**
  :doc:`How-to guides <howto/api>`

The sign language model
=======================

SignBridge ships with a MobileNet-based Sri Lanka Sign Language (SLSL)
classifier that runs client-side via TensorFlow.js. Model files live in
``static/models/``.

* **Overview:**
  :doc:`How the model works <topics/model/overview>`

* **Architecture:**
  :doc:`MobileNet model architecture <topics/model/architecture>` |
  :doc:`Input preprocessing <topics/model/preprocessing>` |
  :doc:`Inference & confidence thresholds <topics/model/inference>`

* **Customisation:**
  :doc:`Adding new sign classes <howto/add-sign-classes>` |
  :doc:`Retraining guide <howto/retrain>`

* **Help pages:**
  :doc:`SLSL chart <ref/templates/help/slslchart>` |
  :doc:`Video tutorial page <ref/templates/help/video-tutorial>`

The development process
=======================

Learn about the various components and tools that support local development of
SignBridge.

* **Configuration:**
  :doc:`config.py overview <ref/misc/config>` |

* **App factory:**
  :doc:`app/__init__.py <ref/misc/app-factory>` |
  :doc:`extensions.py <ref/misc/extensions>` 

* **Logging:**
  :doc:`Logging setup <topics/logging>` 

* **Static files:**
  :doc:`CSS overview <ref/static/css-overview>` |
  :doc:`JS module overview <ref/static/js>`

Testing
=======

SignBridge's test suite is built with pytest, covering models, authentication
flows, the REST API, room logic, and end-to-end Selenium tests.

* **Introduction:**
  :doc:`Running the test suite <topics/testing/overview>` |
  :doc:`conftest.py <ref/testing/conftest>`

* **Test module reference:**
  :doc:`test_models.py <ref/testing/test-models>` |
  :doc:`test_auth.py <ref/testing/test-auth>` |
  :doc:`test_api.py <ref/testing/test-api>` |
  :doc:`test_rooms.py <ref/testing/test-rooms>` |
  :doc:`test_selenium.py <ref/testing/test-selenium>`

Deployment
==========

* **Overview:**
  :doc:`Deployment overview <howto/deployment/index>` |
  :doc:`Pre-deployment checklist <howto/deployment/checklist>`

* **WSGI:**
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

* :doc:`Security overview <topics\security>`
* :doc:`CSRF protection with Flask-WTF <topics/security/csrf>`
* :doc:`Password hashing <topics/security/passwords>`

Indices and Search
==================

* :ref:`genindex`
* :ref:`modindex`

The SignBridge project
======================

* **Design:**
  :doc:`Architecture overview <internals/architecture>` |
  :doc:`ERD diagram <ref/misc/erd>` |
  `GitHub repository <https://github.com/nuhaaaaaaa24/SignBridge>`_

* **SignBridge over time:**
  :doc:`Changelog <releases/changelog>` |
  :doc:`About this documentation <internals/documentation>`

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Getting Started

   intro/overview
   intro/installation
   intro/requirements
   ref/misc/config
   ref/index

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Tutorials

   intro/tutorial01

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Models

   topics/db/models
   topics/migrations
   topics/db/queries
   ref/misc/erd
   ref/databases/postgres
   ref/databases/sqlite
   howto/run-migrations
   howto/initial-data

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Blueprints

   ref/blueprints/auth
   ref/blueprints/admin
   ref/blueprints/call
   ref/blueprints/errors
   ref/blueprints/help
   ref/blueprints/main
   ref/blueprints/user

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: REST API

   ref/api/index
   topics/api
   howto/api

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Development

   ref/misc/app-factory
   ref/misc/extensions
   topics/logging

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Security & Changes

   topics/security
   releases/changelog

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Project Info

   info
   dataset
   security
   internals/architecture
   faq/index
   contents