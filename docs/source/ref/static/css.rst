=====================
Styles.css References
=====================

Overview
========

The ``styles.css`` file contains the primary styling rules used 
throughout the SignBridge web application.

The stylesheet is responsible for defining:

* page layouts
* typography
* colour themes
* spacing and alignment
* responsive behaviour
* reusable user interface components

The design focuses on simplicity, accessibility, responsiveness and 
maintainability.

Design Goals
============

The frontend styling was designed with the following goals:

* provide a clean and modern interface
* maintain consistent layouts across pages
* support responsive web design
* improve usability and readability
* create familiarity through video-conferencing inspired layouts

Responsive Design
=================

The application uses responsive web design techniques to support multiple 
screen sizes and device orientations.

Media queries are used to adapt layouts for:

* desktop devices
* tablets
* mobile devices
* portrait orientation
* landscape orientation

Responsive adjustments include:

* resizing navigation elements
* stacking layout components vertically on smaller screens
* adjusting spacing and typography
* resizing video containers and transcript panels

Reusable Components
===================

The stylesheet contains reusable styles for common interface elements.

Examples include:

* buttons
* forms
* cards
* navigation bars
* transcript containers
* video panels
* dropdown menus
* modal components

Using reusable styles improves consistency and reduces duplicated CSS rules.

Colour Palette
==============

The SignBridge frontend primarily uses the following colour palette:

.. list-table::
   :header-rows: 1
   :widths: 30 30
   
   * - Purpose
     - Colour Code
   * - Primary Blue-Grey
     - ``#3A5673``
   * - Dark Accent
     - ``#444B54``
   * - Background
     - ``#F2F2F2``

These colours were selected to create a clean, professional, and accessible
visual identity.

Typography
==========

Typography styles are designed to improve readability and visual hierarchy.

The stylesheet defines:

* heading styles
* body text styles
* button text
* spacing between sections
* responsive font sizing

Larger headings and spacing are used to guide user attention throughout the
application.

Layout System
=============

The frontend layout primarily uses:

* Flexbox
* CSS Grid
* responsive containers

These layout systems help organise components such as:

* video call panels
* transcript displays
* profile cards
* help page content
* navigation structures

Accessibility
=============

The stylesheet includes accessibility-focused design decisions such as:

* sufficient colour contrast
* large clickable buttons
* clear form labels
* responsive text sizing
* consistent navigation structure

The interface was designed to remain simple and easy to understand for users
with varying levels of technical experience.

Maintainability
===============

The stylesheet is organised to improve maintainability and scalability.

Reusable classes and modular sections help reduce duplicated styling rules and
make future frontend updates easier to manage.


The ``styles.css`` file provides the visual foundation of the SignBridge
frontend and supports a consistent, responsive, and user-friendly interface.