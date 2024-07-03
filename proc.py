import numpy as np
def rfromc(df):
  x = df.copy()
  x['Open'] = df.Open / df.Close.shift(1)
  x['High'] = df.High / df.Close.shift(1)
  x['Low'] = df.Low / df.Close.shift(1)
  x['Close'] = df.Close / df.Close.shift(1)
  x = x.drop(['Adj Close','Volume'],axis=1)
  for i in range(1,4):
    for a in ['Open','High','Low','Close']:
      x[f'{i}{a}'] = x[a].shift(i)
  x = x.dropna()
  return x

def priceagos(df,ago=5):
  df = df.copy()
  df = df.drop(['Adj Close','Volume'],axis=1)
  for i in range(ago):
    for a in ['Open','High','Low','Close']:
      df[f'{i+1}{a}'] = df[a].shift(i)
  df = df.dropna()
  return df

def mergedfs(tickers,data,func,scaler,**kwargs):
  flag = True
  for tik in tickers:
    df = data[tik].copy()
    df = func(df,**kwargs)
    scaler.fit(df)
    df = scaler.fit_transform(df)
    leng = int(df.shape[0] * .9)
    df = df[:leng].copy()
    if flag:
      X = df.copy()
      flag = False
    else:
      X = np.concatenate((X, df), axis=0)
  return X
