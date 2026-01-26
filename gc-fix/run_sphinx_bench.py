#!/usr/bin/env ./python
import contextlib
import os
import sys
import shutil
import subprocess
import time
import venv
from pathlib import Path
import tempfile


def run(args, output=None):
    try:
        c = subprocess.run(args, check=True, capture_output=True, text=False)
    except subprocess.CalledProcessError as e:
        print(e.stdout.decode('utf-8'))
        print(e.stderr.decode('utf-8'))
        raise
    if output:
        with open(output, 'wb') as fp:
            fp.write(c.stdout)
            fp.write(c.stderr)


def include_path(doc_path):
    return doc_path == Path("library/typing.rst")
    #return doc_path.match('library/*')


def run_in_doc(outfile, pydir):
    for path in Path(".").iterdir():
        if path.is_dir() and not str(path).startswith("."):
            for doc_path in path.rglob("*.rst"):
                if not include_path(doc_path):
                    doc_path.write_text("foo")

    venv.create(".venv", with_pip=True)

    run(
        [
            ".venv/Scripts/python.exe",
            "-m",
            "pip",
            "install",
            "-r",
            "requirements.txt",
            "--no-binary=':all:'",
        ]
    )

    start = time.perf_counter()

    run(
        [
            "time",
            "-v",
            ".venv/Scripts/python.exe",
            "-Xpystats",
            pydir / "sphinx_typing.py",
        ],
        output=outfile,
    )

    print(time.perf_counter() - start)


def main():
    outfile = os.path.abspath(sys.argv[1])
    pydir = Path(os.path.abspath('.'))
    with tempfile.TemporaryDirectory(prefix='tmp.sphinx.', delete=1) as tmpdir:
        print('tmp', tmpdir)
        shutil.copytree('Doc', tmpdir, dirs_exist_ok=True)
        with contextlib.chdir(tmpdir):
            run_in_doc(outfile, pydir)

if __name__ == '__main__':
    main()

