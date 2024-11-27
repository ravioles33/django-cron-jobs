// community_posts/utils/puppeteer_publish.js

require("dotenv").config(); // Cargar variables de entorno
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
puppeteer.use(StealthPlugin());

const fs = require("fs");

async function main() {
    let postData;

    // Leer datos de la entrada estándar si están disponibles
    try {
        const input = fs.readFileSync(0, "utf-8");
        postData = JSON.parse(input);
    } catch (err) {
        console.error("Error al leer los datos de entrada: ", err.message);
        return;
    }

    const { community_id, content } = postData;

    if (!community_id || !content) {
        console.error("Faltan datos requeridos: community_id o content.");
        return;
    }

    const username = process.env.LW_USERNAME;
    const password = process.env.LW_PASSWORD;

    if (!username || !password) {
        console.error("Credenciales faltantes en las variables de entorno.");
        return;
    }

    try {
        const browser = await puppeteer.launch({
            headless: true, // Cambiar a false para debugging
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });

        const page = await browser.newPage();
        await page.setViewport({ width: 1920, height: 1080 });

        // Navegar a la página de inicio de sesión
        const loginPageUrl = "https://go.producthackers.com/?msg=not-logged-in";
        console.log("Navegando a la página de inicio de sesión...");
        await page.goto(loginPageUrl, { waitUntil: "networkidle2" });

        // Aceptar cookies si el banner está presente
        try {
            await page.waitForSelector('button:contains("¡Entendido!")', { timeout: 5000 });
            await page.click('button:contains("¡Entendido!")');
            console.log("Banner de cookies aceptado.");
        } catch {
            console.log("No se detectó el banner de cookies.");
        }

        // Iniciar sesión
        console.log("Iniciando sesión...");
        await page.waitForSelector("#animatedModal", { visible: true });
        await page.type('input.sign-input.-email-input[name="email"]', username);
        await page.type('input.sign-input.-pass-input[name="password"]', password);
        await page.click('div#submitLogin');
        await page.waitForNavigation({ waitUntil: "networkidle2" });
        console.log("Inicio de sesión exitoso.");

        // Obtener el token CSRF
        const csrfToken = await page.$eval(
            'meta[name="csrf-token"]',
            (element) => element.content
        );
        console.log("Token CSRF obtenido:", csrfToken);

        // Publicar el mensaje
        const postUrl = "https://go.producthackers.com/api/posts";
        const headers = {
            accept: "application/json",
            "content-type": "application/json",
            "csrf-token": csrfToken,
            origin: "https://go.producthackers.com",
            referer: `https://go.producthackers.com/author/social/channel/${community_id}`,
            "user-agent": await page.evaluate(() => navigator.userAgent)
        };

        const data = {
            text: content,
            group_id: community_id
        };

        const response = await page.evaluate(
            async ({ postUrl, headers, data }) => {
                const response = await fetch(postUrl, {
                    method: "POST",
                    headers,
                    body: JSON.stringify(data)
                });
                return {
                    status: response.status,
                    text: await response.text()
                };
            },
            { postUrl, headers, data }
        );

        console.log("Código de estado:", response.status);
        console.log("Respuesta:", response.text);

        if (response.status === 200) {
            console.log("Publicación exitosa.");
        } else {
            console.error("Error al publicar:", response.text);
        }

        await browser.close();
    } catch (err) {
        console.error("Error durante la ejecución:", err.message);
    }
}

main();
