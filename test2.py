# coding : utf-8
#x*sin(x)-1=0の解を求める。
import math

x0=float(input("初期値："))
xn=x0
for i in range(5):

    xn=xn-(xn*(math.sin(xn))-1)/((math.sin(xn))+xn*(math.cos(xn)))
    print(str(i+1)+"回目の反復解"+str(xn))