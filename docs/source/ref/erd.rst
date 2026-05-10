Entity Relationship Diagram
============================

.. image:: ../../../app/static/images/erd_diagram.PNG
   :alt: Entity Relationship Diagram

Overview
--------

The diagram models a real-time chat application with five core entities: **User**, **Room**, **RoomParticipant**, **messages**, and **transcript**.

Entities and Relationships
--------------------------

**User**
   Stores registered user accounts with fields: ``user_id`` (PK), ``username``, ``email``, and ``password``.

**Room**
   Represents a chat room, identified by ``room_id`` (PK), along with ``created_at`` and ``owner_id`` (FK links to User). Each room is owned by exactly one user, but a user can own many rooms.

**RoomParticipant**
   A junction table linking users to rooms. Fields: ``user_room_id`` (PK), ``user_id`` (FK links to User), and ``room_id`` (FK links to Room). A room can have many participants, and a user can join many rooms (many-to-many relationship resolved through this table).

**messages**
   Holds individual chat messages with fields: ``message_id`` (PK), ``content``, ``time``, ``user_id`` (FK links to User), and ``room_id`` (FK links to Room). Each message belongs to one user and one room; a room and user can each have many messages.

**transcript**
   Stores a compiled or saved transcript for a room, with fields: ``transcript_id`` (PK), ``room_id`` (FK links to Room), ``content``, and ``created_at``. A room can have zero or many transcripts.

Key Relationships Summary
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - From
     - To
     - Relationship
   * - User
     - Room
     - One user owns zero or many rooms
   * - User
     - RoomParticipant
     - One user participates in zero or many rooms
   * - Room
     - RoomParticipant
     - One room has one or many participants
   * - User
     - messages
     - One user sends zero or many messages
   * - Room
     - messages
     - One room contains zero or many messages
   * - Room
     - transcript
     - One room has zero or many transcripts