EASY = ('Easy.opensudoku', 'easy.sudoku')
MEDIUM = ('Medium.opensudoku', 'medium.sudoku')
def main():
    w = open(EASY[1],"w+")
    with open(EASY[0]) as f:
        for line in f:
            read_data = line.strip()
            if read_data.startswith('<game'):
                data = read_data[read_data.find('data="'):]
                data = data.strip(' />')
                data = data.strip('data="')
                if data == "":
                    continue
                if data.startswith('version:'):
                    data = data.replace('version: 1&#10;','')
                    data = data.strip('|')
                    num = data.split('|')
                    data_ = []
                    for i in range(0, 81 * 3, 3):
                        num_str = num[i] + num[i+2]
                        data_.append(num_str)
                    num_str = ''
                    for d in data_:
                        if d[1] == '0':
                            num_str = num_str + d[0]
                        else:
                            num_str = num_str + '0'

                    data = num_str

                w.write(data+'\n')
    f.closed
    w.close()

main()
