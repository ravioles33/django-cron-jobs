# community_posts/utils/selenium_publish.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def execute_publish_script(post, logger):
    username = os.getenv('LW_USERNAME')
    password = os.getenv('LW_PASSWORD')
    group_id = post.community.community_id
    message_html = post.content

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    try:
        login_page_url = 'https://go.producthackers.com/?msg=not-logged-in'
        driver.get(login_page_url)
        logger.info('Página cargada')

        wait = WebDriverWait(driver, 30)

        try:
            cookie_banner = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.lw-cookie-disclaimer')))
            accept_button = cookie_banner.find_element(By.XPATH, ".//button[contains(text(), '¡Entendido!')]")
            accept_button.click()
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.lw-cookie-disclaimer')))
            logger.info('Banner de cookies cerrado')
        except Exception:
            logger.warning('No se detectó banner de cookies o hubo un error al cerrarlo:', exc_info=True)

        modal = wait.until(EC.visibility_of_element_located((By.ID, 'animatedModal')))
        email_input = modal.find_element(By.CSS_SELECTOR, 'input.sign-input.-email-input[name="email"]')
        password_input = modal.find_element(By.CSS_SELECTOR, 'input.sign-input.-pass-input[name="password"]')

        email_input.send_keys(username)
        password_input.send_keys(password)
        login_button = modal.find_element(By.CSS_SELECTOR, 'div#submitLogin')
        driver.execute_script("arguments[0].click();", login_button)

        wait.until(EC.url_contains('dashboard'))
        logger.info('Inicio de sesión exitoso')

        cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        page_source = driver.page_source
        csrf_token_match = re.search(r'name="csrf-token" content="([a-zA-Z0-9_-]+)"', page_source)
        csrf_token = csrf_token_match.group(1) if csrf_token_match else None

        if csrf_token:
            logger.info(f'Token CSRF obtenido desde HTML: {csrf_token}')
        else:
            logger.warning('No se pudo obtener el token CSRF desde el HTML')
            return False

        url = "https://go.producthackers.com/api/posts"
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'csrf-token': csrf_token,
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

        data = {
            'text': message_html,
            'group_id': group_id
        }

        response = session.post(url, headers=headers, json=data)
        logger.info(f'Status Code: {response.status_code}')
        logger.info(f'Response: {response.text}')

        return response.status_code == 200

    except Exception as e:
        logger.error(f'Error durante el inicio de sesión: {e}', exc_info=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f'login_error_{timestamp}.png'
        driver.save_screenshot(screenshot_name)
        logger.error(f'Captura de pantalla guardada como {screenshot_name}')
        return False

    finally:
        driver.quit()
