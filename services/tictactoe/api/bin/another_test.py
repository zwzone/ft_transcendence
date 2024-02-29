import subprocess

p = subprocess.Popen("python3 klak.py",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
out, err = p.communicate(input="insta\n".encode())
if p.returncode != 0:
    print(out)
    print(err)
else:
    print("error")