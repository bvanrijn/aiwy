import json
import logging
import pathlib
import re
import shutil
import time
from datetime import datetime

import praw
from praw.models import Message

import env
import templates

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


class IgnoreHandler:
    def __init__(self):
        self._ignorefile = str(pathlib.Path.cwd() / "ignore.json")

        with open(self._ignorefile) as ignores:
            self.ignores = json.load(ignores)

    def _exist(self, _in, name):
        return name in self.ignores[_in]

    def _should_ignore(self, _in, name):
        return self._exist(_in, name)

    def _set(self, _in, name):
        if not self._exist(_in, name):
            self.ignores[_in].append(name)

        self.save_ignores()

    def _rm(self, _in, name):
        if name in self.ignores[_in]:
            self.ignores[_in].remove(name)

        self.save_ignores()

    def ignore_user(self, user):
        self._set("users", user)

    def unignore_user(self, user):
        self._rm("users", user)

    def ignore_subreddit(self, subreddit):
        self._set("subreddits", subreddit)

    def unignore_subreddit(self, subreddit):
        self._rm("subreddits", subreddit)

    def save_ignores(self):
        backup_file_name = str(
            pathlib.Path.cwd()
            / "ignores"
            / f"ignores.{datetime.now().strftime('%Y-%m-%d--%H:%M:%S')}.json"
        )

        shutil.move(self._ignorefile, backup_file_name)

        with open(self._ignorefile, "w+") as ignores:
            ignores.write(json.dumps(self.ignores, indent=4))

    def should_ignore_user(self, name):
        return self._should_ignore("users", name)

    def should_ignore_subreddit(self, name):
        return self._should_ignore("subreddits", name)


handler = IgnoreHandler()


def main():
    reddit = praw.Reddit(
        client_id=env.client_id,
        client_secret=env.client_secret,
        password=env.password,
        user_agent=env.user_agent,
        username=env.username,
    )

    print("Handling ignores/bans...")

    SUBREDDIT_REGEX = re.compile(
        r"(?:\/?r\/([a-zA-Z0-9_]{2,21}))", re.IGNORECASE | re.MULTILINE
    )

    for item in reddit.inbox.stream():
        if isinstance(item, Message):
            message = item

            subject = message.subject

            if message.author is not None:
                author = message.author.name

            message.mark_read()

            if (
                "You've been banned from participating in " in subject
                and message.author is None
            ) or ("nab " in subject and message.author.name == env.admin):
                subreddit = SUBREDDIT_REGEX.findall(subject)[0]

                print(f"Handling ban/nab for /r/{subreddit}")

                handler.ignore_subreddit(subreddit)
            elif "unban " in subject and message.author.name == env.admin:
                subreddit = SUBREDDIT_REGEX.findall(subject)[0]

                print(f"Handling unban for /r/{subreddit}")

                handler.unignore_subreddit(subreddit)
            elif subject == "ignore":
                message.reply(templates.BOT_IGNORE)

                print(f"Handling ignore for /u/{author}")

                handler.ignore_user(author)
            elif subject == "unignore":
                message.reply(templates.BOT_UNIGNORE)

                print(f"Handling unignore for /u/{author}")

                handler.unignore_user(author)
            else:
                print(f"Not handling '{subject}' by /u/{author}")

                message.mark_unread()


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            logger.warning(e)
            time.sleep(10 * 60)
