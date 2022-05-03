# attribute
# @test
def test(element):
    element._test = True
    return element

# unittests
class UnitTests:
    def __init__(self):
        self.fatal  = 0 # the test couldn't be fully run [2]*
        self.failed = 0 # the test recived an unexcpected result [1]
        self.passed = 0 # the test passed as excpected [0]
        self.invalidReturn = 0 # if the returned value is not one of the above*
        self.total  = 0 # all tests

        self.errors = {} # docs all error messages if fatal

        # *) this error code should not acutally be returned from the testing function.
    
    def run(self, CLASS):
        METHODS = self.getMethods(CLASS)
        self.executeMethods(CLASS, METHODS)
        self.report(CLASS)
    
    def getMethods(self, CLASS):
        methods = []
        for method in dir(CLASS):
            attr = getattr(CLASS, method)
            if callable(attr) and getattr(attr, "_test", False):
                methods.append(method)
        return methods
    
    def executeMethods(self, CLASS, METHODS):
        for method in METHODS:
            ERRORMSG = None
            try:
                result = getattr(CLASS, method)()
            except Exception as errorMsg:
                ERRORMSG = errorMsg
                result   = 2
            self.returnMethodEval(result, method, ERRORMSG)
    
    def returnMethodEval(self, result, method, errorMsg=None):
        if result == 0:
            self.passed += 1
        elif result == 1:
            self.failed += 1
            self.errors[method] = errorMsg
        elif result == 2:
            self.fatal += 1
            self.errors[method] = errorMsg
        else:
            self.invalidReturn += 1
        self.total += 1
                    
    def report(self, CLASS):
        CLASSSTRING = str(CLASS).split('.')[1].split(' ')[0]
        REPORT = f""">>> UNIT TEST REPORT FOR: {CLASSSTRING} <<<

        METHODS FATAL:   {self.fatal},
        METHODS FAILED:  {self.failed},
        METHODS PASSED:  {self.passed},
        METHODS INVALID: {self.invalidReturn}

        METHODS TOTAL:  {self.total}\n\n>>> ERROR MESSAGE(S) <<<
        {self.generateErrorMsgs(CLASSSTRING)}
        """
        print(REPORT)
    
    def generateErrorMsgs(self, CLASSSTRING):
        ERRORMSGS = ""
        for keys in self.errors:
            ERRORMSGS += f"\nMETHOD: {CLASSSTRING}.{keys}()\nERROR:  {self.errors[keys]}\n\n"
        return ERRORMSGS