# coding : utf-8
#x^3-3=0の解を求める。

x0=float(input("初期値："))
xn=x0
for i in range(5):
    xn=xn-(xn*xn*xn-3)/(3*xn*xn)
    print(str(i+1)+"回目の反復解"+str(xn))