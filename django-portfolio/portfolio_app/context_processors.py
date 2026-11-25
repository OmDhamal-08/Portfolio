SOCIAL_LINKS = [
    {'name': 'github', 'label': 'GitHub', 'url': 'https://github.com/OmDhamal-08'},
    {'name': 'linkedin', 'label': 'LinkedIn', 'url': 'https://www.linkedin.com/in/om-dhamal-411545295/'},
    {'name': 'leetcode', 'label': 'LeetCode', 'url': 'https://leetcode.com/u/omdhamal77/'},
    {'name': 'codeforces', 'label': 'Codeforces', 'url': 'https://codeforces.com/profile/omdhamal'},
    {'name': 'x', 'label': 'X (Twitter)', 'url': 'https://x.com/OmDhamal5'},
    {'name': 'instagram', 'label': 'Instagram', 'url': 'https://www.instagram.com/dhamal_om_96/'},
]


def site(request):
    """Values every template needs (footer, contact page, nav)."""
    return {
        'social_links': SOCIAL_LINKS,
        'contact_email': 'dhamalom@gmail.com',
        'contact_location': 'Pune, India',
    }
