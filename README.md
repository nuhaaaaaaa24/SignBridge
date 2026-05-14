# SignBridge - Real-Time Sign Language Detection and Translation
SignBridge is a video calling application intended to aid with translating Sri Lankan Sign Language into text. It consists of a conventional two-person video call interface combined with a deep learning model that captures the camera feed and displays a text transcript in real time. 

The application is developed with Flask, HTML, CSS and JavaScript. The deep learning model is developed with Python, TensorFlow and TensorFlow.js.

The demo for this application can be viewed at https://signbridge-pzm3.onrender.com/ 

## How to run this application locally
To run this on a local development server, you will need to set the environment variables defined in config.py.

If you do not know how to do this, contact me for assistance.

<b>1) Clone the repository to your local drive:</b>

```
git clone https://github.com/nuhaaaaaaa24/SignBridge.git
```

<b>2) Navigate to the folder you just created:</b>

```
cd your/path/here/SignBridge
```

<b>3) Create a Python virtual environment.</b>

In your terminal, run the following command:

```
python3 -m venv venv
```

<b>4) Activate the virtual environment</b>

On Windows Command Prompt, run the following:

```
venv\Scripts\activate
```

On Windows PowerShell, run the following:

```
venv\Scripts\Activate.ps1
```

On MacOS, run the following:

```
source venv/bin/activate
```

On Linux, run the following:

```
source venv/bin/activate
```

<b>5) Install the required dependencies</b>

Run ONE of the following commands: 

```
pip install -r requirements.txt
```
or
```
python3 -m pip install -r requirements.txt
```

<b>6) Run the development server with the following command:</b>

```
python signbridge.py
```

<b>For Pytest</b>

```
pytest tests/ --ignore=tests/test_selenium.py -v
```

<b>For Selenium</b>

```
pytest tests/test_selenium.py -v
```

<b>Sphinx Autobuild<b>

```
sphinx-autobuild source build/html
```

## Changelog - Version 0.4.12
- Updated login decorator in JS to support guest call access
- Added restriction to prevent blocked users from becoming admins
- Reduced the number of TURN servers used

## Changelog - Version 0.4.11

- Added privacy notice popup explaining that video processing happens locally.
- Removed the login requirement from the Join Session route to allow guest joining.
- Updated landing page content and feature presentation.
- Added confirmation prompts before leaving calls or cancelling sessions.
- Updated edit profile page to show current user details.
- Added Gravatar-based profile picture editing.
- Fixed spacing around the delete account button.

## Changelog - Version 0.4.10

- Updated and refined the main CSS styling.
- Added the SLSL chart page documentation.
- Added the video tutorial page documentation.
- Updated navbar layout and behavior.
- Added CSS overview documentation.

## Changelog - Version 0.4.9
- Improved UI formatting and reduced font size for form validation error messages.
- Secured `/join` and `/call` endpoints by enforcing user login requirements.
- Enhanced security by removing hardcoded reCAPTCHA keys from the source code and migrating them to environment variables.

## Changelog - Version 0.4.8

- Added template overview documentation.
- Added `styles.css` reference documentation.

## Changelog - Version 0.4.7

- API tokens now auto-renew when less than 60 seconds remain on expiry (model.py)
- Added Sphinx autobuild for Developer Documentation

## Changelog - Version 0.4.6

- Replaced the waiting room spinner with a progress bar.
- Created the account deletion request page.
- Made layout fixes and responsive UI improvements.

## Changelog - Version 0.4.5

- Improved responsive web design for better compatibility across desktop, and mobile devices.
- Applied consistent section title colour styling across the Admin Dashboard and Profile.
- Updated the Help and Video Tutorial pages with revised content and navigation improvements.
- Improved and reorganized the Help page layout.
- Updated the Edit Profile page button styling.


## Changelog - Version 0.4.4
- The current HTML files were showing "other participant", changed the backend to show it as the Username


## Changelog - Version 0.4.3
### Added
- Display peer username on remote video
- Integrated Google reCAPTCHA v2 ("I'm not a robot") for bot protection.
- Added reCAPTCHA validation to the user registration and Login forms.
- Configured secure API key handling via Environment Variables for deployment.
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

### Updated
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

### Fixed
- Fixed call sidebar layout causing chat and detection panels to appear below transcript
- Fixed missing dropdown functionality for authenticated navigation
- Fixed chat placeholder persistence after messages begin
- Fixed transcript/chat overflow issues by adding scrollable panels
- Fixed oversized icons and image scaling issues in help/about pages
- Fixed video placeholder overlay interfering with participant video rendering
- Fixed navbar route mismatches and template integration issues
- Fixed Bootstrap mic/camera toggle states and muted visual feedback

### Refactored
- Refactored CSS into reusable shared components and cleaner structure
- Refactored frontend templates to align redesigned UI with backend routes and Jinja logic
- Refactored call page controls and supporting JavaScript interactions

## Documentation
This application uses Sphinx for documentation - please visit https://www.sphinx-doc.org/en/master/usage/quickstart.html for help.

Use `cd docs` followed by `build html` to build the documentation on your machine.

Please note that the documentation is currently UNFINISHED!

## Added to the developer documentation
- API tokens now auto-renew when less than 60 seconds remain on expiry
- Pages added to the developer documentation:
    - Requirements
    - Tutorial: user journey, models and database, blueprints and routing
    - FAQ, API (how-to), running migrations, intro to models, making queries, API Authentication, logging, intro to flask migrate, REST API, Blueprints, App factory, Configuration Reference, erd, extensions

## To-Do
* Add models to the toggle menu
* Polish models

## Academic Supervision
This application was guided and supervised by Ann Roshanie Appuhamy as part of undergraduate coursework.