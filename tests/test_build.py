import json
from pathlib import Path

import build


def test_good_timings_have_no_problems():
    clinics = json.loads(Path("site/clinic-timings.json").read_text())
    assert build.check_timings(clinics) == []


def test_bad_times_are_caught():
    bad = [{"name": "X", "open": "8:00", "close": "20:00"}, {"name": "Y", "open": "21:00", "close": "09:00"}]
    problems = build.check_timings(bad)
    assert any("not HH:MM" in p for p in problems) and any("opens at" in p for p in problems)


def test_build_writes_the_site_and_version(tmp_path):
    out = build.build("abc1234", "7", tmp_path / "dist")
    assert (out / "index.html").exists()
    assert json.loads((out / "version.json").read_text())["sha"] == "abc1234"
