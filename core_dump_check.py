# this file outputs the slurm output file associated with a coredump
from pathlib import Path
import subprocess as sp
import re

core_dumps = sorted(Path().glob("core*"))

# run the file command on each
# look for a line like /tmp/...json
# grep the *.out files
failed_regions = []
for core in core_dumps:
  print(core)
  json_line = sp.run(f"file {core}".split(" "),stdout = sp.PIPE)
  output = json_line.stdout.decode()
  print(output)
  res = re.search(r"(/tmp/.*?\.json)",output)
  if res:
    
    tmp_line = res.group(0)
    print(tmp_line)
    print(f"grep {tmp_line} *.out".split(" "))
    grep_res = sp.run(f"grep '{tmp_line}' *.out",shell=True,stdout = sp.PIPE)
    grep_stdout = grep_res.stdout.decode()
    grep_match = re.search(r"slurm.*?out",grep_stdout)
    if grep_match:
      failed_regions.append(grep_match.group(0))

print(failed_regions)
   
    
  

