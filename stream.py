import streamlit as st
import yfinance as yf
import pandas as pd
import mplfinance as mpf
from functions import cloud,dmi,mkplots

plots = {
  'macd':['macd','macdsig','macdhis','macdpos'],
  'ema':['ema5','ema25','emapos'],
  'bband':['lb','ub','bbpos'],
  'rsi':['rsi','rsipos'],
  'fkd' : ['%k','%d','fkdpos'],
  'dmi' : ['+di','-di','adx','dmipos'],
  'cloud':['minus26','plus26','plus52','cloudpos'],
}

# ページのレイアウト設定をワイドにする
st.set_page_config(layout="wide")

# データをキャッシュする関数
@st.cache_data
def get_stock_data(symbol, start, end):
    df = yf.download(symbol, start=start, end=end)
    return df

# 指標の計算を行う関数
def calculate_indicators(df, ma_period, dmi_period):
    if ma_period:
        df[f'MA_{ma_period}'] = df['Close'].rolling(window=ma_period).mean()
    #
    # if rsi_period:
    #     delta = df['Close'].diff()
    #     gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    #     loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    #     rs = gain / loss
    #     df['RSI'] = 100 - 100 / (1 + rs)
    # if cloud_period:
    #     df = cloud(df)
    if dmi_period:
        df = dmi(df)

    
    return df

# 銘柄シンボルを入力
symbols = st.text_input('銘柄シンボルをカンマで区切って入力 (例: AAPL,MSFT,GOOGL)', 'AAPL,MSFT,GOOGL')

# ダウンロード範囲の指定
download_start_date = pd.to_datetime('2020-01-01')
download_end_date = pd.to_datetime('today')

# ダウンロード範囲の入力
download_start_date_input = st.date_input('ダウンロード開始日', value=download_start_date)
download_end_date_input = st.date_input('ダウンロード終了日（通常は今日）', value=download_end_date)

# デフォルトの表示範囲を現在の日付から3か月前に設定
default_display_start_date = download_end_date - pd.DateOffset(months=3)
default_display_end_date = download_end_date

# シンボルリストを分割
symbols_list = [symbol.strip() for symbol in symbols.split(',')]

# 各銘柄の設定とチャートの描画
for symbol in symbols_list:
    # レイアウト設定 (3:1の比率)
    chart_col, control_col = st.columns([3, 1])

    # 編集項目を設定
    with control_col:
        with st.expander(f'{symbol}の設定を開く', expanded=True):
            # 移動平均線の表示設定
            show_ma = st.checkbox(f'{symbol} MA20', value=True)
            ma_period = 20 if show_ma else None
            #
            # # RSIの表示設定
            # show_rsi = st.checkbox(f'{symbol} RSI', value=True)
            # rsi_period = 14 if show_rsi else None

            # Volumeの表示設定
            show_vol = st.checkbox(f'{symbol} Volume', value=True)

            # show_cloud = st.checkbox(f'cloud {symbol}', value=True)
            # cloud_period = True if show_cloud else None

            show_dmi = st.checkbox(f'dmi {symbol}', value=True)
            dmi_period = True if show_dmi else None

            # 表示範囲の指定
            start_date = st.date_input(f'{symbol}の表示開始日', value=default_display_start_date, key=f'{symbol}_start')
            end_date = st.date_input(f'{symbol}の表示終了日', value=default_display_end_date, key=f'{symbol}_end')
    
    # データ取得（キャッシュされたデータを使用）
    df_full = get_stock_data(symbol, download_start_date_input, download_end_date_input)

    # 指標の計算
    df_full = calculate_indicators(df_full,ma_period,dmi_period)

    # 指定された期間にフィルタリング
    df = df_full.loc[start_date:end_date]

    # チャートを表示
    with chart_col:
        add_plots = []
        if show_ma and ma_period:
            add_plots.append(mpf.make_addplot(df[f'MA_{ma_period}'], color='blue', label=f'MA_{ma_period}'))
        # if show_rsi:
        #     add_plots.append(mpf.make_addplot(df['RSI'], panel=1, color='orange', ylabel='RSI'))
        if show_vol:
            # ボリュームデータを追加
            add_plots.append(mpf.make_addplot(df['Volume'], type="bar",panel=2, color='gray', ylabel='Volume'))
        # if show_cloud:
        #     add_plots.append(mkplots(df,plots['cloud'],title='cloud'))
        if show_dmi:
            add_plots.append(mkplots(df,plots['dmi'],panel=1,title='dmi'))
        

          # パネルの比率設定
        if show_dmi and show_vol:
            panel_ratios = (3, 1, 1)  # RSIとボリュームが表示される場合、ボリュームが一番下
        elif show_dmi or show_vol:
            panel_ratios = (3, 1)  # RSIのみ表示する場合
        else:
            panel_ratios = (1,)  # 何も表示しない場合

        fig, axlist = mpf.plot(
            df,
            type='candle',
            addplot=add_plots,
            title=f'{symbol}',
            style='nightclouds',
            returnfig=True,
            figscale=1.5,
            figsize=(14, 8),
            panel_ratios=panel_ratios  # パネルの比率設定
        )
        st.pyplot(fig)
