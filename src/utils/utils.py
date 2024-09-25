import requests
from dataclasses import dataclass
from urllib.parse import urlparse
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import base64
from dotenv import load_dotenv
import os

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
    parsed_url = urlparse(url)
    if "github.com" not in parsed_url.netloc:
        print("This is not a GitHub repository URL.")
        return ""

    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts) < 2:
        print("Invalid GitHub repository URL.")
        return ""

    owner, repo = path_parts[:2]

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


def query_github_api(url: str) -> str:
    parsed_url = urlparse(url)
    if "github.com" not in parsed_url.netloc:
        print("This is not a GitHub repository URL.")
        return ""

    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts) < 2:
        print("Invalid GitHub repository URL.")
        return ""

    owner, repo = path_parts[:2]
    readme_api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"

    try:
        readme_response = requests.get(readme_api_url)
        if readme_response.status_code == 200:
            readme_data = readme_response.json()
            readme_content = base64.b64decode(readme_data["content"]).decode("utf-8")

            return readme_content
        else:
            print("No README found.")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""


PROMPT_TEMPLATE = """
You are a helpful assistant that improves the README.md file of a GitHub repository.

You make sure the readme explains clearly what the project does, how to use it, and any important information about the project.

You also make sure the readme is well-structured and easy to read, with clear headings and subheadings.
You will add a lot of citation by famous computer scientists and engineers or anyone that is known by the greater tech and computer science community.
These citations but be formatted as quotes in Markdown.
Here is the current README.md file:

{readme}
"""

MODEL_TO_USE = "gpt-4o-mini"
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


@dataclass
class QueryResponse:
    original_readme: str
    improved_readme: str
    llm_used: str


def query_llm_to_improve_readme(url: str) -> QueryResponse:
    original_readme = query_github_api(url)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = ChatOpenAI(model_name=MODEL_TO_USE, temperature=0.1, api_key=OPENAI_API_KEY)
    chain = {"readme": RunnablePassthrough()} | prompt | llm | StrOutputParser()
    improved_readme = chain.invoke(original_readme)
    print(f"Improved README:\n{improved_readme}")

    return QueryResponse(
        original_readme=original_readme,
        improved_readme=improved_readme,
        llm_used=MODEL_TO_USE,
    )


if __name__ == "__main__":
    query_llm_to_improve_readme("https://github.com/psf/requests")
