﻿import numpy as np
import time

class SimplexTable:
  def __init__(self, v_cnt,s_cnt,a_cnt, obj, e_left, e_right, e_compare):
    self.v_cnt = v_cnt  # 変数の数
    self.s_cnt = s_cnt  # スラック変数と制約の数
    self.a_cnt=a_cnt    #人為変数の数
    self.bases = np.zeros(s_cnt+v_cnt+a_cnt)  # 基底変数のビットで表したリスト
    self.obj = -1*obj  # 目的関数の係数(表に書くために－１倍)
    self.e_left=e_left
    self.e_right=e_right
    self.e_compare=e_compare
    self.count=0         #基底の入れ換え操作の回数
    self.ans= np.zeros(s_cnt+v_cnt+a_cnt)     #最適解を入れるリスト
    self.bcol=np.zeros(len(e_right))   #基底の数だけ要素を持つリスト
    self.jinigyou=np.zeros(a_cnt)  #人為変数の1がある行を保存するリスト

    self.end=0      #最適解に到達したら1にしてすべてのメソッドから出る

    self.min=0      #最適解を入れる

    self.sol=0

    if a_cnt!=0:#目的関数の数が2つ必要な時
       self.o_cnt=2
    else:     #二段階法がいらないとき、または二段階法のフェーズ2
       self.o_cnt=1
    
#基底変数に当たる要素を1にする
    if a_cnt==0:  #二段階法しないとき
        i=self.v_cnt
        while i<self.v_cnt+self.s_cnt:        
            self.bases[i]=1
            i+=1    
            
    self.table=self._create_table()
 
 #ここは没案   
#   if a_cnt==0:            #二段階法を適用しなくてよいとき
#     self.set_value1()
#   if a_cnt>0:             #二段階法を適用するとき


#二段階法をするしないに問わずset_value2()に行く
    self.set_value2()
    
    if a_cnt>0:             #二段階法を適用するとき
        print("phase 1")
    print("bases list:")
    print(self.bases)
    print(self.table)

  def _create_table(self):
    c_table=np.zeros((len(self.e_left)+self.o_cnt,self.v_cnt+self.s_cnt+self.a_cnt+1))  #このメソッド内だけの名前で０行列を作る。行の数を基底変数+目的関数の数にする(基底変数の数と制約式の数は等しい)
    c_table[self.o_cnt:len(self.e_right)+self.o_cnt, 1:self.v_cnt+1] = self.e_left  # 制約式の左辺の係数
        
    c_table[self.o_cnt-1, 1:self.v_cnt+1] = self.obj
  
    return c_table          #生成した行列を__init__の中に戻す
    
    
    
#ここは没案、二段階法をしないときに使うつもりだった   
#  def set_value1(self):
#    for i in range(s_cnt):
#            self.table[i+self.o_cnt, self.v_cnt + i+1] = 1  # 基底のスラック変数を追加（１の要素）
#            self.table[i+1, 0] = self.e_right[i]  # 右辺の値を設定




  def set_value2(self):      #二段階法をするときのメソッド
        j=0 #スラック変数を記入する列に使う(0からs_cnt-1まで変化)
        k=0 #人為変数変数を記入する列に使う(0からa_cnt-1まで変化)
        m=0 
        n=0
        for i in range(len(self.e_right)):  #iは行に使う
            self.table[i+self.o_cnt, 0] = self.e_right[i]  # 右辺の値を設定
            #スラック変数と人為の係数を表に書く(行ごとに)
            if self.e_compare[i]=="Less":
                self.table[i+self.o_cnt][j+self.v_cnt+1]=1
                self.bases[j+self.v_cnt]=1      #Lessのスラック変数は基底
                self.bcol[m]=j+self.v_cnt  #基底変数の要素番号を保存
                j+=1
                m+=1
            if self.e_compare[i]=="Greater":
                self.table[i+self.o_cnt][j+self.v_cnt+1]=-1     #スラック変数は係数-1
                j+=1
                self.table[i+self.o_cnt][k+self.v_cnt+(self.s_cnt)+1]=1     #人為変数は1
                self.bases[k+self.v_cnt+(self.s_cnt)]=1
                self.jinigyou[n]=i+self.o_cnt  #人為変数のある行を目的関数行に足すのに使うjinigyou
                self.bcol[m]=k+self.v_cnt+(self.s_cnt)  #基底変数の要素番号を保存
                m+=1
                k+=1
                n+=1
            if self.e_compare[i]=="Equal":
                self.table[i+self.o_cnt][k+self.v_cnt+(self.s_cnt)+1]=1
                self.bases[k+self.v_cnt+(self.s_cnt)]=1
                self.bcol[m]=k+self.v_cnt+(self.s_cnt)  #基底変数の要素番号を保存
                self.jinigyou[n]=i+self.o_cnt
                n+=1
                m+=1
                k+=1
#        print(self.jinigyou)
        if self.a_cnt>0:  #二段階法するとき
            for i in range(self.v_cnt+self.s_cnt+1):
                for j in range(self.a_cnt):
                    col=self.jinigyou[j]
                    self.table[0][i]=self.table[0][i]+self.table[int(col)][i]  #フェーズ1の目的関数行に制約行をたす(人為変数を基底にするため)
 
  def solution(self):
    print(self.bcol)
    for i in range(self.s_cnt+self.v_cnt):
      if self.bases[i]==1:
        for j in range(len(self.e_right)):
          if self.table[j+1][i+1]==1:
            self.ans[i]=self.table[j+1][0]

    return self.ans

  def choose_row(self):
    if self.end==1:
       return
    i=1
    pivot_row=0                     #ピボット列初期化（0のままだと基底にすべき変数がなかったことを表す）

    
    while i<=self.v_cnt+self.s_cnt+self.a_cnt:                     #変数の数だけループ
      if self.table[0][i]>0:
        if pivot_row==0:            #初めて正の要素が来たらその列をピボット候補に
            pivot_row=i
        else:
            if self.table[0][pivot_row]<self.table[0][i]:        #目的関数の中で係数が大きいものを選ぶ
              pivot_row=i                                 #ピボットする列の番号
      i+=1
    return pivot_row


  def choose_col(self,pivot_row):
    if self.end==1:
       return
    
    min_ratio=-1   #最小の比を-1に初期化(退化するとき比0をとりうるかつ比が負になることはないため)比が負の時は一度も比が計算されていないことを表す    
    if pivot_row!=0:                                     #基底の入れ換えをすべきとき
      for i in range(len(self.e_right)):             #制約の数だけループ
        if self.table[i+self.o_cnt][pivot_row]>0:
          ratio=self.table[i+self.o_cnt][0]/self.table[i+self.o_cnt][pivot_row]           #列ごとに比を計算
          print("ratio:"+str(ratio))
        if self.table[i+self.o_cnt][pivot_row]<=0:     #比を計算しないとき
          ratio=-1           #比がないことを表す
          print("ratio:No calculation required")
 
        if min_ratio==-1 and ratio!=-1:
          min_ratio=ratio                #最初に計算できた比は比の最小値に入れる
          pivot_col=i+self.o_cnt
        if ratio<min_ratio and ratio!=-1:               #今考えている比が暫定最小比よりも小さいとき
          min_ratio=ratio
          pivot_col=i+self.o_cnt
      if min_ratio==-1:
         self.end==1
         return  0#ピボットすべき行がなかったとき処理を終了
      print("minimum ratio:"+str(min_ratio))
      print("pivot:"+str(pivot_col)+","+str(pivot_row))

    return pivot_col


  def choose_pivot(self):           #ピボットを選ぶ関数(フェーズ1・2で2重にchoose_pivotに入る)
    if self.end==1:
       return
    
    pivot_row=self.choose_row()  
    
 
#フェーズ2に移行するとき
    if self.a_cnt!=0 and pivot_row==0 and self.count!=0:
        self.init_phase2()
        return

    if pivot_row!=0:
        print("\npivot row:"+str(pivot_row))

#行列操作の終わり
    if pivot_row==0 and self.count!=0 and self.end==0:                    #基底の入れ換えを一度でもした後で基底にすべき変数がないとき(フェーズ1・2で2重にchoose_pivotに入るためend==0でこの条件に一度のみ入るようにする)
        print("\nThe optimal solution has been reached.")
        self.end=1
        self.ans=self.solution() 
        print(self.ans)
        self.obj=self.obj*-1  #表への記入のために－1倍したものを戻す
        print("\noptimal solution:")
        for i in range(self.v_cnt):
          self.min+=self.obj[i]*self.ans[i]
          print(str(self.obj[i])+"*"+str(self.ans[i]), end='')
          if i!=self.v_cnt-1:
             print("+",end='')
        print("="+str(self.min))
        return

    if pivot_row==0 and self.count==0:                    #基底の入れ換えを一度もせず基底にすべき変数がないとき
        print("Pivot selection error")
        return
   

    pivot_col=self.choose_col(pivot_row)
    
    if pivot_col==0: #0のとき、すべての行がNo calculation requiredのとき。この条件は非有界の条件としては正しくない！！
        print("unbounded")
        return

    self.swapping_bases(pivot_col,pivot_row)


#基底の入れ替え
  def swapping_bases(self,pivot_col,pivot_row):      
    if self.end==1:
       return
    
    a=self.table[pivot_col][pivot_row]                #分母a
    for i in range(self.s_cnt+self.v_cnt+self.a_cnt+1):
      self.table[pivot_col][i]=self.table[pivot_col][i]/a    #ピボット行を選んだ要素で割る

   #（すべての行-ピボット行）をする
    for i in range(len(self.e_right)+self.o_cnt):     #iは行(基底の数＋目的関数の数だけループ)
      b=self.table[i][pivot_row]         #ピボット列の数字をbに入れる
      for j in range(self.s_cnt+self.v_cnt+self.a_cnt+1):  #j列
        if(i!=pivot_col):
         self.table[i][j]=self.table[i][j]-b*self.table[pivot_col][j]    #各行からb倍したピボット行を引く

    print(self.bcol)
    #基底変数を表すリストを更新(基底を1に非基底を0に)
    self.bases[pivot_row-1]=1
    b=self.bcol[pivot_col-self.o_cnt]    #bは小数になっている
    self.bases[int(b)]=0        #basesのb番目を0にする
    self.count+=1   #回数を＋1
    self.bcol[pivot_col-self.o_cnt]=pivot_row-1
    print("\n"+str(self.count)+" time bases list:")
    print(self.bases)
    print(np.round(self.table,3))               #小数点以下を三桁で表示
    
    self.choose_pivot()

#フェーズ2の数値設定
  def init_phase2(self):
    if self.end==1:
       return
   
   
#ここで人為変数に基底があるとき、フェーズ2に以降せず実行不可能な問題であると表示
    i=self.v_cnt+self.s_cnt+1
    while i<self.v_cnt+self.s_cnt+self.a_cnt+1:
       if self.table[0][i]==0:
          print("This problem is not possible")
          self.end=1
          return    
       i+=1 
   
      
    print("Phase 1 completed\n--------------\nPhase 2")
    self.count=0  #試行回数の初期化
    self.o_cnt=1  #目的関数の数を１に
    self.a_cnt=0  #人為変数列はいらないため０に（a_cnt==0のとき二段階法をしなくなる）  
    copy=self.table
    self.table=np.zeros((len(self.e_left)+self.o_cnt,self.v_cnt+self.s_cnt+1))  #人為変数列とフェーズ1の目的関数行を消した要素０のリスト
    self.table=copy[1:len(self.e_right)+2,0:self.v_cnt+self.s_cnt+1]
    copy=self.bases
    self.bases=np.zeros(s_cnt+v_cnt)
    self.bases=copy[0:self.v_cnt+self.s_cnt]
    print(self.bases)
    print(self.table)
    self.ans= np.zeros(s_cnt+v_cnt) 

    self.choose_pivot()




'''
#制約がGreaterだけの問題
#目的関数の係数
obj=np.array([3,2])
#制約式の係数と右辺
e_left=np.array([[2,1],
                [4,3],
                [5,4]])
e_right=np.array([20,56,73])
#不等号の向き（<=のときLess,>=のときGreater,=のときEqual）
e_compare = ['Greater', 'Greater','Greater']
'''
'''
#上の問題をLessのみに書き換える
#目的関数の係数
obj=np.array([3,2])
#制約式の係数と右辺
e_left=np.array([[-2,-1],
                [-4,-3],
                [-5,-4]])
e_right=np.array([-20,-56,-73])
#不等号の向き（<=のときLess,>=のときGreater,=のときEqual）
e_compare = ['Less', 'Less','Less']
'''

'''
#一つ目の制約をGreaterにする（非負条件違反）
#目的関数の係数
obj=np.array([3,2])
#制約式の係数と右辺
e_left=np.array([[2,1],
                [-4,-3],
                [-5,-4]])
e_right=np.array([20,-56,-73])
#不等号の向き（<=のときLess,>=のときGreater,=のときEqual）
e_compare = ['Greater', 'Less','Less']
'''

'''
#二つ目の制約をGreaterへ（非負条件違反）
#目的関数の係数
obj=np.array([3,2])
#制約式の係数と右辺
e_left=np.array([[-2,-1],
                [4,3],
                [-5,-4]])
e_right=np.array([-20,56,-73])
#不等号の向き（<=のときLess,>=のときGreater,=のときEqual）
e_compare = ['Less', 'Greater','Less']
'''


'''
#制約がGreaterだけの問題を三つ目の制約をGreater（非負条件違反）
#目的関数の係数
obj=np.array([3,2])
#制約式の係数と右辺
e_left=np.array([[-2,-1],
                [-4,-3],
                [5,4]])
e_right=np.array([-20,-56,73])
#不等号の向き（<=のときLess,>=のときGreater,=のときEqual）
e_compare = ['Less', 'Less','Greater']
'''





'''
#制約がLessだけの例題
obj=np.array([-4,-3])
#制約式の係数と右辺
e_left=np.array([[1,2],
                [12,18],
                [6,4]])
e_right=np.array([2,19,7])
#不等号の向き（<=のときLess）Lessの場合のみを考える
e_compare = ['Less', 'Less','Less']
'''



'''
#上の制約がLessだけの例題を制約式―1倍した問題
obj=np.array([-4,-3])
#制約式の係数と右辺
e_left=np.array([[-1,-2],
                [-12,-18],
                [-6,-4]])
e_right=np.array([-2,-19,-7])
#不等号の向き（<=のときLess）Lessの場合のみを考える
e_compare = ['Greater', 'Greater','Greater']
'''


'''
#制約がGreater,Less,Equalの問題
obj=np.array([-2,-3])
e_left=np.array([[2,5],
                [3,2],
                [1,2]])
e_right=np.array([20,14,6])
e_compare=['Less','Greater','Equal']
'''

#制約がGreater,Less,Equalの問題
obj=np.array([-2,-3])
e_left=np.array([[2,5],
                [3,2],
                [1,2],
                [1,2]])
e_right=np.array([20,14,6,6])
e_compare=['Less','Greater','Less','Greater']


'''
#実行不可能な問題
obj=np.array([-2,3])
e_left=np.array([[4,3],
                [-1,1],
                [2,5]])
e_right=np.array([11,6,9])
e_compare=['Less','Greater','Greater']
'''



'''
#非有界の問題
obj=np.array([-1,-1])
e_left=np.array([[-1,-1],
                [-2,1],
                [1,-2]])
e_right=np.array([-1,1,1])
e_compare=['Less','Less','Less']
'''

'''
#退化する問題
obj=np.array([-16, -19, -23, -28])
e_left=np.array([[2,3,4,5],
                [1,0,0,0],
                [0,1,0,0],
                [0,0,1,0],
                [0,0,0,1]])
e_right=np.array([7,1,1,1,1])
e_compare=['Less','Less','Less','Less','Less']
'''

'''
#一度もピボット操作をしないで最適解＝0の問題(すべての変数＝0のとき最適解)
#このときピボットエラーで最適解を表示できない(実行可能解にたどり着けていない場合との書き分けができていない)
obj=np.array([3,5])
e_left=np.array([[1,2],
                [1,1]])
e_right=np.array([0,0,])
e_compare=['Less','Less']
'''

'''
#scipyでの比較問題
obj=np.array([-1,4])
e_left=np.array([[-3,1],
                [1,2],
                [0,-1]])
e_right=np.array([6,4,3])
e_compare=['Less','Less','Less']
'''

'''
#memo
obj=np.array([-10,57,9,24,0,0,0])
e_left=np.array([[-0.5,5.5,2.5,-9,-1,0,0],
                [-0.5,1.5,0.5,-1,0,-1,0],
                [1,0,0,0,0,0,1]])
e_right=np.array([0,0,0])
e_compare=['Equal','Equal','Equal']


obj=np.array([0,-53,-41,204,20,0,0])
e_left=np.array([[-1,11,5,-18,-2,0,0],
                [0,-4,-2,8,1,-1,0],
                [0,-11,-5,18,2,0,-1]])
e_right=np.array([0,0,-1])
e_compare=['Equal','Equal','Equal']
'''

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
