from sklearn.preprocessing import MinMaxScaler
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
  x = df.copy()
  x = x.drop(['Adj Close','Volume'],axis=1)
  for i in range(ago):
    for a in ['Open','High','Low','Close']:
      x[f'{i+1}{a}'] = x[a].shift(i)
  x = x.dropna()
  return x

def mergedfs(tickers,data,func,scaler,**kwargs):
  flag = True
  for tik in tickers:
    df = data[tik].copy()
    scaler.fit(df)
    df = scaler.fit_transform(df)
    x = func(df,**kwargs)
    if flag:
      X = x.copy()
      flag = False
    else:
      X = np.concatenate((X, x), axis=0)
  return X
