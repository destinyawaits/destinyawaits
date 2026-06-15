import json
import os
import urllib.request

USERNAME = os.environ["GITHUB_USERNAME"]
TOKEN = os.environ["GITHUB_TOKEN"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    pinnedItems(first: 6, types: REPOSITORY) {
      nodes {
        ... on Repository {
          name
          description
          url
          homepageUrl
          stargazerCount
          primaryLanguage {
            name
          }
        }
      }
    }
  }
}
"""

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({
        "query": QUERY,
        "variables": {"login": USERNAME}
    }).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": USERNAME,
    },
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode("utf-8"))

repos = data["data"]["user"]["pinnedItems"]["nodes"]

cards = []
for repo in repos:
    name = repo["name"]
    desc = repo["description"] or "No description provided."
    url = repo["url"]
    lang = repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "N/A"
    stars = repo["stargazerCount"]
    live = repo["homepageUrl"]

    extra = f" · ⭐ {stars} · {lang}"
    live_link = f' · [Live]({live})' if live else ""

    cards.append(
        f"""<a href="{url}" target="_blank">
  <img src="https://github-readme-stats.vercel.app/api/pin/?username={USERNAME}&repo={name}&hide_border=true&theme=tokyonight" />
</a>

**[{name}]({url})** — {desc}{extra}{live_link}
"""
    )

content = "\n".join(cards)

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

start = "<!-- featured-projects:start -->"
end = "<!-- featured-projects:end -->"

before = readme.split(start)[0]
after = readme.split(end)[1]

updated = before + start + "\n" + content + "\n" + end + after

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated)
