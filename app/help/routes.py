"""Route handlers for the help blueprint.

Serves static informational pages registered under the ``/help`` prefix
(see :func:`app.create_app` for blueprint registration). All views are
``GET``-only and require no authentication.
"""

from flask import render_template

from app.help import help_bp


@help_bp.route('/')
def help_index():
    """Render the help index page.

    Acts as the landing page for the ``/help`` prefix. Named
    ``help_index`` rather than ``help`` to avoid shadowing Python's
    built-in :func:`help` function.

    Returns:
        flask.Response: The rendered ``help/help.html`` template.
    """
    return render_template('help/help.html', title='Help')


@help_bp.route('/slslchart')
def slslchart():
    """Render the Sri Lanka Sign Language (SLSL) fingerspelling chart.

    Provides a static visual reference for the SLSL fingerspelling
    alphabet used by the sign-recognition model.

    Returns:
        flask.Response: The rendered ``help/slslchart.html`` template.
    """
    return render_template('help/slslchart.html', title='SLSL Chart')


@help_bp.route('/video-tutorial')
def video_tutorial():
    """Render the video tutorial page.

    Hosts an embedded walkthrough demonstrating how to use the
    application's call and sign-recognition features.

    Returns:
        flask.Response: The rendered ``help/video-tutorial.html``
        template.
    """
    return render_template('help/video-tutorial.html', title='Video Tutorial')