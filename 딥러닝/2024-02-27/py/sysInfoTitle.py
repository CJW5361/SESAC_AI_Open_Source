import sys

class Line:
    def __init__(self,char='-',count=100):
        self.char = char
        self.count = count
        
    def LinePrn(self,char=None, count=None):
        if char is None:
            char = self.char
        if count is None:
            count = self.count
             
        print('\n▶', char * count)
        
class PythonTitlePrinter(Line):
    def sysInfo(self): 
        super().__init__()
        # self.LinePrn() 
        info=[]
        info.append("▷ Python Version:"+ sys.version)
        info.append("▷ Python Implementation:"+ sys.implementation.name)
        info.append("▷ Python Compiler:"+ sys.version.split()[0])
        info.append("▷ Python Build Number:"+sys.version.split()[2])
        # self.LinePrn('#',100)
        info_str='\n'.join(info)
        return info_str

# 예제 사용
# python_title_printer = PythonTitlePrinter()
# python_title_printer.sysInfo()
