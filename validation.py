import config


def file_readlines(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    return lines


def main():
    """Main method."""
    if config.CONSUME_LOGFILE != '':
        failed_counter = 0
        list_line = file_readlines(config.CONSUME_LOGFILE)
        pre_line = 0
        for line in list_line:
            if int(line.replace('\n', '')) < pre_line:
                print('Validate failed: ' + line.replace('\n', ''))
                failed_counter += 1
            pre_line = int(line.replace('\n', ''))
        if failed_counter == 0:
            print('Validate success!')


if __name__ == '__main__':
    main()
