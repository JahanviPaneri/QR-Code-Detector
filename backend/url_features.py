import re
from urllib.parse import urlparse, urlunparse

SUSPICIOUS_WORDS = [
    'login',
    'secure',
    'verify',
    'account',
    'update',
    'free',
    'bonus',
    'bank',
    'wallet',
    'gift',
]

FEATURE_COLUMNS = [
    'url_length',
    'num_dots',
    'num_hyphens',
    'num_digits',
    'num_special_chars',
    'has_https',
    'num_subdirs',
    'num_params',
    'has_ip_address',
    'tld_length',
    'contains_suspicious_words',
]


def normalize_url(raw: str) -> str:
    """
    Normalizes arbitrary QR payloads or URLs captured from CSV rows.
    Ensures we always return a lowercase scheme and trimmed string.
    """
    if raw is None:
        return ''

    url = str(raw).strip()
    # A lot of notebook exports keep "1234    http..." structure.
    if '\n' in url:
        url = url.split('\n', 1)[0]
    if '    http' in url:
        parts = url.split()
        # take last token that looks like a URL
        candidates = [p for p in parts if 'http' in p]
        if candidates:
            url = candidates[-1]

    # Ensure scheme
    parsed = urlparse(url, scheme='http')
    if not parsed.netloc and parsed.path:
        # Strings like "example.com/path" land in path
        parsed = urlparse(f'http://{url}')

    normalized = parsed._replace(scheme=parsed.scheme.lower() or 'http')
    return urlunparse(normalized)


def extract_features(url: str) -> dict:
    cleaned = normalize_url(url)
    parsed = urlparse(cleaned)
    domain = parsed.netloc or ''
    path = parsed.path or ''
    query = parsed.query or ''

    features = {
        'url_length': len(cleaned),
        'num_dots': cleaned.count('.'),
        'num_hyphens': cleaned.count('-'),
        'num_digits': sum(ch.isdigit() for ch in cleaned),
        'num_special_chars': sum(ch in '?=&%' for ch in cleaned),
        'has_https': 1 if cleaned.lower().startswith('https') else 0,
        'num_subdirs': max(path.count('/') - 1, 0),
        'num_params': query.count('='),
        'has_ip_address': 1
        if re.search(r'\b\d{1,3}(?:\.\d{1,3}){3}\b', domain)
        else 0,
        'tld_length': _tld_length(domain),
        'contains_suspicious_words': 1
        if any(word in cleaned.lower() for word in SUSPICIOUS_WORDS)
        else 0,
    }
    return features


def _tld_length(domain: str) -> int:
    match = re.search(r'\.([a-zA-Z0-9-]+)$', domain)
    return len(match.group(1)) if match else 0


__all__ = ['extract_features', 'FEATURE_COLUMNS', 'normalize_url']

