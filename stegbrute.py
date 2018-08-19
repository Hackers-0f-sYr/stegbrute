def banner():
    from pyfiglet import Figlet

    print(Figlet(font='graffiti').renderText('Die();'))
    print('[#] HTB: https://www.hackthebox.eu/home/users/profile/47396')

def parseArgs():
    import argparse
    from sys import argv

    if(len(argv) < 3):
        print('Usage: {} [Options] use -h for help'.format(argv[0]))
        exit()
    parser = argparse.ArgumentParser(epilog='Example: {} -i steg.jpg -o output.txt -w wordlist.txt'.format(argv[0]))
    parser._optionals.title = 'OPTIONS'
    parser.add_argument('-i', '--image', help='select stego image', required=True)
    parser.add_argument('-o', '--output', help='select file name for extracted data', required=True)
    parser.add_argument('-w', '--wordlist', help='select a wordlist', required=True)
    return parser.parse_args().image, parser.parse_args().output, parser.parse_args().wordlist 

def steghide(password):
    from subprocess import call, DEVNULL

    cmd = 'steghide extract -sf {0} -xf {1} -p {2}'.format(image, output, password)
    if call(cmd.split(), stdout = DEVNULL, stderr = DEVNULL) == 0:
        print('[#] password: {}\n[ctrl + c] to stop'.format(password))

if __name__ == '__main__':
    from multiprocessing import Pool
    from time import time

    banner()
    image, output, wordlist = parseArgs()
    pool = Pool()
    start = time()
    pool.map(steghide, [password.rstrip() for password in open(wordlist, errors = 'ignore')])
    totalTime = time() - start
    timeFormat = 'seconds'
    if(totalTime >= 60):
        totalTime = totalTime/60
        timeFormat = 'minutes'
        if(totalTime >= 3600):
            totalTime = totalTime/60
            timeFormat = 'hours'
    print('[#] Finished : {0:.2f} {1}'.format(totalTime, timeFormat))