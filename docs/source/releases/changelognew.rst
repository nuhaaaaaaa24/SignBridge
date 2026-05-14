Changelog
=========

Unreleased
----------

Added
~~~~~
- Added user names to transcript display during calls
- Added email template documentation under authentication
- Added CSRF error handler
- Added password reset token documentation
- Added account deletion functionality

Updated
~~~~~~~
- Updated authentication flow documentation (``auth/flows.rst``)
- Updated requirements


Version 0.4.12
--------------

Notes
~~~~~
- Version bump release


Version 0.4.11
--------------

Added
~~~~~
- Added TURN server integration for improved call reliability
- Added ability to change profile picture
- Added privacy notice page
- Added confirmation dialog before leaving calls or sessions
- Added database-level constraint for blocking users
- Added block cooldown mechanism
- Added Sphinx documentation themes
- Added developer documentation: authentication overview, auth flow, password reset, tokens, CSS reference, template overview
- Added updated AI recognition model
- Added SLSL chart and video tutorial pages to documentation
- Added last seen tracking for users

Updated
~~~~~~~
- Updated CSS styling
- Updated edit profile page to display current user details
- Updated landing page layout
- Updated navbar
- Updated security documentation and ERD
- Updated config and environment variables
- Updated authentication flow documentation with password complexity, DB validation, and reCAPTCHA details
- Updated token documentation with auto-renewal logic
- Cleaned up startup files

Fixed
~~~~~
- Fixed email bugs
- Fixed call layout issue
- Fixed index changes
- Fixed typos in documentation


Version 0.4.7
-------------

Added
~~~~~
- Required login for the call route
- Required login for the join route
- Removed hardcoded reCAPTCHA values

Fixed
~~~~~
- Fixed room code field HTML error message UI
- Fixed reset password HTML error message UI
- Fixed reset password request HTML error message UI
- Fixed login page error message UI
- Fixed edit profile error message UI
- Fixed registration error message UI


Version 0.4.6
-------------

Added
~~~~~
- Added account deletion page
- Added negative training model
- Replaced waiting room spinner with progress bar


Fixed
~~~~~
- Fixed layout issues


Version 0.4.5
-------------

Added
~~~~~
- Added responsive web design
- Switched to updated TensorFlow.js model

Updated
~~~~~~~
- Updated help and video tutorial pages
- Updated section title colours

Fixed
~~~~~
- Fixed typo in edit profile; updated button styling

Version 0.4.4
-------------

Notes
~~~~~
- Version bump release


Version 0.4.3
-------------

Added
~~~~~
- Implemented Google reCAPTCHA v2 bot protection on all authentication forms


Version 0.4.2
-------------

Added
~~~~~
- Added documentation folder (``docs/``)

Fixed
~~~~~
- Fixed create new session button UI
- Fixed flash toast messages
- Removed unused files; merged prior repository history


Version 0.4.1
--------------

Fixed
~~~~~
- Fixed database issues


Version 0.4.0
--------------

Added
~~~~~
- Redesigned and integrated responsive frontend UI across the Flask/Jinja application
- Added authenticated user dashboard for post-login navigation
- Added user dropdown navigation menu with profile, dashboard, admin access, and logout
- Added admin dashboard interface for user management and room monitoring
- Added profile editing UI improvements including avatar support groundwork
- Added video tutorial error placeholder and fallback handling
- Added Bootstrap icon controls for microphone and camera toggling in call interface
- Added improved real-time chat bubble styling and empty-state behavior
- Added transcript and chat scrolling support during calls
- Added visual mute/unmute and camera off indicators

Updated
~~~~~~~
- Updated base template structure and shared partials (navbar/footer)
- Updated authentication flow to redirect users to dashboard after login
- Updated home navigation behavior to allow authenticated users back to landing page
- Updated call page layout with split-panel video, transcript, recognition, and chat interface
- Updated waiting room experience and call control styling
- Updated contact, help, about, dashboard, profile and auth page layouts
- Updated responsive navigation including mobile menu and user dropdown behavior
- Updated chat styling to use CSS-based bubble components instead of hardcoded inline styles
- Updated recognition panel and transcript presentation during live calls
- Updated overall visual theme, spacing, card system, and reusable component styling

Fixed
~~~~~
- Fixed call sidebar layout causing chat and detection panels to appear below transcript
- Fixed missing dropdown functionality for authenticated navigation
- Fixed chat placeholder persistence after messages begin
- Fixed transcript/chat overflow issues by adding scrollable panels
- Fixed oversized icons and image scaling issues in help/about pages
- Fixed video placeholder overlay interfering with participant video rendering
- Fixed navbar route mismatches and template integration issues
- Fixed Bootstrap mic/camera toggle states and muted visual feedback

Refactored
~~~~~~~~~~
- Refactored CSS into reusable shared components and cleaner structure
- Refactored frontend templates to align redesigned UI with backend routes and Jinja logic
- Refactored call page controls and supporting JavaScript interactions


Version 0.3.15
--------------

Updated
~~~~~~~
- Added logs to ``.gitignore``
- Updated config


Version 0.3.14
--------------

Added
~~~~~
- Implemented Redis-based rate limiter
- Added in-call menu with mute audio and video controls
- Added timeout, rate limit updates, and security headers
- Added user profile button improvements

Fixed
~~~~~
- Fixed edit profile page
- Fixed rate limiting login — restricted lockout message to login route; kept generic slow-down message for other paths
- Fixed deployment not using PostgreSQL
- Fixed database relationship issues
- Fixed minor bugs and restored missing files

Updated
~~~~~~~
- Improved security policies: minimum password length increased to 12 characters, client-side validation updated, admin accounts exempted from auto-blocking, admin contact email added to block message
- Migrated to new PostgreSQL database
- Updated tests


Version 0.3.9
-------------

Fixed
~~~~~
- Minor bugfixes
- Added back missing files


Version 0.3.10
-------------

- Fixed IP address issue with limiter on Render deployment
- Miscellaneous bug fixes for Render deployment

Version 0.3.9
-------------

- Added Sphinx for documentation
- Added base documentation folder and code

Version 0.3.8
-------------

- Added code for Render deployment build
- Miscellaneous bug fixes

Version 0.3.7
-------------

- Miscellaneous bug fixes

Version 0.3.6
-------------

- Miscellaneous bug fixes

Version 0.3.5
-------------

- Miscellaneous bug fixes

Version 0.3.4
-------------

- Miscellaneous bug fixes

Version 0.3.3
-------------

- Fixed syntax errors and routing issues
- Fixed rate limits not triggering at all
- General bug fixes

Version 0.3.2
--------------

- Added function to specify the development server link
- Updated requirements.txt

Version 0.3.1
--------------

- Removed extraneous files

Version 0.3.0
-------------

* Refactored all code to fit Flask best practices
* All html files now use Jinja templating - they inherit from base.html, with additional code as needed.
* app.py has been removed and its code aggressively modularized. Parts of it can be found in __init__.py, handlers.py, routes.py, signbridge.py... you get the idea. Not an exhaustive list. Please read all the files.
* Most JavaScript has been removed and replaced with server-side Python code.
* On that note, app.js and main.js have been removed.
* Routes are in routes.py
* HTTP errors are in /app/errors/handlers.py
* forms.py handles forms server-side. Check the respective html files for front-end side.
* Database stuff is in /app/models.py
* Websocket stuff is in /app/sockets.py
* Room code generation has been moved to /app/services.py
* Database uses the SQLAlchemy package instead of SQLite3 (well it still uses SQLite in the database but can be converted to PostgreSQL fairly easily now)
* profile.html has been renamed to user.html
* landing.html has been renamed to join.html
* Landing page is now index.html 
* waiting.html has been removed and its code integrated into call.html 
* new rooms are created in profile
* Added secret key (check config.py) to protect forms against cross-site request forgery (CSRF) attacks
* Username, email and password validation should work correctly now
* Passwords are hashed with PBKDF2 - change to bcrypt if required
* Added session authentication
* Changed contact phone number to Dulitha's because it's funny
* Database has been updated to include additional tables for messages and transcripts
* Added support for profile pictures via Gravatar.
* Added email support for admins
* Added logging capabilities. Logs are saved to /logs/signbridge.log
* Users can now reset their passwords via email.
* Added tests.py for testing capabilities. Will add dummy tests soon.
* Added rate limiting back into the app (for some reason it disappeared in the last version on GitHub). Thanks Dulneth!
* Added webcam and microphone support
* Fixed layout issues in call.html

Version 0.2.4
-------------

- Added error page HTML
- Updated help page and miscellaneous HTML files


Version 0.2.3
-------------

- Added profile page
- Added logout page
- Added contact page backend code
- Cleaned up code for readability

Version 0.2.2
-------------

- Re enhanced password validation: require uppercase, lowercase, 
numbers, and special characters with real time visual feedback
- Added password confirmation field to prevent typos, implement 
frontend/backend password validation, Added specific error msgs for 
existing username/email, enforce minimum 6 character password length

Version 0.2.1
-------------

- Fixed login and registration routing issues

Version 0.2.0
-------------

- Updated login and register UI pages
- Fixed registration issues in app.js


Version 0.1.4
-------------

- Fixed missing routes for help, video tutorial and SLSL chart pages.

Version 0.1.3
-------------

- Added rate limiting using Flask-Limiter 
- General security improvements


Version 0.1.2
-------------

- Added registration, login, and room backend
- Added SQLite database

Version 0.1.1
-------------

- Added SLSL chart page
- Added video tutorial page
- Updated help page

Version 0.1.0
-------------

- First functional prototype
