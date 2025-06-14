#

from pathlib import Path

rtl_dir = Path(__file__).parent / "rtl"

def add_verilog_file(plat, file_name):
    if file_name not in plat.extra_files:
        with (rtl_dir / file_name).open('rb') as f:
            plat.add_file(file_name, f.read())

def add_verilog_files(plat, file_names):
    if plat is not None:
        for d in file_names:
            add_verilog_file(plat, d)
