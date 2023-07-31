from TinyFaults.DFT import DFTCircuit

def main():
    # cktcsv = 'c17netlist.csv'
    cktcsv = 'circuit2.csv'
    # cktcsv = 'circuit2m.csv'
    # cktcsv = 'circuit3.csv'
    # cktcsv = 'circuit4.csv'
    # cktcsv = 'circuit5.csv'
    # cktcsv = 'circuit6.csv'
    myCircuit = DFTCircuit(generateMethod='FROM_FILE', filePath='samplecircuits\\' + cktcsv, format='ISCAS')
    print(myCircuit)
    
    myCircuit.traverseUpUp()
    print('---------------')

    myCircuit.reduceEquivalentFaults()
    myCircuit.printFaultsToTest()
    print('---------------')

    myCircuit.findAllCC()
    myCircuit.findAllCO()
    myCircuit.printTestabilityMeasures()
    print('---------------')

    return

if __name__ == '__main__':
    main()