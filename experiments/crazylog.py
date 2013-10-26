import logging
import cflib
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import Log, LogTocElement

class LogConfig():
    def __init__(self, configname, period=0, filename=""):
        self.period = period
        self.variables = []
        self.configName = configname
        self.configFileName = filename
        self.datarangeMin = 0
        self.datarangeMax = 0

    def addVariable(self, var):
        self.variables.append(var)

    def setPeriod(self, period):
        self.period = period

    def setDataRange(self, minVal, maxVal):
        self.datarangeMin = minVal
        self.datarangeMax = maxVal

    def getVariables(self):
        return self.variables

    def getName(self):
        return self.configName

    def getDataRangeMin(self):
        return self.datarangeMin

    def getDataRangeMax(self):
        return self.datarangeMax

    def getPeriod(self):
        return self.period

    def __str__(self):
        return ("LogConfig: name=%s, period=%d, variables=%d" %
                (self.configName, self.period, len(self.variables)))


class LogVariable():
    """A logging variable"""

    TOC_TYPE = 0
    MEM_TYPE = 1

    def __init__(self, name="", fetchAs="uint8_t", varType=0, storedAs="",
                 address=0):
        self.name = name
        self.fetchAs = LogTocElement.get_id_from_cstring(fetchAs)
        if (len(storedAs) == 0):
            self.storedAs = self.fetchAs
        else:
            self.storedAs = LogTocElement.get_id_from_cstring(storedAs)
        self.address = address
        self.varType = varType
        self.fetchAndStoreageString = fetchAs
        self.storedAsString = storedAs
        self.fetchAsString = fetchAs

    def setName(self, name):
        """Set the name"""
        self.name = name

    def setTypes(self, storeAs, fetchAs):
        """
        Set the type the variable is stored as in the Crazyflie and the type it
        should be fetched as.
        """
        self.fetchAs = fetchAs
        self.storeAs = storeAs

    def isTocVariable(self):
        """
        Return true if the variable should be in the TOC, false if raw memory
        variable
        """
        return self.varType == LogVariable.TOC_TYPE

    def setAddress(self, addr):
        """Set the address in case of raw memory logging."""
        self.address = addr

    def getName(self):
        """Return the variable name"""
        return self.name

    def getStoredAs(self):
        """Return the type the variable is stored as in the Crazyflie"""
        return self.storedAs

    def getFetchAs(self):
        """Return the type the variable should be fetched as."""
        return self.fetchAs

    def getAddress(self):
        """Return the address in case of memory logging."""
        return self.address

    def getVarType(self):
        """Get the variable type"""
        return self.varType

    def getStoredFetchAs(self):
        """Return what the variable is stored as and fetched as"""
        return (self.fetchAs | (self.storedAs << 4))

    def setFetchAndStorageString(self, s):
        """Set the fetch and store string"""
        self.fetchAndStoreageString = s

    def getFetchAndStorageString(self):
        """Return the fetch and store string"""
        return self.fetchAndStoreageString

    def __str__(self):
        return ("LogVariable: name=%s, store=%s, fetch=%s" %
                (self.name, LogTocElement.get_cstring_from_id(self.storedAs),
                 LogTocElement.get_cstring_from_id(self.fetchAs)))
