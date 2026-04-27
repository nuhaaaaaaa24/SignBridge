Dataset Documentation
======================


Overview
--------

This dataset was created to support the development of a real-time gesture recognition system for Sri Lankan Sign Language (SLSL).

The dataset focuses on a subset of 10 static hand gesture letters: **A, E, I, O, U, L, N, R, S, T**.

As no suitable public dataset was available for this specific use case, a custom dataset was collected and curated.


Dataset Structure
------------------

The dataset is organised into class-based directories, where each folder represents a gesture class (letter).

.. code-block:: text

   dataset/
   ├── A/
   │   ├── A001.jpg
   │   ├── A002.jpg
   ├── E/
   │   ├── E001.jpg
   │   ├── E002.jpg
   ├── I/
   │   ├── I001.jpg
   │   ├── I002.jpg
   ├── O/
   │   ├── O001.jpg
   │   ├── O002.jpg

Each folder contains images that correspond to a single gesture.


Dataset Composition
-------------------

- Number of letters: 10  
- Letters included: A, E, I, O, U, L, N, R, S, T  
- Total number of images: 456  

The dataset is approximately balanced with each class containing a similar number of images.


Dataset Summary
---------------

+--------+-------------+
| Letter | Image Count |
+========+=============+
| A      | 45          |
+--------+-------------+
| E      | 45          |
+--------+-------------+
| I      | 46          |
+--------+-------------+
| O      | 45          |
+--------+-------------+
| U      | 44          |
+--------+-------------+
| L      | 47          |
+--------+-------------+
| N      | 47          |
+--------+-------------+
| R      | 47          |
+--------+-------------+
| S      | 45          |
+--------+-------------+
| T      | 45          |
+--------+-------------+


Data Collection
---------------

Images were collected using standard smartphone cameras.

To improve dataset diversity and model generalisation, images were captured under varying conditions:

- Lighting: natural light, indoor lighting, and low-light environments
- Backgrounds: plain and cluttered backgrounds
- Angles: slight variations in hand orientation
- Participants: multiple individuals with different hand sizes and skin tones


File Naming
------------

All images follow a consistent naming format:

``LETTER+NUMBER.jpg``

- **LETTER** corresponds to the class label  
- **NUMBER** is a sequential identifier  

Examples:

.. code-block:: text

   A001.jpg
   E012.jpg

Images were converted to `.jpg` format using ImageMagick.


Usage
-----

This dataset is intended for use in image classification tasks related to sign language gesture recognition.

It can be used to:

- Train machine learning models for gesture classification
- Evaluate model performance on static hand gestures
- Develop and test real-time sign language recognition systems


Ethical Considerations
----------------------

- No personally identifiable information is included
- Only hand gesture images were collected
- Participation was voluntary
- Data is used strictly for academic purposes


Limitations
-----------

- Dataset size is relatively small (456 images total)
- Only a subset of letters is included
- Static gestures only
- Slight class imbalance between letters
- Environmental conditions may affect model performance
- Regional variations in SLSL are not fully represented


Future Improvements
-------------------

- Expand dataset to include the full alphabet
- Increase dataset size and diversity
- Include dynamic hand gestures
- Collect data from multiple regions
- Improve variation in environmental conditions