// findInPage finds all the AMP URLs on the page
function findInPage() {
    const links = document.querySelectorAll("a")
    const AMP_REGEX = new RegExp("google[a-z.]+\/amp\/(?:s/)?(.*)", "gi")
    let ampURLs = []

    for (const link of links) {
        if (AMP_REGEX.test(link) === true) {
            console.log(`Found ${link} on page.`)

            ampURLs.push(link.href)
        }
    }

    return ampURLs
}

// createRequest creates an Axios POST request for an AMP URL to be resolved using canonical
function createRequest(url) {
    console.log(`Creating request for ${url}`)
    return axios.post("https://canonical.now.sh/", {
        url: url,
    })
}

// getNonAMPURLs resolves all AMP URLs passed to it
function getNonAMPURLs(ampURLs) {
    let nonAMPURLs = {};
    let requests = [];

    for (const ampURL of ampURLs) {
        requests.push(createRequest(ampURL))
    }


    axios.all(requests)
        .then(axios.spread(function (...responses) {
            for (const response of responses) {
                const data = response.data

                if (data.ok === true) {
                    for (let link of document.querySelectorAll("a")) {
                        if (link.href === data.original) {
                            if (link.innerText === data.original) {
                                link.innerText = data.canonical
                            }

                            link.href = data.canonical
                            link.style.border = "1px solid green"
                        }
                    }
                }
            }
        }
        ))

    return nonAMPURLs
}

const ampURLs = findInPage()
const nonAMPURLs = getNonAMPURLs(ampURLs)


// console.log(getNonAMPURLs(["https://www.google.co.uk/amp/s/comicbook.com/marvel/amp/2018/07/08/ant-man-and-the-wasp-norman-osborn-mcu/?source=images"]))

