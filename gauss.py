# -*- coding: utf-8 -*-
"""
Created on Thu May 23 18:02:49 2022
@author: StJoesy
"""

"""
https://en.wikipedia.org/wiki/Cholesky_decomposition
"""
import sys,operator,os
from fractions import Fraction

from functools import reduce

termSizeColumns = os.get_terminal_size().columns


class gauss :
    _colors_ = {
        'W':'\033[0m',
        'R':'\033[31m',
        'G':'\033[32m',
        'O':'\033[33m',
        'B':'\033[34m',
        'P':'\033[35m',
    }

    def __init__ ( self, twoDimensionList, trace=False ):
        self.rowCount = len(twoDimensionList)
        self.collCount = len(twoDimensionList[0])
        self.mx = twoDimensionList.copy()
        self.trace = trace
        print (self._colors_)
        print("rowCount:{rowCount} ,collCount:{collCount}".format(rowCount=self.rowCount,collCount=self.collCount) )
        
        #convert  two dimension array  to "fraction MX"
        for row in range(len(twoDimensionList)) :
            for cell in range(len(twoDimensionList[row])):
                self.mx[row][cell] = Fraction(twoDimensionList[row][cell])

        self._printLine()
        print("Fraction MX:")
        self._printFractionMX()
        self._printLine()

    def _divideRow( self, row, divisor) :
        return list(map(lambda x:x/divisor,row))

    def _addRows( self, row1, row2) :
        return list(map(operator.add,row1, row2))

    def _subRows( self, row1, row2) :
        return list(map(operator.sub,row1, row2) )


    def _multiplicateRowByConstant(self, row, constant) :
        return list(map(lambda x:x*constant,row))

    def _det(self):
        tmp = []
        for row in range(len(self.mx)) :
            print(self.mx[row][row],' ', end='')
            tmp.append(self.mx[row][row])
        print()
        return reduce((lambda x, y: x * y), tmp)
    
    def det(self):
        return self._det()

    def _printFractionMX (self):
        for row in range(len(self.mx)) :
            self._printFractRow(self.mx[row])
            print("")
    
    def printFractionMX (self):
        self._printFractionMX()
            
    def _printFractRow (self, row) :
        for cell in range(len(row)):
            cItem = row[cell]
            print ( "[ {}/{} ]".format(cItem.numerator,cItem.denominator) , end ='')
    def _printLine (self) :
        print(u'\u2500' * termSizeColumns)

    def _gauss( self,currentRowIndex, rowToCheck  ) : 
        currentColIndex=currentRowIndex
        divisor = self.mx[rowToCheck][currentColIndex] / self.mx[currentRowIndex][currentColIndex]
        
        if self.trace: print ('''{G}current row index:   {currentRowIndex}{O}
                                            current row value: {currentRowVal}{B}
                                            row to check index:   {rowToCheckIndex}{G}
                                            row to check value:    {rowToCheckVal}{O}
                                            divisor:{divisor}{W}'''
        .format(currentRowIndex = currentRowIndex, 
        rowToCheckIndex=rowToCheck, 
        rowToCheckVal=self.mx[rowToCheck][currentColIndex], 
        currentRowVal=self.mx[currentRowIndex][currentColIndex],
        divisor=divisor,
        G=self._colors_['G'],
        W=self._colors_['W'],
        O=self._colors_['O'],
        B=self._colors_['B']).replace('  ', ''))

        if divisor  > 0 :
            tmpCurrnetRow = self._multiplicateRowByConstant(self.mx[currentRowIndex],divisor)
            self.mx[rowToCheck] = self._subRows(self.mx[rowToCheck],tmpCurrnetRow)
        elif divisor < 0 :
            tmpCurrnetRow = self._multiplicateRowByConstant(self.mx[currentRowIndex],(divisor*-1))
            self.mx[rowToCheck] = self._addRows(self.mx[rowToCheck],tmpCurrnetRow)
        if self.trace: self.printFractionMX()

    def gaussJordan( self ) :
        for currentRowIndex in range(self.rowCount):
            currentColIndex=currentRowIndex
            if  self.mx[currentRowIndex][currentColIndex] != 1 :
                self.mx[currentRowIndex] = self._divideRow(self.mx[currentRowIndex],self.mx[currentRowIndex][currentColIndex])
            self._printFractionMX()
            for rowToCheck in range (self.rowCount) :
                if rowToCheck != currentRowIndex :
                    self._gauss(currentRowIndex,rowToCheck)

    def upperDiagonal( self ) :
        for currentRowIndex in range(self.rowCount):
            for rowToCheck in range (self.rowCount) :
                if rowToCheck > currentRowIndex :
                    self._gauss(currentRowIndex,rowToCheck)

a1 = [[2,3,1],
     [1,2,2],
     [2,1,4]] #det:9   

a2 = [[1,1,1],
     [2,1,2],
     [1,1,1]] #det:0

a3 = [[2,3,1],
     [1,1,2],
     [1,1,1]] #det:1

a4 = [[-2,3,1],
     [1,-4,2],
     [1,-6,1]] #det:-15

a5 = [[2,1,1],
     [6,6,4],
     [10,11,11]] #det:24

a6 = [[2,1,1,7],
     [6,6,4,9],
     [10,11,11,12]] #-15 nem jó    


g = gauss(a6,True)

g.gaussJordan()


#g.upperDiagonal()
#print ("det:", g.det())


print("--Done-----")        

g.printFractionMX()

