#!/usr/bin/env python3
"""Fetch and extract job posting content from URLs.

Usage:
    uv run scripts/fetch_job_posting.py <url> [--output <output_file>]
    uv run scripts/fetch_job_posting.py <url> --cache-dir ~/.cache/resume-jobs

Examples:
    uv run scripts/fetch_job_posting.py "https://linkedin.com/jobs/view/12345"
    uv run scripts/fetch_job_posting.py "https://indeed.com/..." --output job_desc.txt
"""

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

# Known JS-heavy job sites that may not work well with simple fetching
JS_HEAVY_SITES = {
    "linkedin.com": "LinkedIn requires JavaScript; consider copying job text manually",
    "lever.co": "Lever may require JavaScript rendering",
    "greenhouse.io": "Greenhouse may require JavaScript rendering",
    "workday.com": "Workday requires JavaScript; consider copying job text manually",
    "myworkdayjobs.com": "Workday requires JavaScript; consider copying job text manually",
    "icims.com": "iCIMS may require JavaScript rendering",
    "smartrecruiters.com": "SmartRecruiters may require JavaScript rendering",
}

# Default cache TTL in seconds (24 hours)
DEFAULT_CACHE_TTL = 86400


def get_cache_path(cache_dir: Path, url: str) -> Path:
    """Generate a cache file path for a URL."""
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
    domain = urlparse(url).netloc.replace(".", "_")
    return cache_dir / f"{domain}_{url_hash}.json"


def load_from_cache(cache_path: Path, ttl: int) -> str | None:
    """Load content from cache if valid."""
    if not cache_path.exists():
        return None

    try:
        data = json.loads(cache_path.read_text())
        cached_at = datetime.fromisoformat(data["cached_at"])
        age_seconds = (datetime.now(timezone.utc) - cached_at).total_seconds()

        if age_seconds < ttl:
            print(f"Using cached content (age: {int(age_seconds)}s)", file=sys.stderr)
            return data["content"]
        else:
            print(f"Cache expired (age: {int(age_seconds)}s, ttl: {ttl}s)", file=sys.stderr)
            return None
    except (json.JSONDecodeError, KeyError):
        return None


def save_to_cache(cache_path: Path, url: str, content: str) -> None:
    """Save content to cache."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "url": url,
        "content": content,
        "cached_at": datetime.now(timezone.utc).isoformat(),
    }
    cache_path.write_text(json.dumps(data, indent=2))


def check_js_heavy_site(url: str) -> str | None:
    """Check if URL is from a known JS-heavy site."""
    domain = urlparse(url).netloc.lower()
    for site, warning in JS_HEAVY_SITES.items():
        if site in domain:
            return warning
    return None


def fetch_with_retry(
    url: str,
    max_retries: int = 3,
    initial_delay: float = 1.0,
) -> str:
    """Fetch URL content with retry logic.

    Args:
        url: URL to fetch
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay between retries (doubles each retry)

    Returns:
        Fetched and cleaned content

    Raises:
        RuntimeError: If all retries fail
    """
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("Error: Required packages not available. Run: uv sync", file=sys.stderr)
        sys.exit(1)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    delay = initial_delay
    last_error = None

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove non-content elements
            for element in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
                element.decompose()

            # Get text
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)

            # Check for minimal content (may indicate JS-heavy site)
            if len(text) < 200:
                js_warning = check_js_heavy_site(url)
                if js_warning:
                    print(f"Warning: {js_warning}", file=sys.stderr)
                print(
                    "Warning: Extracted content is very short. "
                    "This may be a JavaScript-heavy site.",
                    file=sys.stderr,
                )

            return text

        except requests.exceptions.HTTPError as e:
            if e.response.status_code in (429, 503, 502, 504):
                # Retryable errors
                last_error = e
                if attempt < max_retries - 1:
                    print(
                        f"Retry {attempt + 1}/{max_retries} after {delay:.1f}s "
                        f"(HTTP {e.response.status_code})",
                        file=sys.stderr,
                    )
                    time.sleep(delay)
                    delay *= 2
                    continue
            raise RuntimeError(f"HTTP error: {e}")

        except requests.exceptions.Timeout:
            last_error = "Request timed out"
            if attempt < max_retries - 1:
                print(
                    f"Retry {attempt + 1}/{max_retries} after {delay:.1f}s (timeout)",
                    file=sys.stderr,
                )
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError("Request timed out after multiple retries")

        except requests.exceptions.ConnectionError as e:
            last_error = e
            if attempt < max_retries - 1:
                print(
                    f"Retry {attempt + 1}/{max_retries} after {delay:.1f}s (connection error)",
                    file=sys.stderr,
                )
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError(f"Connection error: {e}")

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request error: {e}")

    raise RuntimeError(f"All retries failed. Last error: {last_error}")


def fetch_job_posting(
    url: str,
    cache_dir: Path | None = None,
    cache_ttl: int = DEFAULT_CACHE_TTL,
    no_cache: bool = False,
    max_retries: int = 3,
) -> str:
    """Fetch job posting content from a URL.

    Args:
        url: Job posting URL
        cache_dir: Directory for caching (None to disable)
        cache_ttl: Cache time-to-live in seconds
        no_cache: If True, bypass cache
        max_retries: Maximum retry attempts

    Returns:
        Extracted job posting content
    """
    # Check JS-heavy site warning
    js_warning = check_js_heavy_site(url)
    if js_warning:
        print(f"Warning: {js_warning}", file=sys.stderr)

    # Try cache first
    cache_path = None
    if cache_dir and not no_cache:
        cache_path = get_cache_path(cache_dir, url)
        cached_content = load_from_cache(cache_path, cache_ttl)
        if cached_content:
            return cached_content

    # Fetch content
    content = fetch_with_retry(url, max_retries=max_retries)

    # Save to cache
    if cache_path:
        save_to_cache(cache_path, url, content)
        print(f"Cached to: {cache_path}", file=sys.stderr)

    return content


def main():
    parser = argparse.ArgumentParser(
        description="Fetch job posting from URL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run scripts/fetch_job_posting.py "https://example.com/jobs/123"
  uv run scripts/fetch_job_posting.py "https://example.com/jobs/123" -o job.txt
  uv run scripts/fetch_job_posting.py "https://example.com/jobs/123" --cache-dir ~/.cache/jobs

Known limitations:
  Some job sites (LinkedIn, Workday, Lever) require JavaScript rendering.
  For these sites, consider copying the job description text manually.
        """,
    )
    parser.add_argument("url", help="Job posting URL")
    parser.add_argument("-o", "--output", type=Path, help="Output file path (default: stdout)")
    parser.add_argument(
        "--cache-dir",
        type=Path,
        help="Cache directory (default: no caching)",
    )
    parser.add_argument(
        "--cache-ttl",
        type=int,
        default=DEFAULT_CACHE_TTL,
        help=f"Cache TTL in seconds (default: {DEFAULT_CACHE_TTL})",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Bypass cache even if cache-dir is set",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Maximum retry attempts (default: 3)",
    )

    args = parser.parse_args()

    try:
        content = fetch_job_posting(
            args.url,
            cache_dir=args.cache_dir,
            cache_ttl=args.cache_ttl,
            no_cache=args.no_cache,
            max_retries=args.retries,
        )

        if args.output:
            args.output.write_text(content)
            print(f"Job posting content written to: {args.output}", file=sys.stderr)
        else:
            print(content)

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
