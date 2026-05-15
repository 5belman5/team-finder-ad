# Field lengths
MAX_LENGTH_NAME = 124
MAX_LENGTH_SURNAME = 124
MAX_LENGTH_PHONE = 15  # Standard international phone length
MAX_LENGTH_ABOUT = 256
MAX_LENGTH_PROJECT_NAME = 200
MAX_LENGTH_SKILL_NAME = 124

# Project statuses
STATUS_OPEN = "open"
STATUS_CLOSED = "closed"
STATUS_CHOICES = [
    (STATUS_OPEN, "Open"),
    (STATUS_CLOSED, "Closed"),
]

# Pagination
PAGINATION_PAGE_SIZE = 12
SKILLS_AUTOCOMPLETE_LIMIT = 10

# External URLs
GITHUB_DOMAIN = "github.com"

# Avatar generation
AVATAR_SIZE = (200, 200)
AVATAR_FONT_SIZE = 120
AVATAR_FONT_NAME = "arial.ttf"
AVATAR_TEXT_COLOR = "white"
AVATAR_ANCHOR_OFFSET = 10

# Developer info
TEAM_FINDER_AUTHOR = "Ivan Mesheryakov"
DEVELOPER_GITHUB = "https://github.com/5belman5"
DEVELOPER_EMAIL = "belvanic2000@gmail.com"
