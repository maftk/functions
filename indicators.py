import numpy as np
import pandas as pd

def sma(df=None,sw=5,lw=25):
  s = f'sma{sw}'
  l = f'sma{lw}'
  df[s] = df['Close'].rolling(window=sw,min_periods=1).mean()
  df[l] = df['Close'].rolling(window=lw,min_periods=1).mean()
  # smac の計算
  smac = np.where(df[s] > df[l], 1, 0)
  # smapos の計算
  df['smapos'] = np.concatenate(([0], np.diff(smac)))
  return df
##指数平滑移動平均
def ema(df=None,sw=5,lw=25):
  sema = f'ema{sw}'
  lema = f'ema{lw}'
  df[sema] = df['Close'].ewm(span=sw,).mean()
  df[lema] = df['Close'].ewm(span=lw,).mean()
  df['emapos'] = np.concatenate(([0],np.diff(np.where(df[sema] > df[lema], 1, 0))))
  return df
##移動平均収束拡散法
def macd(df=None,sw=12,lw=26,sig=9):
  a = df['Close'].ewm(span=sw,).mean()
  b = df['Close'].ewm(span=lw,).mean()
  df['macd'] = a - b 
  df['macdsig'] = df['macd'].ewm(sig).mean()
  df['macdhis'] = df['macd'] - df['macdsig']
  df.loc[df['Close'].isna(),['macd','macdsig','macdhis']] = np.nan
  df['macdpos'] = np.concatenate(([0],np.diff(np.where(df['macd'] > df['macdsig'],1,0))))

  return df
#ボラティリティ系
##ボリンジャーバンド
def bband(df=None,n=25):
  # N期間の移動平均線(SMA)を計算
  df['sma'] = df['Close'].rolling(window=n).mean()
  # 上部バンドを計算
  std_dev = 2
  df['ub'] = df['sma'] + std_dev * df['Close'].rolling(window=n).std()
  # 下部バンドを計算
  df['lb'] = df['sma'] - std_dev * df['Close'].rolling(window=n).std()
  # 売買シグナルの検出
  bbbuy = np.where(df['Close'] < df['lb'], 1, 0)
  bbsel = np.where(df['Close'] > df['ub'], -1, 0)
  df['bbpos'] = bbbuy + bbsel
  return df
def rsi(df=None,w=12):
  # w = 12
  delta = df['Close'].diff()
  gain = (delta.where(delta > 0,0)).rolling(w).mean()
  loss = (-delta.where(delta<0,0)).rolling(w).mean()
  rs = gain / loss
  df['rsi'] = 100 - (100 / (1 + rs))
  # 売買の判定（RSIが70を超えたら売り、30を下回ったら買いとする）
  df.loc[df['Close'].isna(),'rsi'] = np.nan
  df['rsipos'] = np.where(df['rsi'] > 70, -1, np.where(df['rsi'] < 30, 1, 0))
  return df
def fkd(df=None):
  # ロープライスを計算
  llow = df['Low'].rolling(window=14).min()
  # ハイプライスを計算
  hhigh = df['High'].rolling(window=14).max()
  # ストキャスティクスの%Kを計算
  df['%k'] = ((df['Close'] - llow) / (hhigh - llow) * 100)
  # %Dを計算
  df['%d'] = df['%k'].rolling(window=3).mean()
  # ポジション決定
  df['fkdpos'] = 0
  df.loc[(df['%k'] > df['%d']) & (df['%k'] < 20), 'fkdpos'] = 1
  df.loc[(df['%k'] < df['%d']) & (df['%k'] > 80), 'fkdpos'] = -1
  # df.loc[(df['%k'] > df['%d']), 'fkdpos'] = 1
  # df.loc[(df['%k'] < df['%d']), 'fkdpos'] = -1
  return df
def dmi(df=None):
  n=14
  # True Range (TR) の計算
  tr = np.maximum(df['High'] - df['Low'],  np.abs(df['High'] - df['Close'].shift(1)),  np.abs(df['Low'] - df['Close'].shift(1)))
  # +DM と -DM の計算
  pdm = np.where((df['High'] - df['High'].shift(1)) > (df['Low'].shift(1) - df['Low']),  np.maximum(df['High'] - df['High'].shift(1), 0), 0)
  spdm = pd.Series(pdm).ewm(n).mean().values  # n は平滑化の期間
  smtr = pd.Series(tr).ewm(n).mean().values  # n はTRの平滑化の期間

  df['+di'] = (spdm / smtr) * 100
  mdm = np.where((df['Low'].shift(1) - df['Low']) > (df['High'] - df['High'].shift(1)),  np.maximum(df['Low'].shift(1) - df['Low'], 0), 0)
  smdm = pd.Series(mdm).ewm(n).mean().values  # n は平滑化の期間
  df['-di'] = (smdm / smtr) * 100
  adx = (np.abs(df['+di'] - df['-di']) / (df['+di'] + df['-di'])) * 100
  df['adx'] = adx.ewm(n).mean()  # n はADXの平滑化の期間

  # DMIの方向を表す dmipos 列の計算
  df.loc[df['Close'].isna(),['+di','-di','adx']] = np.nan
  df['dmipos'] = np.concatenate(([0], np.diff(np.where(df['+di'] > df['-di'], 1, 0))))
  return df
def cloud(df=None):
  high9 = df['High'].rolling(window=9).max()
  low9 = df['Low'].rolling(window=9).min()
  df['hlm9'] = ((high9 + low9) / 2)
  high26 = df['High'].rolling(26).max()
  low26 = df['Low'].rolling(26).min()
  df['hlm26'] = ((high26 + low26) / 2)
  high52 = df['High'].rolling(52).max()
  low52 = df['Low'].rolling(52).min()
  df['minus26'] = df['Close'].shift(-26)
  # 新しいインデックスを作成
  st = df.index[-1]
  dates = pd.date_range(start=st + pd.Timedelta(days=1), end=st+pd.Timedelta(days=30))
  idx = pd.DatetimeIndex(dates)
  # 新しいDataFrameを作成して、新しいインデックスを設定
  dx = pd.DataFrame(index=idx)
  df = pd.concat([df,dx])
  df['plus26'] = ((high26 + low26) / 2)
  df['plus26'] = df['plus26'].shift(26)
  df['plus52'] = ((high52 + low52) / 2)
  df['plus52'] = df['plus52'].shift(26)

  df['cloudpos'] = np.concatenate(([0], np.diff(np.where(df['Close'] > df['Close'].shift(26), 1, 0))))

  return df

indicts = {
    "sma":sma,
    "ema":ema,
    "macd": macd,
    "bband":bband,
    "rsi":rsi,
    "fkd":fkd,
    'dmi':dmi,
    'cloud':cloud,
  }
