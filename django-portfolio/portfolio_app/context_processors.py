import os

SOCIAL_LINKS = [
    {'name': 'github', 'label': 'GitHub', 'url': 'https://github.com/OmDhamal-08'},
    {'name': 'linkedin', 'label': 'LinkedIn', 'url': 'https://www.linkedin.com/in/om-dhamal080405'},
    {'name': 'leetcode', 'label': 'LeetCode', 'url': 'https://leetcode.com/u/omdhamal77/'},
    {'name': 'codeforces', 'label': 'Codeforces', 'url': 'https://codeforces.com/profile/omdhamal'},
    {'name': 'x', 'label': 'X (Twitter)', 'url': 'https://x.com/OmDhamal5'},
    {'name': 'instagram', 'label': 'Instagram', 'url': 'https://www.instagram.com/dhamal_om_96/'},
]

CONTACT_EMAIL = 'dhamalomm@gmail.com'

# Opens a new message in Gmail on the web. A plain mailto: link does nothing on
# computers without a desktop email app, which is most of them.
GMAIL_COMPOSE_URL = f'https://mail.google.com/mail/?view=cm&fs=1&to={CONTACT_EMAIL}'


# Changes on every Vercel deploy, so browsers fetch fresh CSS/JS after an update.
ASSET_VERSION = os.environ.get('VERCEL_GIT_COMMIT_SHA', 'dev')[:8]


def site(request):
    """Values every template needs (footer, contact page, nav, link previews)."""
    site_url = f'{request.scheme}://{request.get_host()}'
    return {
        'site_url': site_url,                       # e.g. https://portfolio-five-nu-11.vercel.app
        'page_url': site_url + request.path,        # canonical URL of this page
        'social_links': SOCIAL_LINKS,
        'contact_email': CONTACT_EMAIL,
        'gmail_compose_url': GMAIL_COMPOSE_URL,
        'contact_location': 'Pune, India',
        'asset_version': ASSET_VERSION,
    }
