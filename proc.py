import numpy as np
def rfromc(temp,day_ago=4):
    tec = [ 'Open', 'High', 'Low', 'Close', ]
    num_sihyou = len(tec)
    temp = temp[tec]
    temp = temp.dropna(subset=['Close'])
    temp2 = np.array(temp)
    temp3 = np.zeros((len(temp2)-1, num_sihyou*2))
    for i in range(num_sihyou):
      temp3[:, i] = temp2[1:, i] / temp2[:-1, -1]
    # if num_sihyou>=4:
    #   for n in range(4,num_sihyou):
    #     temp3[0:len(temp3),n] = temp2[base-1:len(temp2)-1,n]
    # # tempX : 現在の企業のデータ
    # 日にちごとに横向きに（day_ago）分並べる
    # sckit-learnは過去の情報を学習できないので、複数日（day_ago）分を特微量に加える必要がある
    # 注：tempX[0:day_ago]分は欠如データが生まれる
    tempX = np.zeros((len(temp3), day_ago*num_sihyou))
    for s in range(0, num_sihyou):
        for i in range(0, day_ago):
            tempX[i:len(temp3), day_ago*s+i] = temp3[0:len(temp3)-i,s]
    return tempX[day_ago:]
    # return temp3
