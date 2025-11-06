with open('s2.txt') as f:
    for line in f.readlines():
        if line.startswith('GC[') and 'untracked_tuples' in line:
            line = line.replace('GC[0]', '0;')
            line = line.replace('GC[1]', '1;')
            line = line.replace('GC[2]', '2;')
            line = line.replace('untracked_tuples: ', '')
            print(line, end='')