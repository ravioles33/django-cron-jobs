// community_posts/utils/puppeteer_publish.js

require("dotenv").config();
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
const fs = require("fs");

puppeteer.use(StealthPlugin());

async function main() {
    let postData;

    // Leer datos de la entrada estándar
    try {
        const input = fs.readFileSync(0, "utf-8");
        postData = JSON.parse(input);
    } catch (err) {
        console.error("Error al leer los datos de entrada: ", err.message);
        process.exit(1);
    }

    const { community_id, content, lw_username, lw_password } = postData;

    if (!community_id || !content) {
        console.error("Faltan datos requeridos: community_id o content.");
        process.exit(1);
    }

    if (!lw_username || !lw_password) {
        console.error("Credenciales de LW faltantes.");
        process.exit(1);
    }

    try {
        console.log("Iniciando Puppeteer...");
        const browser = await puppeteer.launch({
            headless: true,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-gpu',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--single-process',
                '--disable-extensions',
            ],
            executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || undefined,
        });

        const page = await browser.newPage();
        await page.setViewport({ width: 1920, height: 1080 });

        // Navegar a la página de inicio de sesión
        console.log("Navegando a la página de inicio de sesión...");
        await page.goto("https://go.producthackers.com/?msg=not-logged-in", { waitUntil: "networkidle2" });

        // Aceptar cookies si el banner está presente
        try {
            const [cookieButton] = await page.$x("//button[contains(text(),'¡Entendido!')]");
            if (cookieButton) {
                await cookieButton.click();
                console.log("Banner de cookies aceptado.");
            }
        } catch (err) {
            console.log("No se detectó el banner de cookies.");
        }

        // Iniciar sesión
        console.log("Iniciando sesión...");
        await page.waitForSelector("#animatedModal", { visible: true });
        await page.type('input.sign-input.-email-input[name="email"]', lw_username);
        await page.type('input.sign-input.-pass-input[name="password"]', lw_password);
        await page.click('div#submitLogin');
        await page.waitForNavigation({ waitUntil: "networkidle2" });
        console.log("Inicio de sesión exitoso.");

        // Obtener el token CSRF
        const csrfToken = await page.$eval('meta[name="csrf-token"]', (el) => el.content);
        console.log("Token CSRF obtenido:", csrfToken);

        // Publicar el mensaje
        const postUrl = "https://go.producthackers.com/api/posts";
        const headers = {
            accept: "application/json",
            "content-type": "application/json",
            "csrf-token": csrfToken,
            origin: "https://go.producthackers.com",
            referer: `https://go.producthackers.com/author/social/channel/${community_id}`,
            "user-agent": await page.evaluate(() => navigator.userAgent),
        };

        const data = {
            attachments: [],
            best_of: null,
            comments: [],
            context: null,
            likes: null,
            social_object: { type: null, data: null },
            social_items: [],
            text: content,
            text_mentions: [],
            group_id: community_id,
        };

        console.log("Enviando solicitud POST para publicar el mensaje...");
        const response = await page.evaluate(
            async ({ postUrl, headers, data }) => {
                const res = await fetch(postUrl, {
                    method: "POST",
                    headers,
                    body: JSON.stringify(data),
                });
                return { status: res.status, body: await res.text() };
            },
            { postUrl, headers, data }
        );

        console.log("Código de estado:", response.status);
        console.log("Respuesta del servidor:", response.body);

        if (response.status === 200) {
            console.log("Publicación exitosa.");
            await browser.close();
            process.exit(0);
        } else {
            console.error("Error al publicar:", response.body);
            await browser.close();
            process.exit(1);
        }
    } catch (err) {
        console.error("Error durante la ejecución:", err.stack);
        await browser.close();
        process.exit(1);
    }
}

main();
