from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests  # Asegurando la importación correcta de requests
import os
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def execute_publish_script(post, logger):
    # Información del usuario desde variables de entorno
    username = os.getenv('LW_USERNAME')
    password = os.getenv('LW_PASSWORD')
    group_id = post.community.community_id
    message_html = post.content

    # Configurar Selenium con opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    try:
        login_page_url = 'https://go.producthackers.com/?msg=not-logged-in'
        driver.get(login_page_url)
        logger.info('Página cargada')

        wait = WebDriverWait(driver, 30)

        # Aceptar las cookies si el banner está presente
        try:
            cookie_banner = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.lw-cookie-disclaimer')))
            accept_button = cookie_banner.find_element(By.XPATH, ".//button[contains(text(), '¡Entendido!')]")
            accept_button.click()
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.lw-cookie-disclaimer')))
            logger.info('Banner de cookies cerrado')
        except Exception as e:
            logger.warning('No se detectó banner de cookies o hubo un error al cerrarlo:', exc_info=True)

        # Esperar a que el modal de inicio de sesión esté visible
        modal = wait.until(EC.visibility_of_element_located((By.ID, 'animatedModal')))
        email_input = modal.find_element(By.CSS_SELECTOR, 'input.sign-input.-email-input[name="email"]')
        password_input = modal.find_element(By.CSS_SELECTOR, 'input.sign-input.-pass-input[name="password"]')

        # Ingresar las credenciales
        email_input.send_keys(username)
        password_input.send_keys(password)
        login_button = modal.find_element(By.CSS_SELECTOR, 'div#submitLogin')
        driver.execute_script("arguments[0].click();", login_button)

        # Esperar a que la URL cambie indicando inicio de sesión exitoso
        wait.until(EC.url_contains('dashboard'))
        logger.info('Inicio de sesión exitoso')

        # Extraer las cookies de la sesión
        cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        # Intentar obtener el token CSRF desde el HTML de la página
        page_source = driver.page_source
        csrf_token_match = re.search(r'name="csrf-token" content="([a-zA-Z0-9_-]+)"', page_source)
        csrf_token = csrf_token_match.group(1) if csrf_token_match else None

        if csrf_token:
            logger.info(f'Token CSRF obtenido desde HTML: {csrf_token}')
        else:
            logger.warning('No se pudo obtener el token CSRF desde el HTML')
            return False

        # URL del endpoint
        url = "https://go.producthackers.com/api/posts"

        # Encabezados (headers) con las cookies y el token CSRF
        headers = {
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-GB,en;q=0.9,es-AR;q=0.8,es;q=0.7',
            'content-type': 'application/json',
            'csrf-token': csrf_token,
            'origin': 'https://go.producthackers.com',
            'referer': f'https://go.producthackers.com/author/social/channel/{group_id}',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

        # Payload (contenido del post)
        data = {
            'attachments': [],
            'best_of': None,
            'comments': [],
            'context': None,
            'likes': None,
            'social_object': {'type': None, 'data': None},
            'social_items': [],
            'text': message_html,
            'text_mentions': [],
            'group_id': group_id
        }

        # Enviar la solicitud POST
        response = session.post(url, headers=headers, json=data)

        # Verificar el resultado
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
        # Cerrar el navegador
        driver.quit()
