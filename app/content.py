"""Owner-approved identity. Pending skills/projects are labeled in the template."""

PROFILE = {
    "name": "Zhivko Petkov",
    "first_name": "Zhivko",
    "last_name": "Petkov",
    "role": "Cybersecurity student",
    "github": "https://github.com/nvm0r",
    "handle": "nvm0r",
    "email": "zhivkop3@gmail.com",
}

# A project learning roadmap, not a claim of proficiency or certification.
SKILLS = [
    {"id": "01", "symbol": "[>_]", "title": "Backend & scripting", "tools": ["Python", "Flask", "pytest"], "state": "IN THIS BUILD"},
    {"id": "02", "symbol": "{ / }", "title": "Cloud & infrastructure", "tools": ["AWS", "Terraform", "ECR"], "state": "PROJECT ROADMAP"},
    {"id": "03", "symbol": "↳ ☐", "title": "Delivery & automation", "tools": ["Docker", "GitHub Actions", "Git"], "state": "PROJECT ROADMAP"},
]
