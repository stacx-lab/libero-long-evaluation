"""Verify published task coverage, local resources, and asset integrity."""

import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "publication-manifest.json").read_text())
    data = json.loads((root / "data.json").read_text())
    tasks = data["tasks"]
    assert len(tasks) == manifest["expected_tasks"] == 10
    assert {task["task_id"] for task in tasks} == set(range(10))
    assert all(task["completed"] and task["edited"] for task in tasks)
    assert sum(task["native_success"] is True for task in tasks) == 7
    assert sum(task["native_success"] is False for task in tasks) == 3
    assert data["final"] and not data["montage"]
    assert "all-10-tasks.mp4" not in (root / "index.html").read_text()
    for entry in manifest["files"]:
        path = root / entry["path"]
        assert path.is_file() and not path.is_symlink(), entry["path"]
        assert path.stat().st_size == entry["bytes"], entry["path"]
        assert hashlib.file_digest(path.open("rb"), "sha256").hexdigest() == entry["sha256"], entry["path"]
        if entry["path"].endswith(".mp4"):
            assert entry["sha256"] == entry["original_sha256"], entry["path"]
        assert path.stat().st_size < 100 * 1024**2, entry["path"]
    for task in tasks:
        task_id = task["id"]
        required = [
            f"edited/{task_id}.mp4",
            f"edited/{task_id}.jpg",
            f"edited/{task_id}.json",
            f"raw/{task_id}/camera.mp4",
            f"raw/{task_id}/camera_wrist.mp4",
            f"evidence/{task_id}/session.txt",
            f"evidence/{task_id}/summary.json",
        ]
        analysis = task["analysis"]
        assert analysis["root_cause"] and analysis["evidence"], task_id
        for key in ("verification_receipt", "contact_audit", "diagnostic_image", "diagnostic_plot", "diagnostic_evidence"):
            if analysis.get(key):
                required.append(analysis[key])
        for relative in required:
            assert (root / relative).is_file(), relative
    for entry in manifest["excluded"]:
        assert not (root / entry["path"]).exists(), entry["path"]
    videos = list(root.glob("edited/*.mp4")) + list(root.glob("raw/*/*.mp4"))
    assert len(videos) == 30
    print(json.dumps({"passed": True, "tasks": 10, "successes": 7, "failures": 3,
                      "individual_videos": len(videos), "verified_files": len(manifest["files"])}))


if __name__ == "__main__":
    main()
