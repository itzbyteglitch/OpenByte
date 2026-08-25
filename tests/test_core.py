from pathlib import Path

def test_project_layout():
    root=Path(__file__).parents[1]
    assert (root/"pyproject.toml").exists()
    assert (root/"src/openbyte/agent.py").exists()
    assert (root/"src/openbyte/tools.py").exists()

def test_skill_files_exist():
    assert list((Path(__file__).parents[1]/"src/openbyte/builtin_skills").rglob("SKILL.md"))
