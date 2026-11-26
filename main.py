"""One Line, One Laugh -- make.fun entry.

Writes a single funny line to the grader's output file and nothing else.
The line is fixed and deterministic: no randomness, no clock, no network,
no input files. The joke is one concrete absurdity -- a GPS that behaves
like a petty ex -- with the reversal landing in its last words.
"""

import os

MAX_CHARS = 140

LINE = (
    "My GPS rerouted me past my ex's house and said 'recalculating' "
    "like it wasn't personal."
)


def output_path():
    """Resolve where the entry line goes.

    OUTPUT_PATH wins when set; otherwise the harness directory
    MAKEFUN_OUTPUT_DIR (default /output) holds entry.txt.
    """
    direct = os.environ.get("OUTPUT_PATH")
    if direct:
        return direct
    return os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.txt")


def main():
    os.umask(0o022)

    line = LINE.strip()
    if not line:
        raise SystemExit("entry line is empty")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise SystemExit(
            "entry is %d characters, over the %d-character limit"
            % (len(line), MAX_CHARS)
        )

    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    # Only the output FILE gets a mode set; never touch the directory
    # itself (the grader owns /output, and chmod on it would fail).
    os.chmod(path, 0o644)

    # Read the file back and confirm exactly the validated line landed:
    # a write that silently changed bytes would otherwise ship an
    # entry nobody checked.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line:
        raise SystemExit("written entry does not match the validated line")


if __name__ == "__main__":
    main()
