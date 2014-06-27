#################################################################################
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#################################################################################
#   #                                                                       #   #
#   #                                                                       #   #
#####                            Info:                                      #####
#   #                         version: 0.03                                 #   #
#   #                                                                       #   #
#####                                                                       #####
#   #                                                                       #   #
#   #                                                                       #   #
#################################################################################
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#################################################################################
#   #                                                                       #   #
#   #                                                                       #   #
#####         .___________.  ______    _______   ______                     #####
#   #         |           | /  __  \  |       \ /  __  \                    #   #
#   #         `---|  |----`|  |  |  | |  .--.  |  |  |  |                   #   #
#####             |  |     |  |  |  | |  |  |  |  |  |  |                   #####
#   #             |  |     |  `--'  | |  '--'  |  `--'  |                   #   #
#   #             |__|      \______/  |_______/ \______/                    #   #
#####                                                                       #####
#   #                                                                       #   #
#   #                                                                       #   #
#####                                                                       #####
#   #   Todo:                                                               #   #
#   #       - Error handling (trailing Spaces or "/" in Settings and Path)  #   #
#####                                                                       #####
#   #       - better Startup Interface                                      #   #
#   #       - Progressbar (1 for current Seq, 1 for all Seq)                #   #
#####                                                                       #####
#   #                                                                       #   #
#   #                                                                       #   #
#################################################################################
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#################################################################################



# Test


from PyQt4 import QtCore, QtGui
import os
import string

##############################################################################################
#
#
#       Settings:
#
FFMPEG_EXE = "D:\\Vincent\\Dropbox\\btSyncFolders\\Tools\\folder2mov\\ffmpeg.exe"


DEFAULTS_SETTINGS = ""
DEFAULTS_SETTINGS += "-pix_fmt yuv420p "
DEFAULTS_SETTINGS += "-c:v libx264 "
DEFAULTS_SETTINGS += "-preset ultrafast "
DEFAULTS_SETTINGS += "-tune film"




##############################################################################################
#
#
#       Core Functions:
#


def getSeqences(path):
    sequences = {}

    for fileName in os.listdir(path):
        baseName, fileExt = os.path.splitext(fileName)

        # Skip nonPictures
        if fileExt.lower() not in  [".jpg", ".tif", ".exr"]:
            continue

        # Split FrameNumber from BaseName
        frameNum = ""
        while baseName[-1] in string.digits:
            frameNum = baseName[-1] + frameNum
            baseName = baseName[:-1]


        # Oh Shit! A new Sequence.
        if baseName not in sequences:
            sequences[baseName] = [fileExt, None, None, len(frameNum)]


        # CleanUp the FrameNum
        while frameNum.startswith("0"):
            frameNum = frameNum[1:]
        frame = int(frameNum)

        # Set new Values ?!?
        if sequences[baseName][1] >= frame or not sequences[baseName][1]:
            sequences[baseName][1] = frame

        if sequences[baseName][2] <= frame:
            sequences[baseName][2] = frame


    # Make it cooler:
    # OldDict: (Name: [start, end, pad])  //   New: [[Name, start, end, pad]]
    out = []
    for baseName in sequences:
        out.append([baseName, sequences[baseName][0], sequences[baseName][1], sequences[baseName][2], sequences[baseName][3]])
    return out







##############################################################################################
#
#
#       Interface:
#


class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()


        self.lineEdits_FileNames = []
        self.lineEdits_Starts = []
        self.lineEdits_Ends = []
        self.lineEdits_FPSs = []
        self.lineEdits_Outputs = []
        self.frameRangeDividers = []



        self.setAcceptDrops(True)

        main_grid = QtGui.QGridLayout()


        # Path
        groupPath = QtGui.QGroupBox("Path:")
        main_grid.addWidget(groupPath, 1, 0, 1, 4)
        gridPath = QtGui.QGridLayout(groupPath)

        self.lineEditPath = QtGui.QLineEdit()
        self.connect(self.lineEditPath, QtCore.SIGNAL("textChanged(QString)"), self.pathChanged)
        gridPath.addWidget(self.lineEditPath, 0, 0)


        # Files
        groupFiles = QtGui.QGroupBox("Files:")
        gridPath.addWidget(groupFiles, 1, 0)

        self.gridFiles = QtGui.QGridLayout(groupFiles)

        self.gridFiles.addWidget(QtGui.QLabel("FileName:"), 0, 0)
        self.gridFiles.addWidget(QtGui.QLabel("FrameRange:"), 0, 1, 1, 3)
        self.gridFiles.addWidget(QtGui.QLabel("FPS:"), 0, 4)
        self.gridFiles.addWidget(QtGui.QLabel("Output:"), 0, 5)

        self.addQLineEdits(None)


        # Settings:
        groupSettings = QtGui.QGroupBox("Settings:")
        main_grid.addWidget(groupSettings, 2, 0, 1, 4)
        gridSettings = QtGui.QGridLayout(groupSettings)

        self.lineEditFileSettings = QtGui.QLineEdit(DEFAULTS_SETTINGS)
        gridSettings.addWidget(self.lineEditFileSettings, 0, 0)


        # Button:
        btnConvert = QtGui.QPushButton("Convert")
        main_grid.addWidget(btnConvert, 3, 3)
        self.connect(btnConvert, QtCore.SIGNAL("clicked()"), self.btnPressed_Convert)



        foobar = QtGui.QWidget()
        foobar.setLayout(main_grid)
        self.setCentralWidget(foobar)
        self.setWindowTitle("folder2mov v02.10")
        self.show()


        # Init State:
        self.pathChanged(None)



    def addQLineEdits(self, seq=None):
        # Create
        lineEditFileName = QtGui.QLineEdit()
        lineEditStart = QtGui.QLineEdit()
        lineEditEnd = QtGui.QLineEdit()
        lineEditFPS = QtGui.QLineEdit()
        lineEditOutput = QtGui.QLineEdit()
        frameRangeDivider = QtGui.QLabel("-")

        # Set Width
        for lineEdit in [lineEditStart, lineEditEnd, lineEditFPS]:
            lineEdit.setMaximumWidth(30)
            lineEdit.setAlignment(QtCore.Qt.AlignCenter)

        # Add to Grid
        n = self.gridFiles.rowCount()
        self.gridFiles.addWidget(lineEditFileName, n, 0)
        self.gridFiles.addWidget(lineEditStart, n, 1)
        self.gridFiles.addWidget(frameRangeDivider, n, 2)
        self.gridFiles.addWidget(lineEditEnd, n, 3)
        self.gridFiles.addWidget(lineEditFPS, n, 4)
        self.gridFiles.addWidget(lineEditOutput, n, 5)

        # Add to self.Arrays
        self.lineEdits_FileNames.append(lineEditFileName)
        self.lineEdits_Starts.append(lineEditStart)
        self.lineEdits_Ends.append(lineEditEnd)
        self.lineEdits_FPSs.append(lineEditFPS)
        self.lineEdits_Outputs.append(lineEditOutput)
        self.frameRangeDividers.append(frameRangeDivider)

        # Set Values
        if seq:
            lineEditFileName.setText(seq[0] + "%0" + str(seq[4]) + "d" + seq[1])
            lineEditStart.setText(str(seq[2]))
            lineEditEnd.setText(str(seq[3]))
            lineEditFPS.setText("24")
            lineEditOutput.setText(seq[0].strip("_").strip(".") + ".mov")

        return True


    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        text = str(e.mimeData().urls()[0].toLocalFile())
        self.lineEditPath.setText(text)


    def delQLineEdits(self):
        for widget in self.lineEdits_FileNames + self.lineEdits_Starts + self.lineEdits_Ends + self.lineEdits_FPSs + self.lineEdits_Outputs + self.frameRangeDividers:
            self.gridFiles.removeWidget(widget)
            widget.deleteLater()

        self.lineEdits_FileNames = []
        self.lineEdits_Starts = []
        self.lineEdits_Ends = []
        self.lineEdits_FPSs = []
        self.lineEdits_Outputs = []
        self.frameRangeDividers = []


    def pathChanged(self, value):
        folder = str(value)

        # CleanUp
        self.delQLineEdits()

        if not os.path.isdir(folder):
            self.addQLineEdits(None)
            self.enableQLineEdits(False)
            return

        else:
            #self.enableQLineEdits(True)
            for seq in getSeqences(folder):
                self.addQLineEdits(seq)


    def btnPressed_Convert(self):
        print "What the FUCK?!"
        settings = str(self.lineEditFileSettings.text())
        path = str(self.lineEditPath.text())

        for i in range(len(self.lineEdits_FileNames)):
            fileName = str(self.lineEdits_FileNames[i].text())
            start = str(self.lineEdits_Starts[i].text())
            #end = str(self.lineEdits_Ends[i].text())
            fps = str(self.lineEdits_FPSs[i].text())
            output = str(self.lineEdits_Outputs[i].text())

            # Build Commandline
            cmdLine = ""
            cmdLine += '"' + FFMPEG_EXE + '" '
            cmdLine += "-start_number " + start + " -f image2 -r " + fps        # Input-Settings
            cmdLine += " -i " + os.path.join(path, fileName) + " "              # Input-FileName
            cmdLine += settings + " "                                           # Output-Settings
            cmdLine += os.path.join(os.path.dirname(path), output)              # Output-FileName
            os.system(cmdLine)





    # Helpers:
    def enableQLineEdits(self, value):
         for widget in self.lineEdits_FileNames + self.lineEdits_Starts + self.lineEdits_Ends + self.lineEdits_FPSs + self.lineEdits_Outputs:
            if value:
                widget.setEnabled(True)
            else:
                widget.setEnabled(False)
                widget.setText("")



if __name__ == '__main__':
    app = QtGui.QApplication([])
    ex = Ui_MainWindow()
    app.exec_()
