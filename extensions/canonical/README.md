# Canonical

Canonical is a server that facilitates fast lookups of `<link rel="canonical" href="...">` values.
A public instance is running at https://canonical.now.sh.

## Usage

Start the server:

```bash
npm run start
```

And then:

```bash
curl -d '{"url": "http://amp.example.com"}' localhost:443
```

and you get back:

```json
{
    "ok": true,
    "original": "http://amp.example.com",
    "canonical": "http://example.com"
}
```

## Your privacy

The extensions in this directory (and the canonical server) are designed to use as little personal data as possible. For instance, the extensions only contact canonical.now.sh over a secure HTTPS connection, and logs are extremely limited in scope:

```
[01/Sep/2018:23:11:38 +0000] POST / 200 647.165 ms - 201
```

The canonical server will only produce a detailed log when explicitly asked to do so (using `{"dev": true}`):

```
[200] (https://www.google.com/amp/s/phys.org/news/2018-08-google-news-liberals-similar-results.amp => https://phys.org/news/2018-08-google-news-liberals-similar-results.html) OK.
[01/Sep/2018:23:15:33 +0000] POST / 200 754.085 ms - 201
```