# AMP Is Watching You

The [amp-is-watching-you Reddit bot](https://old.reddit.com/u/amp-is-watching-you) replaces AMP links on Reddit with their non-AMP counterparts, which is better for privacy.

## Contributing

Get up to speed with the Aiwy project. Some basic Python knowledge is required.

1. Install [Visual Studio Code](https://code.visualstudio.com). It's awesome. And it's free.
2. Install [`pipenv`](https://pipenv.readthedocs.io/en/latest/). `pip3 install pipenv --user` should do the trick.
3. Install [`pyenv`](https://github.com/pyenv/pyenv).
```bash
$ curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```
4. Run `pipenv install` and `pipenv install --pre --dev` to install the required dependencies. (`pipenv` will automatically install Python 3.7 for you ✨🍰✨)
5. Update `python.pythonPath` in `.vscode/settings.json` to `echo $(pipenv --venv)/bin/python`.

...and when that's all done, run `code .` and work on an interesting issue or a new feature. All help is welcome.

## Running the bot

Create a file `env.py`:

```python
# Generate these using https://praw.readthedocs.io/en/latest/getting_started/authentication.html
client_id = "..."
client_secret = "..."

password = "..."
admin = "..." # Your personal user name
user_agent = f"aiwy/1.6.0 by /u/{admin}"
username = "amp-is-watching-you" # Your bot's username
```

Run:

```bash
$ pipenv run comments
$ pipenv run submissions
$ pipenv run ignore
```