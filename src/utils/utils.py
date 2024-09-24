import requests
from urllib.parse import urlparse
import base64

# List of open-source licenses
OPEN_SOURCE_LICENSES = [
    "MIT",
    "Apache-2.0",
    "GPL-3.0",
    "GPL-2.0",
    "LGPL-2.1",
    "LGPL-3.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "MPL-2.0",
    "EPL-1.0",
]


def is_open_source(url: str) -> bool:
    # Parse the GitHub URL to extract the owner and repo name
    parsed_url = urlparse(url)
    if "github.com" not in parsed_url.netloc:
        print("This is not a GitHub repository URL.")
        return False

    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts) < 2:
        print("Invalid GitHub repository URL.")
        return False

    owner, repo = path_parts[:2]

    # Check the license
    license_api_url = f"https://api.github.com/repos/{owner}/{repo}/license"
    license_response = requests.get(license_api_url)
    if license_response.status_code == 200:
        license_data = license_response.json()
        license_name = license_data.get("license", {}).get("spdx_id", "")
        if license_name in OPEN_SOURCE_LICENSES:
            print(f"License: {license_name} (Open Source)")
            return True
        else:
            print(f"License: {license_name} (Not Open Source)")
            return False
    else:
        print("No license found.")
        return False


def get_first_line_of_readme(url: str) -> str:
    # Parse the GitHub URL to extract the owner and repo name
    parsed_url = urlparse(url)
    if "github.com" not in parsed_url.netloc:
        print("This is not a GitHub repository URL.")
        return ""

    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts) < 2:
        print("Invalid GitHub repository URL.")
        return ""

    owner, repo = path_parts[:2]

    # Fetch the README file and return the first line
    readme_api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    readme_response = requests.get(readme_api_url)
    if readme_response.status_code == 200:
        readme_data = readme_response.json()
        readme_content = base64.b64decode(readme_data["content"]).decode("utf-8")
        first_line = readme_content.splitlines()[0]
        print(f"First line of README: {first_line}")
        return first_line
    else:
        print("No README found.")
        return ""
