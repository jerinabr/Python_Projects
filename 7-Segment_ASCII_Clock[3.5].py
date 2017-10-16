from time import sleep
from datetime import datetime

#   -------- 
#  |        |
#  |        |
#  |        |
#   -------- 
#  |        |
#  |        |
#  |        |
#   -------- 

#-------------------------------------------------------#
#--------------------[ VARIABLES ]----------------------#
#-------------------------------------------------------#

shiftUp = 13 #This is how many spaces up the clock will be offset from the bottom of the screen
shiftRight = 25 #This is how many spaces right the clock will be offset from the left of the screen

digitWidth = 12 #This number is how wide each digit is
digitHeight = 8 #This has to be an even number because half of this number will the height of each half of the digit

#-------------------------------------------------------#
#--------------------[ CONSTANTS ]----------------------#
#-------------------------------------------------------#

segments = [
    [ "-" * digitWidth, "|", "|", "-" * digitWidth, "|", "|", " " * digitWidth ],
    [ " " * digitWidth, "|", "|", " " * digitWidth, " ", " ", " " * digitWidth ],
    [ "-" * digitWidth, "|", " ", "-" * digitWidth, "|", " ", "-" * digitWidth ],
    [ "-" * digitWidth, "|", "|", "-" * digitWidth, " ", " ", "-" * digitWidth ],
    [ " " * digitWidth, "|", "|", " " * digitWidth, " ", "|", "-" * digitWidth ],
    [ "-" * digitWidth, " ", "|", "-" * digitWidth, " ", "|", "-" * digitWidth ],
    [ "-" * digitWidth, " ", "|", "-" * digitWidth, "|", "|", "-" * digitWidth ],
    [ "-" * digitWidth, "|", "|", " " * digitWidth, " ", " ", " " * digitWidth ],
    [ "-" * digitWidth, "|", "|", "-" * digitWidth, "|", "|", "-" * digitWidth ],
    [ "-" * digitWidth, "|", "|", "-" * digitWidth, " ", "|", "-" * digitWidth ]
]

dw = " " * digitWidth
sr = " " * shiftRight

#-------------------------------------------------------#
#--------------------[ MAIN ]---------------------------#
#-------------------------------------------------------#

def createASCIIDigit( digit ):
    return [
        " " + segments[ digit ][0] + " ",
        segments[ digit ][5] + dw + segments[ digit ][1],
        " " + segments[ digit ][6] + " ",
        segments[ digit ][4] + dw + segments[ digit ][2],
        " " + segments[ digit ][3] + " "
    ]

def createASCIINumber( num ):
    tens, ones = createASCIIDigit( int( num[0] ) ), createASCIIDigit( int( num[1] ) )
    asciiNum = []
    for i in range( 5 ):
        asciiNum.append( tens[ i ] + "   " + ones[ i ] )
    return asciiNum

while True:
    s = createASCIINumber( "{:02d}".format( datetime.now().second ) )
    m = createASCIINumber( "{:02d}".format( datetime.now().minute ) )
    h = createASCIINumber( "{:02d}".format( ( datetime.now().hour - 1 ) % 12 + 1 ) )

    lines = [
        sr + h[0] + "     " + m[0] + "     " + s[0] + "\n",
        ( sr + h[1] + "     " + m[1] + "     " + s[1] + "\n" ) * ( digitHeight // 2 ),
        sr + h[2] + "  :  " + m[2] + "  :  " + s[2] + "\n",
        ( sr + h[3] + "     " + m[3] + "     " + s[3] + "\n" ) * ( digitHeight // 2 ),
        sr + h[4] + "     " + m[4] + "     " + s[4]
    ]

    print( "\n" * 30 )
    print( lines[0] + lines[1] + lines[2] + lines[3] + lines[4] )
    print( "\n" * shiftUp )
    sleep( 1 )
