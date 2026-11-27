"""Live coding stats from LeetCode, GitHub and Codeforces.

The home page loads these after it has rendered (HTMX), so a slow API never
slows the page. Results are cached for a day, and if a service is down the
last good numbers (or the fallbacks below) are shown instead of an error.
"""
import json
import logging
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from django.core.cache import cache

logger = logging.getLogger(__name__)

LEETCODE_USER = 'omdhamal77'
GITHUB_USER = 'OmDhamal-08'
CODEFORCES_USER = 'omdhamal'

CACHE_KEY = 'coding-stats'
LAST_GOOD_KEY = 'coding-stats:last-good'
CACHE_SECONDS = 24 * 60 * 60
TIMEOUT = 4
USER_AGENT = 'portfolio-coding-stats/1.0'

# Shown only if a service has never answered on this server (numbers from Nov 2026).
FALLBACK = {
    'leetcode': {'solved': 297, 'easy': 194, 'medium': 99, 'hard': 4},
    'github': {'contributions': 234, 'repos': 23},
    'codeforces': {'rating': 847, 'max_rating': 869},
}


def _get_json(url, data=None, headers=None):
    request = urllib.request.Request(url, data=data, headers={'User-Agent': USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return json.loads(response.read().decode('utf-8'))


def fetch_leetcode():
    query = {
        'query': 'query($u: String!) { matchedUser(username: $u) { submitStatsGlobal { acSubmissionNum { difficulty count } } } }',
        'variables': {'u': LEETCODE_USER},
    }
    data = _get_json(
        'https://leetcode.com/graphql',
        data=json.dumps(query).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Referer': 'https://leetcode.com'},
    )
    counts = {row['difficulty'].lower(): row['count']
              for row in data['data']['matchedUser']['submitStatsGlobal']['acSubmissionNum']}
    return {'solved': counts['all'], 'easy': counts['easy'], 'medium': counts['medium'], 'hard': counts['hard']}


def fetch_github():
    user = _get_json(f'https://api.github.com/users/{GITHUB_USER}')
    calendar = _get_json(f'https://github-contributions-api.jogruber.de/v4/{GITHUB_USER}?y=last')
    return {'contributions': calendar['total']['lastYear'], 'repos': user['public_repos']}


def fetch_codeforces():
    data = _get_json(f'https://codeforces.com/api/user.info?handles={CODEFORCES_USER}')
    user = data['result'][0]
    return {'rating': user.get('rating', 0), 'max_rating': user.get('maxRating', 0)}


FETCHERS = {'leetcode': fetch_leetcode, 'github': fetch_github, 'codeforces': fetch_codeforces}


def get_coding_stats():
    """Stats for the template, from cache when possible. Never raises."""
    stats = cache.get(CACHE_KEY)
    if stats is not None:
        return stats

    last_good = cache.get(LAST_GOOD_KEY) or FALLBACK
    stats = {}
    with ThreadPoolExecutor(max_workers=len(FETCHERS)) as pool:
        futures = {name: pool.submit(fetch) for name, fetch in FETCHERS.items()}
        for name, future in futures.items():
            try:
                stats[name] = future.result()
            except Exception:
                logger.warning('Could not fetch %s stats; using the last known numbers', name, exc_info=True)
                stats[name] = last_good[name]

    cache.set(LAST_GOOD_KEY, stats, None)  # keep forever as the fallback
    cache.set(CACHE_KEY, stats, CACHE_SECONDS)
    return stats
