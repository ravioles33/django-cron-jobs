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
        await page.waitForSelector('#animatedModal', { visible: true });
        await page.type('input.sign-input.-email-input[name="email"]', username);
        await page.type('input.sign-input.-pass-input[name="password"]', password);
        await page.click('div#submitLogin');
        await page.waitForNavigation({ waitUntil: 'networkidle2' });

        const csrfToken = await page.$eval(
            'meta[name="csrf-token"]',
            (element) => element.content
        );

        return { browser, page, csrfToken };
    } catch (error) {
        console.error('Error during login:', error);
        await browser.close();
        throw error;
    }
};

const postMessage = async (page, csrfToken, groupId, messageHtml) => {
    const postUrl = 'https://go.producthackers.com/api/posts';

    const headers = {
        accept: 'application/json',
        'content-type': 'application/json',
        'csrf-token': csrfToken,
    };

    const data = {
        text: messageHtml,
        group_id: groupId,
    };

    const response = await page.evaluate(
        async ({ postUrl, headers, data }) => {
            const response = await fetch(postUrl, {
                method: 'POST',
                headers,
                body: JSON.stringify(data),
            });
            return response.status;
        },
        { postUrl, headers, data }
    );

    return response;
};

(async () => {
    try {
        const groupId = 'your-group-id';
        const messageHtml = '<p>Test message</p>';
        const { browser, page, csrfToken } = await login();
        await postMessage(page, csrfToken, groupId, messageHtml);
        console.log('Message posted successfully');
        await browser.close();
    } catch (error) {
        console.error('Error:', error);
    }
})();
