from pathlib import Path
import shutil
from subprocess import run
from enum import Enum

PROJECT_DIR = Path(__file__).parent
OUPUT_DIR = PROJECT_DIR / "pop_delimit_practice_app"
PCA_DELIMITATION_NOTEBOOK = PROJECT_DIR / "pca_population_delimitation_practice.py"
DATA_DIR_NAME = "data"
DATA_DIR = PROJECT_DIR / DATA_DIR_NAME
OUTPUT_DATA_DIR = OUPUT_DIR / DATA_DIR_NAME


def remove_dir(dir_):
    if dir_.exists():
        shutil.rmtree(dir_)


class Mode(Enum):
    EDIT = 1
    RUN = 2


def export_notebook_as_app(notebook: Path, output_dir: Path, mode: Mode):
    cmd = [
        "uv",
        "run",
        "marimo",
        "export",
        "html-wasm",
        str(notebook),
        "-o",
        str(output_dir),
        "--no-show-code",  # don't show the cells code (--show-code would be the alternative)
    ]
    mode: str = "edit" if mode == Mode.EDIT else "run"
    cmd.extend(
        [
            "--mode",
            mode,  # don't allow editing (edit would be the alternative)
        ]
    )
    # print(" ".join(cmd))
    run(cmd, check=True)


remove_dir(OUPUT_DIR)
export_notebook_as_app(PCA_DELIMITATION_NOTEBOOK, OUPUT_DIR, mode=Mode.EDIT)
# shutil.copytree(DATA_DIR, OUTPUT_DATA_DIR)

# cd static_app
print("serve with:")
print(f"cd {OUPUT_DIR}")
print("python -m http.server 8000 --bind 127.0.0.1")
