====================
styles.css Reference
====================

Overview
========

The ``styles.css`` file contains the primary styling rules used throughout the
SignBridge web application.

The stylesheet defines the visual appearance and responsive behaviour of the
frontend interface, including layouts, typography, forms, navigation elements,
video communication panels, transcript displays, and reusable user interface
components.

The styling system was designed to support a clean, modern, responsive, and
maintainable frontend architecture.

Design Goals
============

The frontend styling was developed according to the following design goals:

* maintain a clean and modern visual appearance
* support responsive web design across multiple devices
* improve usability and readability
* maintain consistent layouts and spacing
* create familiarity through video-conferencing inspired interfaces
* simplify future frontend maintenance and updates

The overall visual style combines modern SaaS-inspired layouts with soft
glassmorphism elements and accessibility-focused design principles.

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

The frontend layout primarily uses:

* Flexbox
* CSS Grid
* responsive containers

These layout systems help organise interface components such as:

* video communication interfaces
* transcript displays
* profile cards
* dashboard layouts
* help page content
* navigation structures

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
duplicated CSS rules throughout the application.

Colour Palette
==============

The SignBridge frontend primarily uses the following colour palette:

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - Purpose
     - Colour

   * - Primary Accent
     - |primary|
       Warm coral (``#E88D67``)

   * - Secondary Accent
     - |secondary|
       Dusty blue-grey (``#92BCCD``)

   * - Main Text
     - |text|
       Deep teal navy (``#0B3041``)

   * - Danger Accent
     - |danger|
       Berry red (``#B03051``)

   * - Background
     - |background|
       Soft off-white blue (``#F7F8FC``)

.. |primary| raw:: html

   <span style="display:inline-block;width:16px;height:16px;background:#E88D67;border:1px solid #000;margin-right:8px;"></span>

.. |secondary| raw:: html

   <span style="display:inline-block;width:16px;height:16px;background:#92BCCD;border:1px solid #000;margin-right:8px;"></span>

.. |text| raw:: html

   <span style="display:inline-block;width:16px;height:16px;background:#0B3041;border:1px solid #000;margin-right:8px;"></span>

.. |danger| raw:: html

   <span style="display:inline-block;width:16px;height:16px;background:#B03051;border:1px solid #000;margin-right:8px;"></span>

.. |background| raw:: html

   <span style="display:inline-block;width:16px;height:16px;background:#F7F8FC;border:1px solid #000;margin-right:8px;"></span>

These colours were selected to create a calm, professional, and accessible
visual identity suitable for a communication-focused application.

Typography
==========

Typography styles are designed to improve readability and visual hierarchy.

The stylesheet defines styling for:

* headings
* body text
* navigation links
* form labels
* button text
* responsive font sizing

Larger headings and consistent spacing are used to guide user attention
throughout the application interface.

Accessibility
=============

The stylesheet includes accessibility-focused design considerations such as:

* sufficient colour contrast
* responsive scaling
* clear typography hierarchy
* readable spacing and alignment
* large clickable buttons
* consistent navigation structure

The interface was designed to remain simple and easy to understand for users
with different levels of technical experience.

Glassmorphism Styling
=====================

Several interface components use soft glassmorphism-inspired styling through:

* semi-transparent surfaces
* backdrop blur effects
* layered shadows
* soft borders
* translucent containers

Examples include:

* navigation bars
* profile cards
* dashboard cards
* transcript panels
* help page cards
* modal containers

This styling approach helps create visual depth while maintaining a clean and
minimal user interface.

Maintainability
===============

The stylesheet is organised using reusable classes and modular sections to
improve maintainability and scalability.

Separating styling from template structure simplifies frontend development and
helps reduce duplicated styling rules throughout the application.

Reusable utility classes and shared component styles also support easier future
frontend updates and interface redesigns.