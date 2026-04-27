Changelog
=========

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