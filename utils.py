import re

import requests
from bs4 import BeautifulSoup
from praw.models import Comment, Submission

AMP_REGEX = re.compile(
    r"http(|s)://(|.+\.)(?<!(developer)\.)google\.[a-z.]+/amp/(?:s/)?(.*)", re.IGNORECASE | re.MULTILINE
    #r"google[a-z.]+/amp/(?:s/)?(.*)", re.IGNORECASE | re.MULTILINE
)  # https://regex101.com/r/92WOyk/1


def is_amp_url(text):
    matches = re.findall(AMP_REGEX, text)

    if len(matches) == 1:
        return matches[0]
    else:
        return False


def get_canonical_url_and_title_for(url):
    body = requests.get(url)
    soup = BeautifulSoup(body.text, "html.parser")

    title = soup.find("title")
    canonical = soup.find("link", {"rel": "canonical"})

    if canonical is None or title is None:
        return (None, None)

    return (title.get_text(), canonical["href"])


def find_urls_in(obj):
    if isinstance(obj, Submission):
        submission = obj

        if submission.permalink not in submission.url:
            return [submission.url]
        elif submission.selftext_html is not None:
            soup = BeautifulSoup(submission.selftext_html, "html.parser")
            urls = [a["href"] for a in soup.find_all("a")]

            if urls != []:
                return urls
            else:
                return None
        else:
            return None
    elif isinstance(obj, Comment):
        comment = obj

        soup = BeautifulSoup(comment.body_html, "html.parser")
        urls = [a["href"] for a in soup.find_all("a")]

        if urls != []:
            return urls
        else:
            return None
    else:
        return None
