Changelog
=========

Version 0.4.18
--------------

- Added js Module Overview documentation
- Added Deployment Documentation
- Cleaned up CSS file and rewrote comments
- Updated the video tutorial and user guide links

Version 0.4.15
--------------

- Added call guard. 

Version 0.4.14
--------------

- Miscellaneous bug fixes (user account deletion)

Version 0.4.13
--------------

- Added user account deletion flow

Version 0.4.12
--------------

- Updated login decorator in JS to support guest call access
- Added restriction to prevent blocked users from becoming admins
- Reduced the number of TURN servers used
- Added CSRF error handler

Version 0.4.11
--------------

- Added privacy notice popup explaining that video processing happens locally.
- Removed the login requirement from the Join Session route to allow guest joining.
- Updated landing page content and feature presentation.
- Added confirmation prompts before leaving calls or cancelling sessions.
- Updated edit profile page to show current user details.
- Added Gravatar-based profile picture editing.
- Fixed spacing around the delete account button.

Version 0.4.10
--------------

- Cleaned up startup files
- Updated and refined the main CSS styling.
- Added the SLSL chart page documentation.
- Added the video tutorial page documentation.
- Updated navbar layout and behavior.
- Added CSS overview documentation.

Version 0.4.9
-------------

- Added TURN server
- Improved UI formatting and reduced font size for form validation error messages.
- Secured `/join` and `/call` endpoints by enforcing user login requirements.
- Enhanced security by removing hardcoded reCAPTCHA keys from the source code and migrating them to environment variables.

Version 0.4.8
-------------

- Modified config.py
- Fixed email bugs
- Added template overview documentation.
- Added `styles.css` reference documentation.

Version 0.4.7
-------------

- Required login for the call route
- Required login for the join route
- Removed hardcoded reCAPTCHA values
- Fixed room code field HTML error message UI
- Fixed reset password HTML error message UI
- Fixed reset password request HTML error message UI
- Fixed login page error message UI
- Fixed edit profile error message UI
- Fixed registration error message UI

Version 0.4.6
-------------

- API tokens now auto-renew when less than 60 seconds remain on expiry (model.py)
- Added Sphinx autobuild for Developer Documentation
- Replaced the waiting room spinner with a progress bar.
- Created the account deletion request page.
- Made layout fixes and responsive UI improvements.
- Miscellaneous bug fixes
- Modified config.py

Version 0.4.5
-------------

- Switched to updated TensorFlow.js model
- Fixed a typo.
- Updated the Edit Profile page button styling.
- Improved and reorganized the Help page layout.
- Updated the Help and Video Tutorial pages with revised content and navigation improvements.
- Applied consistent section title colour styling across the Admin Dashboard and Profile.
- Improved responsive web design for better compatibility across desktop, and mobile devices.
- Changed waiting room spinner to progress bar

Version 0.4.4
-------------

- Display peer username on remote video

Version 0.4.3
-------------

- Integrated Google reCAPTCHA v2 ("I'm not a robot") for bot protection.
- Added reCAPTCHA validation to the user registration and Login forms.
- Configured secure API key handling via Environment Variables for deployment.

Version 0.4.2
-------------

- Modified documentation folder
- Moved transcript logic to sockets.py
- Fixed create new session button and toast messages

Version 0.4.1
--------------

- Fixed database issues

Version 0.4.0
--------------

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
- Fixed call sidebar layout causing chat and detection panels to appear below transcript
- Fixed missing dropdown functionality for authenticated navigation
- Fixed chat placeholder persistence after messages begin
- Fixed transcript/chat overflow issues by adding scrollable panels
- Fixed oversized icons and image scaling issues in help/about pages
- Fixed video placeholder overlay interfering with participant video rendering
- Fixed navbar route mismatches and template integration issues
- Fixed Bootstrap mic/camera toggle states and muted visual feedback
- Refactored CSS into reusable shared components and cleaner structure
- Refactored frontend templates to align redesigned UI with backend routes and Jinja logic
- Refactored call page controls and supporting JavaScript interactions

Version 0.3.19
--------------

- Added Selenium tests

Version 0.3.18
--------------

- Added bearer tokens so at registration the tokens are generated for each user
- Removed the 'View owned rooms' button in profile because it clutters the UI and we are not really implementing joining back or viewing messages.
- Migration added for User Tokens
- Added logs to gitignore

Version 0.3.17
--------------

- Added 30-minute inactivity logout using PERMANENT_SESSION_LIFETIME
- Enforced moving-window strategy with strict 60-second rate limit blocks
- Added JS to disable submit buttons during rate-limit triggers.
- Added security headers: HSTS, X-Frame-Options, X-Content-Type-Options.
- Improved error handler redirects to keep users on the same page for button locking

Version 0.3.16
--------------

- Added test suite configuration

Version 0.3.15
--------------

- Added menu inside call, mute audio and video
- Modified user profile button UI

Version 0.3.14
--------------
- Fix edit_profile and fixed rate limiting login
- restrict login lockout msg to login route and keep generic slow down msg for other paths

Version 0.3.13
--------------

- Improved security policies by increasing minimum password length to 12 characters, updating client-side validation, exempting admin accounts from auto-blocking, adding admin contact email to block acc msg.

Version 0.3.12
--------------

- Fixed database bugs - deleting users would orphan other records.
- Miscellaneous bug fixes 

Version 0.3.11
--------------

- Migrated Render deployment to new PostgreSQL database
- Created a default email - admin.signbridge@gmail.com
- Added email support to the contact page
- Added admin dashboard
- Added user id-based rate limiting
- Added user autoblock after too many failed login attempts. Currently requires an admin to unblock
- Fixed IP address issue with limiter on Render deployment
- Miscellaneous bug fixes for Render deployment


Version 0.3.10
--------------

- Added ML model files to codebase

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

- Refactored all code to fit Flask best practices
- All html files now use Jinja templating - they inherit from base.html, with additional code as needed.
- app.py has been removed and its code aggressively modularized. Parts of it can be found in __init__.py, handlers.py, routes.py, signbridge.py... you get the idea. Not an exhaustive list. Please read all the files.
- Most JavaScript has been removed and replaced with server-side Python code.
- On that note, app.js and main.js have been removed.
- Routes are in routes.py
- HTTP errors are in /app/errors/handlers.py
- forms.py handles forms server-side. Check the respective html files for front-end side.
- Database stuff is in /app/models.py
- Websocket stuff is in /app/sockets.py
- Room code generation has been moved to /app/services.py
- Database uses the SQLAlchemy package instead of SQLite3 (well it still uses SQLite in the database but can be converted to PostgreSQL fairly easily now)
- profile.html has been renamed to user.html
- landing.html has been renamed to join.html
- Landing page is now index.html 
- waiting.html has been removed and its code integrated into call.html 
- new rooms are created in profile
- Added secret key (check config.py) to protect forms against cross-site request forgery (CSRF) attacks
- Username, email and password validation should work correctly now
- Passwords are hashed with PBKDF2 - change to bcrypt if required
- Added session authentication
- Changed contact phone number to Dulitha's because it's funny
- Database has been updated to include additional tables for messages and transcripts
- Added support for profile pictures via Gravatar.
- Added email support for admins
- Added logging capabilities. Logs are saved to /logs/signbridge.log
- Users can now reset their passwords via email.
- Added tests.py for testing capabilities. Will add dummy tests soon.
- Added rate limiting back into the app (for some reason it disappeared in the last version on GitHub). Thanks Dulneth!
- Added webcam and microphone support
- Fixed layout issues in call.html

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

- Re enhanced password validation: require uppercase, lowercase, numbers, and special characters with real time visual feedback
- Added password confirmation field to prevent typos, implement frontend/backend password validation, Added specific error msgs for existing username/email, enforce minimum 6 character password length

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
