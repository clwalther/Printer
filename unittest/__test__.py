def test(element):
    element._test = True
    return element
def before(element):
    element._before = True
    return element
def after(element):
    element._after = True
    return element

class Unittest():
    def __init__(self, CLASS):
        # init
        self.CLASS = CLASS

        # vals
        self.fatal  = 0
        self.failed = 0
        self.passed = 0
        self.invalidReturn = 0

        self.total  = 0
        self.errors = {}

        self.methods  = [[], [], []]
        self.classStr = str(self.CLASS).split('.')[1].split(' ')[0]

    def run(self):
        self.getMethods()
        self.runMethods()
        self.getReport()

    def getMethods(self):
        for index in range(len(dir(self.CLASS))):
            methodStr = dir(self.CLASS)[index]
            method    = getattr(self.CLASS, methodStr)
            if callable(method):
                if getattr(method, "_before", False):
                    self.methods[0].append(methodStr)
                elif getattr(method, "_test",   False):
                    self.methods[1].append(methodStr)
                elif getattr(method, "_after",  False):
                    self.methods[2].append(methodStr)

    def runMethods(self):
        for methodStr in self.methods[0]:
            getattr(self.CLASS, methodStr)()

        for methodStr in self.methods[1]:
            try:
                result = getattr(self.CLASS, methodStr)()
                self.methodEval(result, methodStr, None)
            except Exception as errorMsg:
                result = 2 # <--- fatal
                self.methodEval(result, methodStr, errorMsg)

        for methodStr in self.methods[2]:
            getattr(self.CLASS, methodStr)()

    def methodEval(self, result, methodStr, errorMsg):
        if   result == 0:
            self.passed += 1
        elif result == 1:
            self.failed += 1
            self.errors[methodStr] = errorMsg
        elif result == 2:
            self.fatal  += 1
            self.errors[methodStr] = errorMsg
        else:
            self.invalidReturn += 1
        self.total += 1

    def getReport(self):
        errorMsgs = self.generateErrorMsgs()
        report = f""">>> UNITTEST REPORT FOR: {self.classStr} <<<

        METHODS FATAL:   {self.fatal},
        METHODS FAILED:  {self.failed},
        METHODS PASSED:  {self.passed},
        METHODS INVALID: {self.invalidReturn},

        METHODS TOAL:    {self.total}
        \n>>> ERROR MESSAGE(S) <<<
        {errorMsgs}
        """
        print(report)
    
    def generateErrorMsgs(self):
        errorMsgs = ""
        for methodName in self.errors.keys():
            if not self.errors[methodName] == None:
                errorMsgs += f"\nMETHOD: {self.classStr}.{methodName}()\nERROR:  {self.errors[methodName]}\n\n"
        return errorMsgs