from linear_relaxation import SimplexTable
import numpy as np
import time


#
obj=np.array([-3, -4, -5, -6])  #最大化を考えるので―1倍
e_left=np.array([[2,3,4,5],
                [1,0,0,0],
                [0,1,0,0],
                [0,0,1,0],
                [0,0,0,1]])
e_right=np.array([5,1,1,1,1])
e_compare=['Less','Less','Less','Less','Less']

v_cnt=len(obj) #変数の数は目的関数の変数とする
a_cnt=0 #人為変数の数の初期化
s_cnt=0 #スラック変数の数の初期化

#それぞれ変数の数を決める
for cmp in e_compare:
    if cmp=="Greater":
        a_cnt+=1
        s_cnt+=1
    if cmp=="Equal":
        a_cnt+=1
    if cmp=="Less":
        s_cnt+=1

start=time.time()
simplex_table = SimplexTable(v_cnt=v_cnt, s_cnt=s_cnt,a_cnt=a_cnt, obj=obj, e_left=e_left, e_right=e_right, e_compare=e_compare)
simplex_table.choose_pivot()

finish=time.time()

jikan=finish-start
print("\nTime:"+str(jikan))

