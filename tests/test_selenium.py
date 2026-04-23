import pytest
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = 'http://127.0.0.1:5000'

# unique suffix so re-runs don't collide with existing users in the db
UNIQUE = uuid.uuid4().hex[:8]
TEST_USERNAME = f'selenium_{UNIQUE}'
TEST_EMAIL = f'selenium_{UNIQUE}@test.com'
TEST_PASSWORD = 'Test@Password123!'

@pytest.fixture(scope='module')
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def js_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    driver.execute_script("arguments[0].click();", element)

def test_homepage_loads(driver):
    driver.get(BASE_URL)
    assert 'SignBridge' in driver.title

def test_register_flow(driver):
    driver.get(f'{BASE_URL}/register')
    driver.find_element(By.NAME, 'username').send_keys(TEST_USERNAME)
    driver.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
    driver.find_element(By.NAME, 'password').send_keys(TEST_PASSWORD)
    driver.find_element(By.NAME, 'repeat_password').send_keys(TEST_PASSWORD)
    js_click(driver, driver.find_element(By.CSS_SELECTOR, 'input[type=submit]'))
    WebDriverWait(driver, 10).until(EC.url_contains('/login'))
    assert '/login' in driver.current_url

def test_login_flow(driver):
    driver.get(f'{BASE_URL}/login')
    driver.find_element(By.NAME, 'username').send_keys(TEST_USERNAME)
    driver.find_element(By.NAME, 'password').send_keys(TEST_PASSWORD)
    js_click(driver, driver.find_element(By.CSS_SELECTOR, 'input[type=submit]'))
    WebDriverWait(driver, 10).until(lambda d: d.current_url != f'{BASE_URL}/login')
    assert driver.current_url != f'{BASE_URL}/login'

def test_join_invalid_room(driver):
    driver.get(f'{BASE_URL}/join')
    driver.find_element(By.NAME, 'room_code').send_keys('FAKE-0000')
    js_click(driver, driver.find_element(By.CSS_SELECTOR, 'input[type=submit]'))
    import time; time.sleep(2)  # wait for page to reload
    # app stays on /join and re-renders the form for invalid room codes
    assert driver.current_url == f'{BASE_URL}/join'
    assert driver.find_element(By.NAME, 'room_code')  # form is still present