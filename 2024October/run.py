import os
import sys
runall = len(sys.argv) == 2
torun = list(sys.argv[2:])

for file in sorted(os.listdir(sys.argv[1])):
    if file.endswith(".in") and (runall or any(("_"+x) in file for x in torun)):
        print("running", file)
        prog = "python3"
        py = os.path.join(sys.argv[1], sys.argv[1] + ".py")
        pip1 = "<"
        infile = os.path.join(sys.argv[1], file)
        pip2 = ">"
        outfile = os.path.join(sys.argv[1], file.removesuffix(".in") + ".out")
        cmd = " ".join([prog, py, pip1, infile, pip2, outfile])
        print(cmd)
        os.system(cmd)
        print("finished", file)