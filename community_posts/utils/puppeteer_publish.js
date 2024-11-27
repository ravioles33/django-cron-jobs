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
        const browser = await puppeteer.launch({ headless: true });
        const page = await browser.newPage();

        await page.goto("https://example-login-page.com/login", { waitUntil: "networkidle0" });
        await page.type("#username", username);
        await page.type("#password", password);
        await page.click("#loginButton");

        await page.waitForNavigation();

        await page.goto(`https://example-community.com/${community_id}/post`, { waitUntil: "networkidle0" });
        await page.type("#postContent", content);
        await page.click("#submitPost");

        console.log("Post publicado con éxito.");
        await browser.close();
    } catch (err) {
        console.error("Error durante la ejecución: ", err.message);
    }
}

main();
