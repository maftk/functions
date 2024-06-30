from .trypo import tryport
make_addplot=tryport('mplfinance').make_addplot
import datetime
from dateutil.relativedelta import relativedelta
def mkplots(df=None,plots=None,ax=None,panel=0,title=None):
  mk= []
  fill = []
  wid = 1
  alpha = .1
  share = dict(panel=panel,secondary_y=False)
  if title=='cloud':
    y1,y2 = df['plus26'].values,df['plus52'].values
    fill+=[dict(y1=y1, y2=y2, where=y1 >= y2, facecolor='lightcoral', alpha=alpha)]
    fill+=[dict(y1=y1, y2=y2, where=y1 < y2, facecolor='lightblue', alpha=alpha)]
  if title=='dmi':
    y1,y2=df['+di'].values,df['-di'].values
    fill+=[dict(y1=y1, y2=y2, where=y1>=y2, facecolor='lightcoral', alpha=alpha)]
    fill+=[dict(y1=y1, y2=y2, where=y1<y2, facecolor='lightblue', alpha=alpha)]
  if title=='macd':
    mk+=[make_addplot(df[plots.pop(2)],**share,type='bar',color='m')]
  if title=='rsi':
    mk+=[make_addplot([70]*len(df.index),**share,color='r',width=wid)]
    mk+=[make_addplot([50]*len(df.index),**share,color='r',width=wid)]
    mk+=[make_addplot([30]*len(df.index),**share,color='r',width=wid)]
  if title=='fkd':
    mk+=[make_addplot([80]*len(df.index),**share,color='r',width=wid)]
    mk+=[make_addplot([50]*len(df.index),**share,color='r',width=wid)]
    mk+=[make_addplot([20]*len(df.index),**share,color='r',width=wid)]
  if not fill:
    mk+= [make_addplot(df[plots],**share)]
  elif fill:
    mk+= [make_addplot(df[plots],**share,fill_between=fill)]
  return mk
def mksignal(df=None,pos=None,panel=0,buy=True,sell=False):
  c = 'Close'
  mk = []
  if buy:
    buydf = df[[c,pos]]
    buydf.loc[buydf[pos].isin([0,-1]),c] = None
    mk += [make_addplot(buydf[c],scatter=True,markersize=100,marker='^',color='r')]
  if sell:
    selldf = df[[c,pos]]
    selldf.loc[selldf[pos].isin([0,1]),c] = None
    mk += [make_addplot(selldf[c],scatter=True,markersize=100,marker='v',color='b')]
  return mk
def setdate(df=None,month=3):
  ed = df.index[-1]+datetime.timedelta(days=1)
  st = ed - relativedelta(months=month)
  idx = df[(df.index > st) & (df.index < ed)].index
  return df.loc[idx]
