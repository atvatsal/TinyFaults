from TinyFaults.const import *

class Net:
    def __init__(self, netid, type, fromNets, toNets):
        self.netid = netid
        self.type = type
        self.fromNets = fromNets
        self.toNets = toNets

    def addFromNet(self, net):
        self.fromNets.append(net)

    def addToNet(self, net):
        self.toNets.append(net)

    def isPI(self):
        return self.type == NetType.INPUT
    
    def isPO(self):
        return len(self.toNets) == 0
    
    def isStem(self):
        return len(self.toNets) > 1  #TODO: check if stem sivay bija mate true nathi thatu ne, note 2

class Circuit:
    from TinyFaults.const import LogicValue
    
    def __init__(self, netClass = Net, *args, **kwargs):
        self._nets = []
        self._netClass = netClass

        if len(kwargs) == 0:
            return
        method = kwargs['generateMethod']

        if method == 'FROM_FILE':
            self.generateFromFile(kwargs['filePath'], kwargs['format'])
            return            

    def _addNet(self, net):
        if type(net) != self._netClass:
            raise TypeError('net must be of type ' + str(self._netClass) + ': Got ' + str(type(net)))
        self._nets.append(net)

    def _findNet(self, netid):
        for net in self._nets:
            if net.netid == netid:
                return net
        raise ValueError('Net not found: ' + str(netid))

    def generateFromFile(self, filePath, format='ISCAS'):
        if format == 'ISCAS':
            netlist = pd.read_csv(filePath).values

            for netData in netlist:
                self._addNet(self._netClass(netData[0], NetType.fromString(netData[2]), [], []))
            
            for netData in netlist:
                if netData[2] == 'inpt':
                    continue
                
                net = self._findNet(netData[0])
                if netData[2] == 'from':
                    stemNet = self._findNet(netData[3])
                    net.addFromNet(stemNet)
                    stemNet.addToNet(net)
                    continue
                for i in range(5,5+netData[4]):
                    if netData[i] == 0: # see note 1
                        continue
                    inputNet = self._findNet(netData[i])
                    net.addFromNet(inputNet)
                    inputNet.addToNet(net)
            return
        
        raise ValueError('Invalid format: '+ format)

    #TODO: remove this
    def traverseUpUp(self):
        for net in self._nets:
            if net.isPO():
                startpoint = net
                break
        
        currentNet = startpoint
        while True:
            inputnets = ''
            for inet in currentNet.fromNets:
                inputnets += str(inet.netid) + ' '
            outputnets = ''
            for onet in currentNet.toNets:
                outputnets += str(onet.netid) + ' '

            print('netid. ', str(currentNet.netid), ' | type ', currentNet.type, ' | inputs ', inputnets, ' | outputs ', outputnets)
            if currentNet.isPI():
                break
            currentNet = currentNet.fromNets[0]