// Ruta: community_posts/utils/puppeteer_publish.js

const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
require('dotenv').config();

puppeteer.use(StealthPlugin());

const login = async () => {
    const loginPageUrl = 'https://go.producthackers.com/?msg=not-logged-in';
    const username = process.env.LW_USERNAME;
    const password = process.env.LW_PASSWORD;

    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    try {
        await page.goto(loginPageUrl, { waitUntil: 'networkidle2' });
        await page.type('input[name="email"]', username);
        await page.type('input[name="password"]', password);
        await page.click('button[type="submit"]');
        await page.waitForNavigation({ waitUntil: 'networkidle2' });

        const csrfToken = await page.$eval(
            'meta[name="csrf-token"]',
            element => element.content
        );

        return { browser, page, csrfToken };
    } catch (error) {
        console.error('Error during login:', error);
        await browser.close();
        throw error;
    }
};

const executePublishScript = async (post, logger) => {
    try {
        const { browser, page, csrfToken } = await login();
        const postUrl = 'https://go.producthackers.com/api/posts';
        const response = await page.evaluate(async ({ postUrl, post, csrfToken }) => {
            return await fetch(postUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'csrf-token': csrfToken
                },
                body: JSON.stringify({
                    text: post.content,
                    group_id: post.community.community_id
                })
            });
        }, { postUrl, post, csrfToken });

        logger.info('Post publicado:', response.status);
        await browser.close();
        return response.ok;
    } catch (error) {
        logger.error('Error publicando el post:', error);
        return false;
    }
};

module.exports = { executePublishScript };
