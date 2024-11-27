// community_posts/utils/puppeteer_publish.js

// Importar dependencias
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const dotenv = require('dotenv');
const fs = require('fs');

// Cargar configuración desde el archivo .env
dotenv.config();

// Habilitar el plugin stealth para evitar detección
puppeteer.use(StealthPlugin());

// Verificar que las credenciales estén configuradas
if (!process.env.LW_USERNAME || !process.env.LW_PASSWORD) {
    console.error("Error: Las credenciales de LW no están configuradas en el archivo .env");
    process.exit(1);
}

// Recibir datos del post desde el argumento del proceso
const postData = JSON.parse(process.argv[2]);

(async () => {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    try {
        // Iniciar sesión en LW
        console.log("Iniciando sesión en LW...");

        await page.goto('https://login.lw.com', { waitUntil: 'networkidle2' });

        await page.type('#username', process.env.LW_USERNAME, { delay: 100 });
        await page.type('#password', process.env.LW_PASSWORD, { delay: 100 });

        await Promise.all([
            page.click('#login-button'),
            page.waitForNavigation({ waitUntil: 'networkidle2' })
        ]);

        console.log("Inicio de sesión exitoso.");

        // Navegar a la comunidad especificada
        console.log(`Navegando a la comunidad: ${postData.community_id}`);
        await page.goto(`https://lw.com/community/${postData.community_id}`, { waitUntil: 'networkidle2' });

        // Publicar el contenido
        console.log("Publicando contenido...");
        await page.type('#post-content', postData.content, { delay: 50 });

        // Enviar el post
        await Promise.all([
            page.click('#submit-post-button'),
            page.waitForNavigation({ waitUntil: 'networkidle2' })
        ]);

        console.log("Publicación exitosa.");
        process.exit(0); // Salida exitosa
    } catch (error) {
        console.error("Error al publicar:", error);
        process.exit(1); // Salida con error
    } finally {
        await browser.close();
    }
})();
