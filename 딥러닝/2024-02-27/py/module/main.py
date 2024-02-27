import test 
from pathlib import Path

FILE=Path(__file__).resolve()
ROOT=FILE.parents[0]
ROOT1=FILE.parents[1]

print(FILE)
print(ROOT)
print(ROOT1)

path=str(FILE.parents[1])+'\\txt\\'
file='val.txt'
with open(path+file,'r')as f:
    content = f.readlines()
    
test.prn(content)
