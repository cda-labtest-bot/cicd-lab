"""Build the Ankura clinic timings site into dist/: check the data first, then copy the site and write version.json."""
import argparse, json, re, shutil, sys, time
from pathlib import Path

SITE = Path("site")
DATA = "clinic-timings.json"
TIME = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


def check_timings(clinics):
    """Return the problems in the clinic timings (an empty list means the data is good)."""
    problems, seen = [], set()
    for c in clinics:
        name = c.get("name", "?")
        if name in seen:
            problems.append(f"{name}: listed twice")
        seen.add(name)
        bad = [k for k in ("open", "close") if not TIME.match(str(c.get(k, "")))]
        problems += [f"{name}: {k} time {c.get(k)!r} is not HH:MM" for k in bad]
        if not bad and c["open"] >= c["close"]:
            problems.append(f"{name}: opens at {c['open']} but closes at {c['close']}")
    return problems


def sorted_clinics(clinics):
    """Clinics in the order the page shows them: the earliest opening first."""
    return sorted(clinics, key=lambda c: c["open"])


def build(sha, run, out=Path("dist")):
    clinics = json.loads((SITE / DATA).read_text())
    problems = check_timings(clinics)
    if problems:
        sys.exit("timings.json has problems:\n  " + "\n  ".join(problems))
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(SITE, out)
    (out / DATA).write_text(json.dumps(sorted_clinics(clinics), indent=1))
    (out / "version.json").write_text(json.dumps({"sha": sha, "run": run, "built": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}))
    return out


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--sha", default="local")
    a.add_argument("--run", default="0")
    args = a.parse_args()
    print("built", build(args.sha, args.run))
