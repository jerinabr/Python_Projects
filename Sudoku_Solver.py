import time #import libraries and modules

bd = [ #unsolved sudoku board. Periods represent blank spaces
    [ "2", ".", ".", "6", ".", "8", ".", ".", "." ],
    [ "4", ".", "5", ".", ".", ".", "6", ".", "." ],
    [ ".", "8", ".", ".", ".", "5", "3", ".", "1" ],
    [ ".", "2", ".", ".", ".", "3", ".", "1", "." ],
    [ ".", ".", "1", ".", "2", ".", "7", ".", "." ],
    [ ".", "6", ".", "9", ".", ".", ".", "2", "." ],
    [ "8", ".", "2", "4", ".", ".", ".", "6", "." ],
    [ ".", ".", "7", ".", ".", ".", "9", ".", "8" ],
    [ ".", ".", ".", "1", ".", "7", ".", ".", "5" ],
]

def printBoard(): #this function prints out the sudoku board in a format that a human can easily read
    print( "-" * 25 )
    for row in range( len( bd ) ):
        line = "| "
        for column in range( len( bd[ row ] ) ):
            line += bd[ row ][ column ] + ( ( column + 1 ) % 3 == 0 and " | " or " " ) #add the element to the line and add a | if it's every third column element
        print( line + ( ( row + 1 ) % 3 == 0 and ( "\n" + "-" * 25 ) or "" ) ) #print each row and print a series of dashes if it's every third row
        
def isNum( num ): #this functions checks if a string character is a number
    return ( num in "0123456789" )

def isBoardFull(): #this function checks to see if the board is full, doesn't check if the board is correct
    for row in bd:
        for column in row:
            if ( not isNum( column ) ): #if the specified space isn't a number, then return false
                return False
    return True

def isBoardSolved(): #this function checks to see if all the space on the board are correct
    check = [ "1", "2", "3", "4", "5", "6", "7", "8", "9" ]
    for r in range( 9 ):
        for c in range( 9 ):
            row, column = [], []
            for i in range( 9 ): #add the elements of the row and the column to the corresponding tables above
                row.append( bd[ r ][ i ] )
                column.append( bd[ i ][ c ] )
            row.sort() #sort the tables so they can be compared to the check table
            column.sort()
            if ( row != check or column != check ): #compare the row and column to the check table and if either of them are not similar, return false
                return False
    return True

def canAdd( num, row, column, board ): #this function returns whether or not it is legal to put a number at the specified row and column in the board
    for i in range( 9 ):
        if ( board[ i ][ column ] == num or board[ row ][ i ] == num ): #check to see if that number isn't already in the specified row or column
            return False
    return True

def getBoardCopy(): #this function returns a copy of the sudoku board. The list.copy() method caused weird results so I'm using this instead
    boardCopy = []
    for row in bd:
        rowCopy = []
        for column in row:
            rowCopy.append( column )
        boardCopy.append( rowCopy )
    return boardCopy

def getBlockData( row, column, board ): #this function returns a table of the numbers in a specific block and a table of the positions of spaces in that block
    n, s = [], []
    for r in range( row, row + 3 ):
        for c in range( column, column + 3 ):
            e = board[ r ][ c ]
            if isNum( e ): #if the element is a number, put it in the table of numbers
                n.append( e )
            else: #if not, put its position in the table of spaces
                s.append( ( r, c ) )
    return n, s

def getRowOrColumnData( rowOrColumn, position, board ): #this function returns a table of the numbers that aren't in a specific row or column and a table of the positions of spaces in that row or column
    n, s = [ "1", "2", "3", "4", "5", "6", "7", "8", "9" ], []
    for p in range( 9 ):
        e = ( rowOrColumn == "row" and board[ position ][ p ] or board[ p ][ position ] )
        if isNum( e ): #if the element is a number, remove it from the table of numbers
            n.remove( e )
        else: #if not, put its position in the table of spaces
            s.append( rowOrColumn == "row" and ( position, p ) or ( p, position ) )
    return n, s

def solveBlocks( board ): #this function goes through all the 3x3 blocks and attempts to solve each one as best as it can and then returns the new board
    for i in range( 9 ): #peform 9 iterations which is all the blocks in the board
        nTable, sTable = getBlockData( int( i / 3 ) * 3, ( i % 3 ) * 3, board ) #get the block data from each block
        for j in range( 1, 10 ):
            num = str( j )
            if ( num not in nTable ): #if the number isn't already in the block...
                sTable2 = sTable.copy()
                for s in sTable:
                    if ( not canAdd( num, s[0], s[1], board ) ): sTable2.remove( s ) #remove all the spaces where the number can't be added
                if ( len( sTable2 ) == 1 ): #if there's only one possible space that the number can be added to, add the number to that space
                    board[ sTable2[0][0] ][ sTable2[0][1] ] = num
                    sTable.remove( sTable2[0] ) #remove the space that the number is in from the space table and move on to the next number
    return board

def solveRowOrColumn( rowOrColumn, position, board ): #this function tries to solve cases where a row or column has 2 or 1 empty spaces and then returns the new board
    nTable, sTable = getRowOrColumnData( rowOrColumn, position, board )
    if ( len( sTable ) == 2 ): #if the row or column has 2 empty spaces then test the two possible number combinations and apply the working one to the board
        if ( ( not canAdd( nTable[0], sTable[0][0], sTable[0][1], board ) ) #test the first possible number combination
        or ( not canAdd( nTable[1], sTable[1][0], sTable[1][1], board ) ) ):
            board[ sTable[0][0] ][ sTable[0][1] ] = nTable[1]
            board[ sTable[1][0] ][ sTable[1][1] ] = nTable[0]
        elif ( ( not canAdd( nTable[1], sTable[0][0], sTable[0][1], board ) ) #test the second possible number combination
        or ( not canAdd( nTable[0], sTable[1][0], sTable[1][1], board ) ) ):
            board[ sTable[0][0] ][ sTable[0][1] ] = nTable[0]
            board[ sTable[1][0] ][ sTable[1][1] ] = nTable[1]
    elif ( len( sTable ) == 1 ): #if the row or column has 1 empty space then put the only possible number that can go there in the board
        board[ sTable[0][0] ][ sTable[0][1] ] = nTable[0]
    return board

def solveRowsAndColumns( board ): #this function basically runs the solveRowOrColumn function for both rows and columns in one function for neatness
    for i in range( 9 ):
        board = solveRowOrColumn( "row", i, board )
        board = solveRowOrColumn( "column", i, board )
    return board

print( "START" )
printBoard()

startTime = time.time() #get the start time
while ( not isBoardFull() ): #loop until the board is full
    boardCopy = getBoardCopy()
    newBoard1 = solveBlocks( boardCopy ) #do the block solving method first
    newBoard2 = solveRowsAndColumns( newBoard1 ) #do the row column solving method second
    bd = newBoard2

endTime = time.time() #get the end time

print( "\nEND" )
printBoard()

print( isBoardSolved() and "\nBoard solved!" or "\nSomething went wrong!" )
print( "Elapsed time: {} seconds".format( endTime - startTime ) ) #print the total time the program took to solve the puzzle
