from datetime import datetime


def info(text):
    printWithTime('INFO: ' + text)


def warn(text):
    printWithTime('WARN: ' + text)


def error(text):
    printWithTime('ERR : ' + text)


def printWithTime(text):
    now = datetime.now().time().isoformat(timespec='seconds')
    print('[' + now + '] ' + text)
