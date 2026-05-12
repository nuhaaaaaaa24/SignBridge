====================
styles.css Reference
====================

Overview
========

The ``styles.css`` file contains the primary styling rules used throughout the
SignBridge web application.

The stylesheet defines the visual appearance and responsive behaviour of the
frontend interface, including layouts, typography, forms, navigation elements,
video communication panels, transcript sections, and reusable user interface
components.

The styling system was designed to support a clean, responsive, accessible,
and maintainable frontend architecture.

Design Goals
============

The frontend styling was developed according to the following design goals:

* maintain a clean and modern visual appearance
* support responsive web design across multiple devices
* improve usability and readability
* maintain consistent layouts and spacing
* create familiarity through video-conferencing inspired interfaces
* simplify future frontend maintenance and updates

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

Responsive behaviour includes:

* resizing navigation components
* stacking layouts vertically on smaller screens
* resizing transcript panels and video containers
* adjusting typography and spacing for readability
* reorganising interface sections for smaller displays

Reusable Components
===================

The stylesheet contains reusable styles for commonly used interface elements.

Examples include:

* buttons
* forms
* cards
* navigation bars
* dropdown menus
* transcript panels
* video communication containers
* flash messages
* modal components

Reusable styling helps maintain consistency across templates and reduces
duplicated CSS rules.

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

The stylesheet defines styling for:

* headings
* body text
* buttons
* navigation links
* form labels
* responsive text sizing

Larger headings and spacing are used to guide user attention throughout the
application interface.

Layout System
=============

The frontend layout primarily uses:

* Flexbox
* CSS Grid
* responsive containers

These layout systems are used to organise components such as:

* video call interfaces
* transcript displays
* profile cards
* dashboard layouts
* help page content
* navigation structures

Accessibility
=============

The stylesheet includes accessibility-focused design considerations such as:

* sufficient colour contrast
* large clickable buttons
* clear typography hierarchy
* responsive scaling
* consistent navigation structure
* readable spacing and alignment

The frontend interface was designed to remain simple and easy to understand
for users with different levels of technical experience.

Maintainability
===============

The stylesheet is organised using reusable classes and modular sections to
improve maintainability and scalability.

Separating styling from template structure simplifies frontend development and
helps reduce duplicated styling rules throughout the application.

The ``styles.css`` file provides the visual foundation of the SignBridge
frontend and supports a responsive, accessible, and user-friendly interface.