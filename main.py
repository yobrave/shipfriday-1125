import json
import os
from pathlib import Path

RULES = {"limit": 159, "artifact": "entry.txt", "owner": "yobrave"}
LABEL = "friday-commit-runner"


def primary(blob):
    found = list(filter(str.strip, blob.replace("\r", "").split("\n")))
    return found[0].strip() if found else ""


def flow():
    origin = Path(__file__).resolve().parent / RULES["artifact"]
    if not origin.exists():
        return {"phase": "missing", "label": LABEL}
    msg = primary(origin.read_text(encoding="utf-8"))
    if not msg:
        return {"phase": "blank", "label": LABEL}
    if len(msg) > RULES["limit"]:
        return {"phase": "overflow", "label": LABEL, "chars": len(msg)}
    base = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    base.mkdir(parents=True, exist_ok=True)
    with open(base / RULES["artifact"], "w", encoding="utf-8", newline="\n") as fh:
        fh.write(msg)
    return {"phase": "committed", "label": LABEL, "chars": len(msg),
            "owner": RULES["owner"], "run": "r21-1930"}


if __name__ == "__main__":
    outcome = flow()
    print(json.dumps(outcome))
    raise SystemExit(0 if outcome["phase"] == "committed" else 1)
