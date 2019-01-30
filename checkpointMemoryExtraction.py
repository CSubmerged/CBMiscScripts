def main():
    # Link to a file outputted by "grep "vb_.*mem_usage" stats.log >> ... "
    file = open("grepMemcachedLog.txt")
    chkMem = 0
    alreadyRead = []
    for line in file:
        lineList = line.split(":")
        for replicaNo in range(128, 256):  # Assumes on node 1 so first half are active
            if lineList[0].endswith(str(replicaNo)) and (replicaNo not in alreadyRead):
                out = int(lineList[2].strip().replace("\n", ""))
                chkMem += out
                alreadyRead.append(replicaNo)
    print(chkMem)
    print(len(alreadyRead))  # In MB-32043's case, this should be 128
    # (no. of replica buckets on the node, half of 256)

main()
