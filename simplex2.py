import numpy as np

class SimplexTable:
  def __init__(self, v_cnt,s_cnt, obj, e_left, e_right, e_compare):
    self.v_cnt = v_cnt  # 変数の数
    self.s_cnt = s_cnt  # スラック変数と制約の数
    self.v_idx = np.zeros(s_cnt, dtype=int)  # 基底変数のインデックス
    self.obj = obj  # 目的関数の係数
    self.e_left=e_left
    self.e_right=e_right
    self.e_compare=e_compare


    self.table=self._create_table()

  def _create_table(self):
    self.table=np.zeros((self.s_cnt+1,self.v_cnt+self.s_cnt+1))  #０行列を作る


    self.table[1:self.s_cnt+1, 1:self.v_cnt+1] = self.e_left  # 制約式の左辺の係数
    self.obj=-1*self.obj
    print(self.obj)
    self.table[0, 1:self.v_cnt+1] = self.obj

    for i in range(s_cnt):
        self.table[i+1, self.v_cnt + i+1] = 1  # 基底のスラック変数を追加（１の要素）
        self.table[i+1, 0] = self.e_right[i]  # 右辺の値を設定
    print(self.table)

  def display(self):






#目的関数の係数
obj=np.array([-4,-3])

#制約式の係数と右辺
e_left=np.array([[1,2],
                [12,18],
                [6,4]])
e_right=np.array([2,19,7])

#不等号の向き（<=のときLess）
e_compare = ['Less', 'Less']

# スラック変数の数＝制約の数
s_cnt = len(e_right)


#制約の数
#e_cnt=len(e_right)

simplex_table = SimplexTable(v_cnt=2, s_cnt=s_cnt, obj=obj, e_left=e_left, e_right=e_right, e_compare=e_compare)

