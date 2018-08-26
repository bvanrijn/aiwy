import logging
import time

import praw

import env
import ignore
import templates
import utils

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

reddit = praw.Reddit(
    client_id=env.client_id,
    client_secret=env.client_secret,
    password=env.password,
    user_agent=env.user_agent,
    username=env.username,
)


def main():
    logger.info("Running bot...")
    r_all = reddit.subreddit("all")

    for comment in r_all.stream.comments():
        if ignore.handler.should_ignore_subreddit(
            comment.subreddit.display_name
        ) or ignore.handler.should_ignore_user(comment.author.name):
            continue

        urls = utils.find_urls_in(comment)

        if urls is None:
            continue

        url_to_title = {}

        for url in urls:
            amp_url = utils.is_amp_url(url)

            if amp_url is not False:
                title, canonical_url = utils.get_canonical_url_and_title_for(
                    "http://" + amp_url
                )

                if canonical_url is None:
                    continue

                logger.info(
                    f"[{comment.fullname}] Adding '{canonical_url}' in response to 'http://{amp_url}..."
                )

                url_to_title[canonical_url] = title

        if len(url_to_title) > 0:
            reply = comment.reply(templates.make_comment_text(url_to_title))

            logger.info(f"[{comment.fullname}] Posted {reply.fullname} in response.")


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:  # noqa: E722
            logger.warning(e)
            time.sleep(10 * 60)
