from zipfile import ZipFile
from shutil import make_archive, copyfile, rmtree, move
from os import walk

def find_usb():
    drives = ['e:\\', 'f:\\', 'g:\\', 'h:\\', 'i:\\']
    fileName = 'robot.zip'
    for letter in drives:
        try:
            files = next(walk(letter))[2]
        except StopIteration:
            continue
        if fileName in files:
            return letter
    else:
        return ''

def main():
    # os.chdir('d:\\')
    tmpDir = 'tmp\\'
    archiveName = 'robot.zip'
    codeDir = '.\\'
    archiveCodeDir = 'user\\'
    usbLetter = find_usb()
    if usbLetter is '':
        print('USB with robot.zip was not found')
        return
    else:
        print('robot.zip found on %s' % (usbLetter))

    archiveDir = ''.join([usbLetter, archiveName])
    usbArchiveDir = ''.join([usbLetter, archiveName])

    with ZipFile(archiveDir, 'r') as archive:
        archive.extractall(tmpDir)

    filenames = next(walk(codeDir))[2]
    for f in filenames:
        if f == 'update_robot.zip.py':
            continue
        fileSourcePath = ''.join([codeDir, f])
        destinationPath = ''.join([tmpDir, archiveCodeDir])
        fileDestinationPath = ''.join([destinationPath, f])
        copyfile(fileSourcePath, fileDestinationPath)

    make_archive(codeDir+'robot', 'zip', tmpDir)
    rmtree(tmpDir)
    move(archiveName, usbArchiveDir)

main()