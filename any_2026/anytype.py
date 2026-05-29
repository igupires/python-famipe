ANYTYPE_API_URL = "http://localhost:31009/v1"
API_KEY = "V9urdzemJuuS6XwGkV+WKrrNwHSIwNlDrda9y2+cxxM="                               # Generated via Anytype Desktop settings
SPACE_ID = "bafyreibkfsneau3vpzul67sjuebk3wecwixzdfalukby2qfn3v6m6s52tu.3mqqvx2xvcae8" # The target Space ID
JIRA_BASE_URL = "https://projetos-levty.atlassian.net/browse/"                         # Base URL for Jira
ANYTYPE_VERSION = "2025-05-20"

# key of the sprint tag in Anytype
TAG_DICT = {
    "Sprint 01 - Back Office ACL": "sprint_01",
    "Sprint 02 - Back Office ACL": "sprint_02",
    "Sprint 03 - Back Office ACL": "sprint_03",
    "Sprint 04 - Back Office ACL": "sprint_04",
    "Sprint 05 - Back Office ACL": "sprint_05",
}

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

CREATE_URL = f"{ANYTYPE_API_URL}/spaces/{SPACE_ID}/objects"
SEARCH_URL = f"{ANYTYPE_API_URL}/spaces/{SPACE_ID}/search"
FILE_URL   = f"{ANYTYPE_API_URL}/spaces/{SPACE_ID}/files"