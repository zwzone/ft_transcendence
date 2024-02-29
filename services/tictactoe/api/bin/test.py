import subprocess

def main():
    p = subprocess.Popen("red",
                                            stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            shell=True)
    array = ["0 0 0 0\n", "0 0 0 2\n", "0 0 1 1\n", "0 0 2 0\n", "0 0 2 2\n", "0 1 0 1\n"]

    print( "here", flush=True )
    out, err = p.communicate(input="0 0 0 0\n".encode())
    p.wait()

# for i in range( len(array) ):
#     out, err = p.communicate(input=array[i].encode())
    print( "error", err, flush=True)
    print( "here ", out, flush=True )

if __name__ == "__main__":
    main()