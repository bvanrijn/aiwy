import praw
from praw.models import Comment, Submission

import env
from utils import find_urls_in

reddit = praw.Reddit(
    client_id=env.client_id,
    client_secret=env.client_secret,
    password=env.password,
    user_agent=env.user_agent,
    username=env.username,
)


class TestFindURLsFunction(object):
    def test_submission_that_has_url(self):
        submission = Submission(
            reddit,
            url="https://www.reddit.com/r/worldnews/comments/98aj0i/former_un_chief_kofi_annan_dies_at_80/",
        )

        assert find_urls_in(submission) == [
            "http://www.bbc.co.uk/news/world-africa-45232892"
        ]

    def test_submission_that_no_has_url(self):
        submission = Submission(
            reddit,
            url="https://www.reddit.com/r/macbookpro/comments/98a0r1/macbook_pro_15_2018_doesnt_wake_up_properly/",
        )

        assert find_urls_in(submission) is None

    def test_self_submission_that_has_url(self):
        submission = Submission(
            reddit,
            url="https://www.reddit.com/r/hiphopheads/comments/9897up/kodak_black_has_just_been_released_from_prison/",
        )

        assert find_urls_in(submission) == [
            "https://www.instagram.com/p/Bmm4J9OgL16/?tagged=kodakblack"
        ]

    def test_self_submission_that_has_urls(self):
        submission = Submission(
            reddit,
            url="https://www.reddit.com/r/IAmA/comments/982pur/iama_saturation_diver_aquanaut_who_has_spent_30/",
        )

        assert find_urls_in(submission) == [
            "https://www.atlasobscura.com/articles/what-is-a-saturation-diver",
            "https://www.gofundme.com/shannonhoveysbandp",
            "https://www.youtube.com/watch?v=SbAxa-_3h6E",
            "https://www.youtube.com/watch?v=slq9lkHWs0I",
            "https://twitter.com/atlasobscura/status/1030197554548539392",
        ]

    def test_self_submission_no_has_text_no_has_url(self):
        submission = Submission(
            reddit,
            url="https://www.reddit.com/r/AskReddit/comments/989eg1/what_real_event_in_your_life_had_it_happened_in_a/",
        )

        assert find_urls_in(submission) is None

    def test_comment_no_has_url(self):
        comment = Comment(
            reddit,
            url="https://www.reddit.com/r/worldnews/comments/98aj0i/former_un_chief_kofi_annan_dies_at_80/e4en2bt/",
        )

        assert find_urls_in(comment) is None

    def test_comment_has_url(self):
        comment = Comment(
            reddit,
            url="https://www.reddit.com/r/worldnews/comments/986846/ukraine_demands_15_year_sentence_for_ousted/e4dqaw1/",
        )

        assert find_urls_in(comment) == [
            "https://www.businessinsider.com/paul-manafort-daughter-text-messages-ukraine-2017-3"
        ]

    def test_comment_has_urls(self):
        comment = Comment(
            reddit,
            url="https://www.reddit.com/r/worldnews/comments/98aq8n/new_paper_shows_that_ants_are_so_productive/e4ek8my/",
        )

        assert find_urls_in(comment) == [
            "https://www.nytimes.com/2018/08/16/science/ants-worker-idleness.html",
            "http://np.reddit.com/r/autotldr/comments/98aw7d/new_paper_shows_that_ants_are_so_productive/",
            "http://np.reddit.com/r/autotldr/comments/31b9fm/faq_autotldr_bot/",
            "http://np.reddit.com/message/compose?to=%23autotldr",
        ]
