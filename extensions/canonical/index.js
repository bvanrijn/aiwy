const { json, send } = require('micro')
const axios = require('axios')
const cheerio = require('cheerio')

module.exports = async (req, res) => {
    const data = await json(req);
    let response;

    const originalURL = data.url

    try {
        response = await axios.get(data.url);

        if (response.status === 200 && response.headers["content-type"].indexOf("text/html") !== -1) {
            const $ = cheerio.load(response.data);

            const canonicalURL = $('link[rel="canonical"]').attr("href")

            console.log(`[200] (${originalURL} => ${canonicalURL}) OK.`)

            send(res, 200, { ok: true, original: originalURL, canonical: canonicalURL })
        } else {
            console.log(`[404] (${originalURL}) Status not OK or Content-Type not 'text/html'.`)
            send(res, 404, { ok: false, original: originalURL, canonical: null })
        }
    } catch (error) {
        console.log(`[500] (${originalURL}) Error while getting the page.`)
        send(res, 500, { ok: false, original: originalURL, canonical: null })
    }
}