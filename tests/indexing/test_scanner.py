from pathlib import Path

from slopo.indexing.scanner import scan_directory

_JAVA = """\
class Calculator {
    int increment(int a) {
        return a + 1;
    }
}
"""

_KOTLIN = """\
fun increment(a: Int): Int {
    return a + 1
}
"""


def test_scans_all_supported_languages(tmp_path: Path):
    (tmp_path / "Calculator.java").write_text(_JAVA)
    (tmp_path / "Increment.kt").write_text(_KOTLIN)

    scanned = {
        sf.path: sf
        for sf in scan_directory(tmp_path, body_node_count_threshold=0, exclude=[])
    }

    assert set(scanned) == {Path("Calculator.java"), Path("Increment.kt")}
    assert [u.name for u in scanned[Path("Calculator.java")].units] == ["increment"]
    assert [u.name for u in scanned[Path("Increment.kt")].units] == ["increment"]


def test_recurses_into_subdirectories_with_paths_relative_to_root(tmp_path: Path):
    (tmp_path / "sub" / "nested").mkdir(parents=True)
    (tmp_path / "sub" / "nested" / "Increment.kt").write_text(_KOTLIN)

    scanned = list(scan_directory(tmp_path, body_node_count_threshold=0, exclude=[]))

    assert [sf.path for sf in scanned] == [Path("sub", "nested", "Increment.kt")]


def test_ignores_unsupported_file_types(tmp_path: Path):
    (tmp_path / "notes.txt").write_text("not code")
    (tmp_path / "data.json").write_text("{}")

    assert list(scan_directory(tmp_path, body_node_count_threshold=0, exclude=[])) == []


def test_excludes_units_below_body_node_count_threshold(tmp_path: Path):
    (tmp_path / "Calculator.java").write_text(_JAVA)

    scanned = list(scan_directory(tmp_path, body_node_count_threshold=1000, exclude=[]))

    assert scanned[0].units == []


def test_excludes_units_exceeding_max_body_chars(tmp_path: Path):
    big_body = "\n".join(f"        int x{i} = {i};" for i in range(500))
    assert len(big_body) == 11779
    source = (
        "class Big {\n"
        "    void huge() {\n"
        f"{big_body}\n"
        "    }\n"
        "    int small(int a) {\n"
        "        return a + 1;\n"
        "    }\n"
        "}\n"
    )
    (tmp_path / "Big.java").write_text(source)

    scanned = list(scan_directory(tmp_path, body_node_count_threshold=0, exclude=[]))

    assert [u.name for u in scanned[0].units] == ["small"]


def test_skips_files_under_excluded_directory(tmp_path: Path):
    (tmp_path / "build").mkdir()
    (tmp_path / "build" / "Generated.kt").write_text(_KOTLIN)
    (tmp_path / "Increment.kt").write_text(_KOTLIN)

    scanned = scan_directory(tmp_path, body_node_count_threshold=0, exclude=["build/"])

    assert [sf.path for sf in scanned] == [Path("Increment.kt")]


def test_skips_files_matching_glob_pattern(tmp_path: Path):
    (tmp_path / "Increment.gen.kt").write_text(_KOTLIN)
    (tmp_path / "Increment.kt").write_text(_KOTLIN)

    scanned = scan_directory(
        tmp_path, body_node_count_threshold=0, exclude=["*.gen.kt"]
    )

    assert [sf.path for sf in scanned] == [Path("Increment.kt")]


def test_negation_pattern_reincludes_excluded_file(tmp_path: Path):
    (tmp_path / "build").mkdir()
    (tmp_path / "build" / "Keep.kt").write_text(_KOTLIN)
    (tmp_path / "build" / "Drop.kt").write_text(_KOTLIN)

    scanned = scan_directory(
        tmp_path,
        body_node_count_threshold=0,
        exclude=["build/", "!build/Keep.kt"],
    )

    assert [sf.path for sf in scanned] == [Path("build", "Keep.kt")]
