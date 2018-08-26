# Canonical

Canonical is a server that facilitates fast lookups of ```<link rel="canonical" href="...">` values.
A public instance is running at https://canonical.now.sh.

## Usage

Start the server:

```bash
$ npm run start
```

And then:

```bash
$ curl -d '{"url": "http://amp.example.com"}" localhost:443
```

and you get back:

```json
{
    "ok": true,
    "original": "http://amp.example.com",
    "canonical": "http://example.com"
}
```
