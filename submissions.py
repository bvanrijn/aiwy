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

    for submission in r_all.stream.submissions():
        if (
            ignore.handler.should_ignore_subreddit(submission.subreddit.display_name)
            or ignore.handler.should_ignore_user(submission.author.name)
            or (submission.selftext_html is None and submission.url is None)
        ):
            continue

        urls = utils.find_urls_in(submission)

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
                    f"[{submission.fullname}] Adding '{canonical_url}' in response to 'http://{amp_url}..."
                )

                url_to_title[canonical_url] = title

        if len(url_to_title) > 0:
            reply = submission.reply(templates.make_comment_text(url_to_title))

            logger.info(f"[{submission.fullname}] Posted {reply.fullname} in response.")


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            logger.warning(e)
            time.sleep(10 * 60)
