#coding=utf-8
import unittest  


class ParametrizedTestCase(unittest.TestCase):  
    """ TestCase classes that want to be parametrized should 
        inherit from this class. 
    """  
    def __init__(self, methodName='runTest', logger=None):  
        super(ParametrizedTestCase, self).__init__(methodName)  
        self.logger = logger  
        
    @staticmethod  
    def parametrize(testcase_klass, logger=None):  
        """ Create a suite containing all tests taken from the given 
            subclass, passing them the parameter 'param'. 
        """  
        testloader = unittest.TestLoader()  
        testnames = testloader.getTestCaseNames(testcase_klass)  
        suite = unittest.TestSuite()
        
#         suit =testloader.loadTestsFromTestCase(testcase_klass)
        for name in testnames:  
            suite.addTest(testcase_klass(name, logger=logger.logger))  
        return suite 

class _TestResult(unittest.TestResult):
    def __init__(self,stream, descriptions, verbosity):
        super(_TestResult, self).__init__(stream, descriptions, verbosity)
        self.trys=0
        self.status=0

    def addFailure(self, test, err):
        super(_TestResult, self).addFailure(test, err)
        self.status =1

    def stopTest(self, test):
        super(_TestResult,self).stopTest(test)
        if self.status ==1:
            self.trys += 1
            if self.trys <= 3:
                print u"用例执行失败，重试中... %d" % self.trys
                test(self)
            else:
                self.status = 0
                self.trys = 0
