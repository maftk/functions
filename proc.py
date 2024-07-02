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
