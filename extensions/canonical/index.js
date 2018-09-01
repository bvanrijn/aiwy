const { json, send } = require('micro')
const axios = require('axios')
const cheerio = require('cheerio')
const pify = require('pify')
const morgan = require('morgan')

const logger = pify(morgan('[:date[clf]] :method :url :status :response-time ms - :res[content-length]')) // Like morgan('dev') but with timestamp

module.exports = async (req, res) => {
  await logger(req, res)

  const data = await json(req)
  let response

  const developerMode = data.dev
  const originalURL = data.url

  const log = (devMessage, noDevMessage) => {
    if (developerMode === true) {
      console.log(devMessage)
    } else {
      console.log(noDevMessage)
    }
  }

  try {
    response = await axios.get(data.url)

    if (response.status === 200 && response.headers['content-type'].indexOf('text/html') !== -1) {
      const $ = cheerio.load(response.data)

      const canonicalURL = $('link[rel="canonical"]').attr('href')

      log(`[200] (${originalURL} => ${canonicalURL}) OK.`, '[200] OK.')

      send(res, 200, { ok: true, original: originalURL, canonical: canonicalURL })
    } else {
      log(`[404] (${originalURL}) Status not OK or Content-Type not 'text/html'.`, "[404] Status not OK or Content-Type not 'text/html'.")
      send(res, 404, { ok: false, original: originalURL, canonical: null })
    }
  } catch (error) {
    log(`[500] (${originalURL}) Error while getting the page.`, '[500] Error while getting the page.')
    send(res, 500, { ok: false, original: originalURL, canonical: null })
  }
}
