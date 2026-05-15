"""End-to-end browser tests using Selenium WebDriver.

Exercises the full user journey through a real Chrome browser against a
running development server. Tests are ordered and share a single
``module``-scoped :func:`driver` fixture so that state (cookies, session)
is preserved across the sequence: homepage → register → login → join.

.. warning::
    These tests require a live application server to be running at
    ``http://127.0.0.1:5000`` before the test session starts. They will
    fail immediately with a ``WebDriverException`` if the server is not
    reachable. Start the server with ``python run.py`` in a separate
    terminal before invoking pytest.

Note:
    A UUID-derived suffix is appended to all test credentials at import
    time so that re-runs against a persistent database do not collide
    with accounts created in previous sessions. reCAPTCHA must be
    disabled (``RECAPTCHA_USE_SSL = False`` and test mode keys) for
    form submissions to succeed.

Attributes:
    BASE_URL (str): Root URL of the running development server.
    UNIQUE (str): Eight-character hex suffix derived from a random UUID,
        used to namespace credentials for this test session.
    TEST_USERNAME (str): Dynamically generated username in the form
        ``selenium_<UNIQUE>``.
    TEST_EMAIL (str): Dynamically generated email in the form
        ``selenium_<UNIQUE>@test.com``.
    TEST_PASSWORD (str): Password used for all registration and login
        operations in this session. Meets the application's complexity
        requirements.
"""

import time
import uuid

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = 'http://127.0.0.1:5000'
UNIQUE = uuid.uuid4().hex[:8]
TEST_USERNAME = f'selenium_{UNIQUE}'
TEST_EMAIL = f'selenium_{UNIQUE}@test.com'
TEST_PASSWORD = 'Test@Password123!'


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope='module')
def driver():
    """Provide a headless Chrome WebDriver instance for the test module.

    Configured with the following options:

    - ``--headless``: runs without a visible browser window, suitable
      for CI environments.
    - ``--no-sandbox``: required when running as root in Docker or CI.
    - ``--disable-dev-shm-usage``: prevents crashes on systems with a
      small ``/dev/shm`` partition.
    - ``--window-size=1920,1080``: ensures responsive layouts render at
      a consistent viewport so element selectors behave predictably.

    The driver is scoped to the module so that the browser session —
    and therefore the authenticated cookie — persists across all tests
    in this file. :func:`~selenium.webdriver.Chrome.quit` is called
    after the last test regardless of pass/fail status.

    Yields:
        selenium.webdriver.Chrome: A fully configured WebDriver instance
        with a 5-second implicit wait applied globally.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    drv = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    drv.implicitly_wait(5)
    yield drv
    drv.quit()


# helper methods

def js_click(driver, element) -> None:
    """Scroll an element into view and click it via JavaScript.

    Used in place of :meth:`~selenium.webdriver.remote.webelement.WebElement.click`
    for submit buttons that may be obscured by a sticky header or
    outside the current viewport, which causes a standard Selenium click
    to raise ``ElementClickInterceptedException``.

    Args:
        driver (selenium.webdriver.Chrome): The active WebDriver instance.
        element (selenium.webdriver.remote.webelement.WebElement): The
            element to scroll to and click.
    """
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    driver.execute_script("arguments[0].click();", element)


# tests begin here

def test_homepage_loads(driver):
    """Landing page loads and includes 'SignBridge' in the browser title.

    Navigates to :data:`BASE_URL` and asserts that the page title
    contains the application name, confirming the server is reachable
    and the root route renders correctly.

    Args:
        driver (selenium.webdriver.Chrome): The module-scoped WebDriver
            provided by :func:`driver`.
    """
    driver.get(BASE_URL)
    assert 'SignBridge' in driver.title


def test_register_flow(driver):
    """Registration form creates a new account and redirects to ``/login``.

    Navigates to ``/register``, fills all required fields with the
    session-unique credentials, submits via :func:`js_click`, and waits
    up to 10 seconds for the URL to contain ``/login``. Asserts that
    the redirect occurred, confirming the account was created
    successfully.

    Note:
        This test must run before :func:`test_login_flow` because the
        registered account is required by subsequent tests. pytest
        executes tests in definition order within a module by default,
        so no explicit ordering plugin is needed.

    Args:
        driver (selenium.webdriver.Chrome): The module-scoped WebDriver
            provided by :func:`driver`.
    """
    driver.get(f'{BASE_URL}/register')
    driver.find_element(By.NAME, 'username').send_keys(TEST_USERNAME)
    driver.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
    driver.find_element(By.NAME, 'password').send_keys(TEST_PASSWORD)
    driver.find_element(By.NAME, 'repeat_password').send_keys(TEST_PASSWORD)
    js_click(driver, driver.find_element(By.CSS_SELECTOR, 'input[type=submit]'))

    WebDriverWait(driver, 10).until(EC.url_contains('/login'))
    assert '/login' in driver.current_url


def test_login_flow(driver):
    """Login form authenticates the registered user and leaves the login page.

    Navigates to ``/login``, submits the session credentials, and waits
    until the URL changes away from ``/login``. Asserts that the final
    URL is not ``/login``, confirming a successful authentication and
    redirect (typically to ``/your-account/dashboard``).

    Args:
        driver (selenium.webdriver.Chrome): The module-scoped WebDriver
            provided by :func:`driver`. The session cookie set here is
            retained for all subsequent tests in this module.
    """
    driver.get(f'{BASE_URL}/login')
    driver.find_element(By.NAME, 'username').send_keys(TEST_USERNAME)
    driver.find_element(By.NAME, 'password').send_keys(TEST_PASSWORD)
    js_click(driver, driver.find_element(By.CSS_SELECTOR, 'input[type=submit]'))

    WebDriverWait(driver, 10).until(
        lambda d: d.current_url != f'{BASE_URL}/login'
    )
    assert driver.current_url != f'{BASE_URL}/login'


def test_join_invalid_room(driver):
    """Join form stays on ``/join`` and re-renders when the room code is invalid.

    Navigates to ``/join``, enters a room code that has no corresponding
    database row (``FAKE-0000``), submits the form, and waits two
    seconds for the page to reload. Asserts two things:

    - The URL remains ``/join``, confirming no redirect to ``/call``
      occurred.
    - The ``room_code`` input element is still present in the DOM,
      confirming the join form was re-rendered rather than replaced with
      an error page.

    Note:
        The two-second ``time.sleep`` is a pragmatic workaround for the
        implicit wait not catching a same-URL page reload. Consider
        replacing it with a :class:`~selenium.webdriver.support.ui.WebDriverWait`
        on a flash message element for a more robust assertion::

            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.flash-message'))
            )

    Args:
        driver (selenium.webdriver.Chrome): The module-scoped WebDriver
            provided by :func:`driver`.
    """
    driver.get(f'{BASE_URL}/join')
    driver.find_element(By.NAME, 'room_code').send_keys('FAKE-0000')
    js_click(driver, driver.find_element(By.CSS_SELECTOR, 'input[type=submit]'))

    time.sleep(2)

    assert driver.current_url == f'{BASE_URL}/join'
    assert driver.find_element(By.NAME, 'room_code')