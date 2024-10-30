from celery import shared_task
from .models import Post
from django.utils import timezone
import os
import requests  # Import para manejar la sesión
def create_session():
    # Crear una nueva sesión para cada ejecución de la tarea para evitar problemas de concurrencia
    return requests.Session()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # Cargar las variables de entorno

@shared_task
def check_pending_posts():
    now = timezone.now()
    pending_posts = Post.objects.filter(status='pending', scheduled_time__lte=now)

    for post in pending_posts:
        try:
            # Crear una nueva sesión para cada post
            session = create_session()
            # Ejecutar el script de publicación con Selenium
            success = execute_publish_script(post, session)
            if success:
                post.status = 'published'  # Actualiza el estado a 'publicado' si se hace correctamente
                print(f"Publicado: {post.content}")
            else:
                update_post_status(post)
                print(f"Error al publicar: {post.content}, reintentando: {post.status}")
        except Exception as e:
            update_post_status(post)
            print(f"Error durante la publicación: {post.content}, Error: {e}")

        post.save()

def update_post_status(post):
    # Actualiza el estado del post según el número de reintentos
    error_statuses = ['pending', 'error', 'error-1', 'error-2', 'error-3', 'error-4']
    if post.status in error_statuses:
        current_index = error_statuses.index(post.status)
        if current_index < len(error_statuses) - 1:
            post.status = error_statuses[current_index + 1]
        else:
            post.status = 'error-00'  # Marca como error final después de 5 intentos

def execute_publish_script(post, session):
    # Información del usuario desde variables de entorno
    username = os.getenv('LW_USERNAME')
    password = os.getenv('LW_PASSWORD')
    group_id = post.community.community_id
    message_html = post.content

    # Configurar Selenium con opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--headless')  # Descomentar si se desea ejecutar en modo headless

    driver = webdriver.Chrome(options=chrome_options)
    try:
        login_page_url = 'https://go.producthackers.com/?msg=not-logged-in'
        driver.get(login_page_url)
        print('Página cargada')

        wait = WebDriverWait(driver, 30)

        # Aceptar las cookies si el banner está presente
        try:
            cookie_banner = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.lw-cookie-disclaimer')))
            accept_button = cookie_banner.find_element(By.XPATH, ".//button[contains(text(), '¡Entendido!')]")
            accept_button.click()
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.lw-cookie-disclaimer')))
            print('Banner de cookies cerrado')
        except Exception as e:
            print('No se detectó banner de cookies o hubo un error al cerrarlo:', e)

        # Esperar a que el modal de inicio de sesión esté visible
        modal = wait.until(EC.visibility_of_element_located((By.ID, 'animatedModal')))
        email_input = modal.find_element(By.CSS_SELECTOR, 'input.sign-input.-email-input[name="email"]')
        password_input = modal.find_element(By.CSS_SELECTOR, 'input.sign-input.-pass-input[name="password"]')

        # Ingresar las credenciales
        email_input.send_keys(username)
        password_input.send_keys(password)
        login_button = modal.find_element(By.CSS_SELECTOR, 'div#submitLogin')
        login_button.click()

        # Esperar a que la URL cambie indicando inicio de sesión exitoso
        wait.until(EC.url_contains('dashboard'))
        print('Inicio de sesión exitoso')

        # Extraer las cookies de la sesión
        cookies = driver.get_cookies()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        # Intentar obtener el token CSRF desde el HTML de la página
        page_source = driver.page_source
        csrf_token_match = re.search(r'name="csrf-token" content="([a-zA-Z0-9_-]+)"', page_source)
        csrf_token = csrf_token_match.group(1) if csrf_token_match else None

        if csrf_token:
            print('Token CSRF obtenido desde HTML:', csrf_token)
        else:
            print('No se pudo obtener el token CSRF desde el HTML')
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
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')

        return response.status_code == 200

    except Exception as e:
        print(f'Error durante el inicio de sesión: {e}')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f'login_error_{timestamp}.png'
        driver.save_screenshot(screenshot_name)
        print(f'Captura de pantalla guardada como {screenshot_name}')
        return False

    finally:
        # Cerrar el navegador
        driver.quit()
