"""Render assets/stats.svg: GitHub stats as an animated terminal. Run by .github/workflows/profile.yml."""
import json, os, sys, urllib.request
from datetime import date, timedelta
from term import term, R, P, G, D, Wt

USER = os.environ.get("GH_USER", "CarlosZambonii")
QUERY = """
query($login: String!) {
  user(login: $login) {
    pullRequests { totalCount }
    merged: pullRequests(states: MERGED) { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      totalCount
      nodes { stargazerCount }
    }
    contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}"""


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}"},
    )
    data = json.load(urllib.request.urlopen(req))
    if "errors" in data:
        sys.exit(data["errors"])
    return data["data"]["user"]


def streaks(days):
    counts = {d["date"]: d["contributionCount"] for w in days for d in w["contributionDays"]}
    best = run = 0
    for d in sorted(counts):
        run = run + 1 if counts[d] else 0
        best = max(best, run)
    cur, d = 0, date.today()
    if not counts.get(d.isoformat()):  # today not over yet
        d -= timedelta(days=1)
    while counts.get(d.isoformat()):
        cur, d = cur + 1, d - timedelta(days=1)
    return cur, best


def main(out):
    u = fetch()
    cal = u["contributionsCollection"]["contributionCalendar"]
    cur, best = streaks(cal["weeks"])
    repos = u["repositories"]
    stars = sum(r["stargazerCount"] for r in repos["nodes"])

    def stat(label, value, extra=""):
        return [("[*] ", P), (f"{label:<26}", D), (value, Wt), (extra, G)]

    body = [
        stat("contributions (1y)", f"{cal['totalContributions']:,}"),
        stat("current streak", f"{cur} day{'' if cur == 1 else 's'}", f"   longest {best}"),
        stat("pull requests", f"{u['pullRequests']['totalCount']}", f"   merged {u['merged']['totalCount']}"),
        stat("repositories", f"{repos['totalCount']}", f"   ★ {stars} stars"),
        [],
        [("[+] ", R), ("scan complete", Wt), (f" · updated {date.today().isoformat()}", G)],
    ]
    term(out, "~", f"./stats.sh --user {USER}", body, T=14.0)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assets/stats.svg")
