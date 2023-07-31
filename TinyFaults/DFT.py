from TinyFaults.Circuit import *

class DFTNet(Net):
    def __init__(self, netid, type, fromNets, toNets):
        super().__init__(netid, type, fromNets, toNets)
        self.faultsToTest = {"SA0": True, "SA1": True}
        self.testabilityMeasures = {"CC0": None, "CC1": None, "CO": None}
        
class DFTCircuit(Circuit):
    def __init__(self, netClass = DFTNet,  *args, **kwargs):
        super().__init__(netClass = netClass, *args, **kwargs)

    def _EFRgoLeft(self, net):
        if (not net.isPO()) and (not net.isStem()):        
            toNet = net.toNets[0]

            # TODO: add support for all(?) other gates
            if toNet.faultsToTest["SA0"]:
                if toNet.type == NetType.AND:
                    net.faultsToTest["SA0"] = False
                elif toNet.type == NetType.NOR:
                    net.faultsToTest["SA1"] = False
                elif toNet.type == NetType.NOT:
                    net.faultsToTest["SA1"] = False
            # TODO: may be use elif here?
            if toNet.faultsToTest["SA1"]:
                if toNet.type == NetType.NAND:
                    net.faultsToTest["SA0"] = False
                elif toNet.type == NetType.OR:
                    net.faultsToTest["SA1"] = False
                elif toNet.type == NetType.NOT:
                    net.faultsToTest["SA0"] = False

        for fromNet in net.fromNets:
            self._EFRgoLeft(fromNet)

        return

    def reduceEquivalentFaults(self):
        for net in self._nets:
            if net.isPO():
                self._EFRgoLeft(net)

        return
    
    #TODO: beautify this
    def printFaultsToTest(self):
        for net in self._nets:
            print('net no.: ', net.netid, '->', net.faultsToTest)
        return

    def min(a,b):
        return a if a < b else b

    def _assignCC(self, net):            
        if net.isPI():
            net.testabilityMeasures["CC0"] = 1
            net.testabilityMeasures["CC1"] = 1
        elif net.type == NetType.FAN:
            net.testabilityMeasures["CC0"] = net.fromNets[0].testabilityMeasures["CC0"]
            net.testabilityMeasures["CC1"] = net.fromNets[0].testabilityMeasures["CC1"]
        elif net.type == NetType.AND:
            net.testabilityMeasures["CC0"] = min(net.fromNets[0].testabilityMeasures["CC0"], net.fromNets[1].testabilityMeasures["CC0"]) + 1
            net.testabilityMeasures["CC1"] = net.fromNets[0].testabilityMeasures["CC1"] + net.fromNets[1].testabilityMeasures["CC1"] + 1
        elif net.type == NetType.OR:
            net.testabilityMeasures["CC0"] = net.fromNets[0].testabilityMeasures["CC0"] + net.fromNets[1].testabilityMeasures["CC0"] + 1
            net.testabilityMeasures["CC1"] = min(net.fromNets[0].testabilityMeasures["CC1"], net.fromNets[1].testabilityMeasures["CC1"]) + 1
        elif net.type == NetType.NOT:
            net.testabilityMeasures["CC0"] = net.fromNets[0].testabilityMeasures["CC1"] + 1
            net.testabilityMeasures["CC1"] = net.fromNets[0].testabilityMeasures["CC0"] + 1
        elif net.type == NetType.NAND:
            net.testabilityMeasures["CC0"] = net.fromNets[0].testabilityMeasures["CC1"] + net.fromNets[1].testabilityMeasures["CC1"] + 1
            net.testabilityMeasures["CC1"] = min(net.fromNets[0].testabilityMeasures["CC0"], net.fromNets[1].testabilityMeasures["CC0"]) + 1
        elif net.type == NetType.NOR:
            net.testabilityMeasures["CC0"] = min(net.fromNets[0].testabilityMeasures["CC1"], net.fromNets[1].testabilityMeasures["CC1"]) + 1
            net.testabilityMeasures["CC1"] = net.fromNets[0].testabilityMeasures["CC0"] + net.fromNets[1].testabilityMeasures["CC0"] + 1
        elif net.type == NetType.XOR:
            net.testabilityMeasures["CC0"] = min(net.fromNets[0].testabilityMeasures["CC0"] + net.fromNets[1].testabilityMeasures["CC0"], 
                                                 net.fromNets[0].testabilityMeasures["CC1"] + net.fromNets[1].testabilityMeasures["CC1"]) + 1
            net.testabilityMeasures["CC1"] = min(net.fromNets[0].testabilityMeasures["CC0"] + net.fromNets[1].testabilityMeasures["CC1"], 
                                                 net.fromNets[0].testabilityMeasures["CC1"] + net.fromNets[1].testabilityMeasures["CC0"]) + 1
        elif net.type == NetType.XNOR:
            net.testabilityMeasures["CC0"] = min(net.fromNets[0].testabilityMeasures["CC0"] + net.fromNets[1].testabilityMeasures["CC1"], 
                                                 net.fromNets[0].testabilityMeasures["CC1"] + net.fromNets[1].testabilityMeasures["CC0"]) + 1
            net.testabilityMeasures["CC1"] = min(net.fromNets[0].testabilityMeasures["CC0"] + net.fromNets[1].testabilityMeasures["CC0"], 
                                                 net.fromNets[0].testabilityMeasures["CC1"] + net.fromNets[1].testabilityMeasures["CC1"]) + 1
        else:
            raise ValueError('Invalid net type: ' + str(net.type))
        return

    def _CCgoLeft(self, net):
        if (net.testabilityMeasures["CC0"] is not None): # used as isVisited
            return
        
        for fromNet in net.fromNets:
            self._CCgoLeft(fromNet)

        self._assignCC(net)
    
    def _CCgoRight(self, net):
        #TODO: not sure if this checking is correct; find a case that violates this
        if (net.testabilityMeasures["CC0"] is not None): # used as isVisited
            return

        for fromNet in net.fromNets: #need CC of all fromNets to calculate CC of net, not in case of CO
            # maybe move is not None condition checking here instead of in _CCgoLeft
            self._CCgoLeft(fromNet)

        self._assignCC(net)

        for toNet in net.toNets:
            self._CCgoRight(toNet)
    
    def findAllCC(self):
        for net in self._nets:
            if net.isPI():
                self._CCgoRight(net)

        return
    
    def _assignCO(self,net,toNet):
        if net.isPO():
            net.testabilityMeasures["CO"] = 1
            return
        
        if net.isStem():
            if (net.testabilityMeasures["CO"] is None) or (toNet.testabilityMeasures["CO"] < net.testabilityMeasures["CO"]):
                net.testabilityMeasures["CO"] = toNet.testabilityMeasures["CO"]
            return
        
        otherNetsTestabilityMeasures = {"CC0": -1*net.testabilityMeasures["CC0"], 
                                        "CC1": -1*net.testabilityMeasures["CC1"]}
        for parallelNet in toNet.fromNets:
            # if parallelNet.netid != net.netid:
            otherNetsTestabilityMeasures["CC0"] += parallelNet.testabilityMeasures["CC0"]
            otherNetsTestabilityMeasures["CC1"] += parallelNet.testabilityMeasures["CC1"]

        if toNet.type == NetType.AND or toNet.type == NetType.NAND:
            net.testabilityMeasures["CO"] = otherNetsTestabilityMeasures["CC1"] + toNet.testabilityMeasures["CO"] + 1
        elif toNet.type == NetType.OR or toNet.type == NetType.NOR:
            net.testabilityMeasures["CO"] = otherNetsTestabilityMeasures["CC0"] + toNet.testabilityMeasures["CO"] + 1
        elif toNet.type == NetType.NOT:
            net.testabilityMeasures["CO"] = toNet.testabilityMeasures["CO"] + 1
        elif toNet.type == NetType.XOR or toNet.type == NetType.XNOR:
            net.testabilityMeasures["CO"] = otherNetsTestabilityMeasures["CC0"] + toNet.testabilityMeasures["CO"] + 1
        else:
            raise ValueError('Invalid net type: ' + str(net.type))

        return
    
    def _COgoLeft(self, net, toNet):
        self._assignCO(net, toNet)

        for fromNet in net.fromNets:
            # why is this condition checking again here? can it be removed from here or from _assignCO?
            if (fromNet.testabilityMeasures["CO"] is None) or (net.testabilityMeasures["CO"] < fromNet.testabilityMeasures["CO"]):
                self._COgoLeft(fromNet, net)
    
    def findAllCO(self):
        for net in self._nets:
            if net.isPO():
                self._COgoLeft(net,None)

        return
    
    #TODO: beautify this
    def printTestabilityMeasures(self):
        for net in self._nets:
            print('net no.: ', net.netid, '->', net.testabilityMeasures)
        return
