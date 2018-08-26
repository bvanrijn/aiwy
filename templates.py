from urllib.parse import quote

COMPOSE_BODY = """If you click 'send' below, the following action will be taken:

* {action}

You will receive a confirmation in reply."""

BOT_IGNORE_ACTION = "The bot will ignore you"
BOT_UNIGNORE_ACTION = "The bot will no longer ignore you"


def make_subscript(text):
    return "&#32;".join(text.split())


def link(text, href):
    return f"[{text}]({href})"


def make_comment_text(ut):
    ignore_message = COMPOSE_BODY.format(action=BOT_IGNORE_ACTION)

    footer = "---\n^^" + make_subscript(
        "I'm a bot - {why} - {ignore}".format(
            why=link(
                "Why?",
                "https://np.reddit.com/user/amp-is-watching-you/comments/970p7j/why_did_i_build_this_bot/",
            ),
            ignore=link(
                "Ignore me",
                f"https://np.reddit.com/message/compose/?to=amp-is-watching-you&subject=ignore&message={quote(ignore_message)}",
            ),
        )
    )

    if len(ut) == 1:
        url = list(ut.keys())[0]

        comment = f"**Direct link**: {url}\n\n{footer}"

        return comment
    else:
        comment = "**Direct links**:\n\n"

        for url in ut:
            title = ut[url]

            comment += f"* {link(title, url)}\n"

        comment += "\n" + footer

        return comment


BOT_IGNORE = """The bot will ignore you from now on.

{}""".format(
    link(
        "Click here if you change your mind",
        "https://www.reddit.com/message/compose/?to=amp-is-watching-you&subject=unignore&message={}".format(
            quote(COMPOSE_BODY.format(action=BOT_UNIGNORE_ACTION))
        ),
    )
)

BOT_UNIGNORE = """Welcome back! The bot will no longer ignore you.

{}""".format(
    link(
        "Click here if you change your mind",
        "https://www.reddit.com/message/compose/?to=amp-is-watching-you&subject=ignore&message={}".format(
            quote(COMPOSE_BODY.format(action=BOT_IGNORE_ACTION))
        ),
    )
)
