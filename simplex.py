import numpy as np
import time

class SimplexTable:
  def __init__(self, v_cnt,s_cnt, obj, e_left, e_right, e_compare):
    self.v_cnt = v_cnt  # 変数の数
    self.s_cnt = s_cnt  # スラック変数と制約の数
    self.bases = np.zeros(s_cnt+v_cnt)  # 基底変数のビット
    self.obj = obj  # 目的関数の係数
    self.e_left=e_left
    self.e_right=e_right
    self.e_compare=e_compare
    self.count=0         #基底の入れ換え操作の回数
    self.ans= np.zeros(s_cnt+v_cnt)     #最適解を入れるリスト
    
#スラック変数に当たるビットを1にする
    i=self.v_cnt
    while i<self.v_cnt+self.s_cnt:        
        self.bases[i]=1
        i+=1    
    print("bases list:")
    print(self.bases)
    self.table=self._create_table()


  def _create_table(self):
    c_table=np.zeros((self.s_cnt+1,self.v_cnt+self.s_cnt+1))  #このメソッド内だけの名前で０行列を作る


    c_table[1:self.s_cnt+1, 1:self.v_cnt+1] = self.e_left  # 制約式の左辺の係数
    self.obj=-1*self.obj
    print(self.obj)
    c_table[0, 1:self.v_cnt+1] = self.obj

    for i in range(s_cnt):
        c_table[i+1, self.v_cnt + i+1] = 1  # 基底のスラック変数を追加（１の要素）
        c_table[i+1, 0] = self.e_right[i]  # 右辺の値を設定
    print(c_table)

    return c_table          #生成した行列を__init__の中に戻す


 
  def solution(self):
    for i in range(self.s_cnt+self.v_cnt):
      if self.bases[i]==1:
        for j in range(self.s_cnt):
          if self.table[j+1][i+1]==1:
            self.ans[i]=self.table[j+1][0]

    return self.ans


  def choose_pivot(self):           #ピボットを選ぶ関数
    i=1
    pivot_row=0                     #ピボット列初期化（0のままだと基底にすべき変数がなかったことを表す）
    while i<=self.v_cnt+self.s_cnt:                     #変数の数だけループ
      if self.table[0][i]>0:
        if pivot_row==0:            #初めて正の要素が来たらその列をピボット候補に
          pivot_row=i
        else:
          if self.table[0][pivot_row]<self.table[0][i]:        #目的関数の中で係数が大きいものを選ぶ
            pivot_row=i                                 #ピボットする列の番号
      i+=1

    if pivot_row!=0:
        print("\npivot row:"+str(pivot_row))

    if pivot_row==0 and self.count!=0:                    #基底の入れ換えを一度でもした後で基底にすべき変数がないとき
        print("最適解に到達しました。")
        self.ans=self.solution() 
        print(self.ans)


    if pivot_row==0 and self.count==0:                    #基底の入れ換えを一度もせず基底にすべき変数がないとき
        print("二段階法をする必要があります。") 
    if pivot_row!=0:                                     #基底の入れ換えをすべきとき
      for i in range(self.s_cnt):             #制約の数だけループ
        if self.table[i+1][pivot_row]>0:
          ratio=self.table[i+1][0]/self.table[i+1][pivot_row]           #列ごとに比を計算
        print("ratio:"+str(ratio))
        if i==0:
          min_ratio=ratio                #最初の値は比の最小値に入れる
          pivot_col=1
        if ratio<min_ratio:               #今考えている比が暫定最小比よりも小さいとき
          min_ratio=ratio
          pivot_col=i+1
      print("minimum ratio:"+str(min_ratio))
      print("pivot:"+str(pivot_col)+","+str(pivot_row))

      self.swapping_bases(pivot_col,pivot_row)


  def swapping_bases(self,pivot_col,pivot_row):      #基底の入れ替え
    a=self.table[pivot_col][pivot_row]                #分母a
    for i in range(self.s_cnt+self.v_cnt+1):
      self.table[pivot_col][i]=self.table[pivot_col][i]/a    #ピボット行を選んだ要素で割る

   #（すべての行-ピボット行）をする
    for i in range(self.s_cnt+1):     #i行
      b=self.table[i][pivot_row]         #ピボット列の数字をbに入れる
      for j in range(self.s_cnt+self.v_cnt+1):  #j列
        if(i!=pivot_col):
         self.table[i][j]=self.table[i][j]-b*self.table[pivot_col][j]    #各行からb倍したピボット行を引く

    #基底変数を表すリストを更新(基底を1に非基底を0に)
    self.bases[pivot_row-1]=1
    self.bases[pivot_col+self.v_cnt-1]=0    
    self.count+=1   #回数を＋1

    print("\n"+str(self.count)+" time bases list:")
    print(self.bases)
    print(self.table)
    
    self.choose_pivot()

#目的関数の係数
obj=np.array([-4,-3])

#制約式の係数と右辺
e_left=np.array([[1,2],
                [12,18],
                [6,4]])
e_right=np.array([2,19,7])

#不等号の向き（<=のときLess）Lessの場合のみを考える
e_compare = ['Less', 'Less']

# スラック変数の数＝制約の数
s_cnt = len(e_right)


#制約の数
#e_cnt=len(e_right)

start=time.time()
simplex_table = SimplexTable(v_cnt=2, s_cnt=s_cnt, obj=obj, e_left=e_left, e_right=e_right, e_compare=e_compare)
simplex_table.choose_pivot()

finish=time.time()

jikan=finish-start
print("Time:"+str(jikan))