import os
import yaml
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

SOFTWARE_INPUT = "_data/software.yml"
CACHE_FILE = "_data/package_downloads.yml"
CACHE_MAX_AGE_DAYS = 30
PYPI_ENDPOINT = "https://api.pepy.tech/api/v2/projects/{}"
GITHUB_ENDPOINT = "https://api.github.com/repos/{}/{}"


def load_software():
    with open(SOFTWARE_INPUT, "r") as f:
        return yaml.safe_load(f)


def get_pypi_downloads(package, api_key):
    r = requests.get(
        PYPI_ENDPOINT.format(package),
        headers={"X-Api-Key": api_key},
    )
    r.raise_for_status()
    return r.json()["total_downloads"]


def get_github_stars(user, repo, token=None):
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.get(GITHUB_ENDPOINT.format(user, repo), headers=headers)
    r.raise_for_status()
    return r.json()["stargazers_count"]


def cache_is_fresh():
    path = Path(CACHE_FILE)
    if not path.exists():
        return False
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    return datetime.now() - mtime < timedelta(days=CACHE_MAX_AGE_DAYS)


def fetch_and_cache():
    software = load_software()
    pepy_api_key = os.environ.get("PEPY_API_KEY") or input("PEPY_API_KEY: ")
    github_token = os.environ.get("GITHUB_TOKEN")  # optional, raises rate limit

    data: dict = {"updated": datetime.now().strftime("%Y-%m-%d"), "pypi": {}, "github_stars": {}}

    for item in software:
        if "pypi" in item:
            pkg = item["pypi"]
            count = get_pypi_downloads(pkg, pepy_api_key)
            data["pypi"][pkg] = count
            print(f"PyPI {pkg}: {count:,}")

        if "user" in item and "repo" in item:
            key = f"{item['user']}/{item['repo']}"
            stars = get_github_stars(item["user"], item["repo"], github_token)
            data["github_stars"][key] = stars
            print(f"GitHub {key}: {stars:,} stars")

    with open(CACHE_FILE, "w") as f:
        yaml.dump(data, f)
    return data


def load_cache():
    with open(CACHE_FILE, "r") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    if cache_is_fresh():
        print(f"Cache is less than {CACHE_MAX_AGE_DAYS} days old, skipping fetch.")
        data = load_cache()
    else:
        data = fetch_and_cache()

    print(f"\nData as of {data['updated']}:")
    for pkg, count in data.get("pypi", {}).items():
        print(f"  PyPI {pkg}: {count:,}")
    for repo, stars in data.get("github_stars", {}).items():
        print(f"  GitHub {repo}: {stars:,} stars")
