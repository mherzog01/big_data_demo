with open('/tmp/binaries.txt') as f:
    tot_size = 0
    for line_no, line in enumerate(f):
        size = line[20:30]
        tot_size += int(size)
        if line_no and line_no % 100000 == 0:
            print('Line ',line_no)
print('Tot size',tot_size)
