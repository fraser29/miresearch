import os
import sys
import argparse
import base64

from miresearch import mi_config



DEFAULT_DICOM_META_TAG_LIST = ["BodyPartExamined",
                                "MagneticFieldStrength",
                                "Manufacturer",
                                "ManufacturerModelName",
                                "Modality",
                                "PatientBirthDate",
                                "PatientID",
                                "PatientName",
                                "PatientSex",
                                "ReceiveCoilName",
                                "SoftwareVersions",
                                "StudyDate",
                                "StudyDescription",
                                "StudyID",
                                "StudyInstanceUID"]

DEFAULT_DICOM_TIME_FORMAT = "%H%M%S" # TODO to config (and above) - or from spydcmtk

#==================================================================
def getDataRoot():
    """Function to return data root from configuration. 

    Returns:
        str: Path to data root - found from config
    """
    return mi_config.DataRootDir

#==================================================================
class DirectoryStructure(object):
    def __init__(self, name, childrenList=[]) -> None:
        super().__init__()
        self.name = name
        self.childrenList = childrenList

class DirectoryStructureTree():
    def __init__(self, topList) -> None:
        self.topList = topList

#==================================================================
# Override error to show help on argparse error (missing required argument etc)
class MiResearchParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def setNList(args):
    if len(args.subjRange) == 2:
        args.subjNList = args.subjNList+list(range(args.subjRange[0], args.subjRange[1]))
    if args.subjNListFile:
        args.subjNList = args.subjNList+subjFileToSubjN(args.subjNListFile)
    # args.subjNList = sorted(list(set(args.subjNList)))
    
#==================================================================
def countFilesInDir(dirName):
    files = []
    if os.path.isdir(dirName):
        for _, _, filenames in os.walk(dirName):  # @UnusedVariable
            files.extend(filenames)
    return len(files)

def datetimeToStrTime(dateTimeVal, strFormat=DEFAULT_DICOM_TIME_FORMAT):
    return dateTimeVal.strftime(strFormat)

#==================================================================
def encodeString(strIn, passcode):
    enc = []
    for i in range(len(strIn)):
        key_c = passcode[i % len(passcode)]
        enc_c = chr((ord(strIn[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


def decodeString(encStr, passcode):
    dec = []
    enc = base64.urlsafe_b64decode(encStr).decode()
    for i in range(len(enc)):
        key_c = passcode[i % len(passcode)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def readFileToListOfLines(fileName, commentSymbol='#'):
    ''' Read file - return list - elements made up of each line
        Will split on "," if present
        Will skip starting with #
    '''
    with open(fileName, 'r') as fid:
        lines = fid.readlines()
    lines = [l.strip('\n') for l in lines]
    lines = [l for l in lines if len(l) > 0]
    lines = [l for l in lines if l[0]!=commentSymbol]
    lines = [l.split(',') for l in lines]
    return lines


def subjFileToSubjN(subjFile):
    allLines = readFileToListOfLines(subjFile)
    try:
        return [int(i[0]) for i in allLines]
    except ValueError:
        tf = [i.isnumeric() for i in allLines[0][0]]
        first_numeric = tf.index(True)
        return [int(i[0][first_numeric:]) for i in allLines]


#==================================================================
class SubjPrefixError(Exception):
    ''' SubjPrefixError
            If errors to do with the subject prefix '''
    def __init__(self, msg2=''):
        self.msg = 'SubjPrefixError: please provide as imput.' + '\n' + msg2
    def __str__(self):
        return self.msg
