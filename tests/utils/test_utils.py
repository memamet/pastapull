from src.utils.utils import is_open_source, get_first_line_of_readme


def test_valid_open_source_repo():
    assert is_open_source("https://github.com/psf/requests") == True


def test_non_open_source_repo():
    # Testing with a repo that is not open-source or has no license
    # You can replace this with an actual repo known to be closed-source
    assert is_open_source("https://github.com/someone/non_open_source_repo") == False


def test_non_github_url():
    assert is_open_source("https://gitlab.com/someuser/somerepo") == False


def test_invalid_github_url():
    assert is_open_source("https://github.com/invalid/repo") == False


def test_github_repo_without_license():
    assert is_open_source("https://github.com/someone/repo_without_license") == False


def test_get_first_line_of_readme_valid_repo():
    first_line = get_first_line_of_readme("https://github.com/psf/requests")
    assert first_line.startswith("# Requests")


def test_get_first_line_of_readme_non_github_url():
    first_line = get_first_line_of_readme("https://gitlab.com/someuser/somerepo")
    assert first_line == ""


def test_get_first_line_of_readme_invalid_github_url():
    first_line = get_first_line_of_readme("https://github.com/invalid/repo")
    assert first_line == ""


def test_get_first_line_of_readme_repo_without_readme():
    first_line = get_first_line_of_readme(
        "https://github.com/someone/repo_without_readme"
    )
    assert first_line == ""
