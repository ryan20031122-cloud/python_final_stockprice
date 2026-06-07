

## Tech Stack

- Front-end: Streamlit, Plotly
- Back-end: Python ETL Pipeline
- Database: PostgreSQL / Supabase PostgreSQL
- Automation: GitHub Actions
- Data Sources: Yahoo Finance through `yfinance`, NewsAPI or demo news fallback

## Repository Structure

```text
tech-stock-sentiment-dashboard/
├── app.py
├── requirements.txt
├── executive_summary.md
├── config/
├── data_pipeline/
├── database/
├── pages/
├── utils/
└── .github/workflows/
```

## Setup
"後端資料處理採用 ETL 流程，分為 Extract、Transform、Load 三個階段。

1. Extract：資料擷取

系統會定期擷取兩種類型的資料：

第一類是股價資料，包含主要科技公司，例如 Apple、Microsoft、Nvidia、Google、Tesla 等公司的歷史股價。擷取欄位包含開盤價、最高價、最低價、收盤價、成交量與日期。

第二類是新聞資料，主要蒐集與科技產業、股市、AI、晶片、國際經濟與企業財報相關的新聞標題。新聞資料可用來分析當天市場情緒，並與股價變化做對照。

2. Transform：資料清理與轉換

取得原始資料後，系統會進行資料清理與轉換，包含：

移除重複資料
處理缺失值
統一日期格式
整理股票代碼與公司名稱
計算每日報酬率
計算 7 日與 30 日移動平均
計算短期波動率
分析新聞標題情緒
將新聞情緒分為 positive、neutral、negative

透過這些處理，原本單純的股價資料會被轉換成更有分析價值的金融指標。例如，收盤價只能顯示價格高低，但每日報酬率與波動率可以進一步顯示市場變動幅度與風險程度。

3. Load：資料寫入資料庫

轉換後的資料會寫入雲端 PostgreSQL 資料庫。資料庫主要包含兩類資料表：

stock_prices：儲存股價、成交量、報酬率、移動平均與波動率
news_sentiment：儲存新聞標題、來源、發布時間、情緒分類與情緒分數

透過資料庫儲存，Dashboard 可以直接讀取最新資料，不需要每次開啟網頁時重新爬取，提升系統穩定性與載入速度。"

使用 GitHub Actions 建立自動更新機制。系統會依照設定的排程自動執行 ETL pipeline，定期重新擷取股價與新聞資料，並更新資料庫。

此設計可以讓資料在雲端自動刷新，不需要使用本機電腦執行程式，也符合本專案不能使用 localhost 作為展示網址的要求。

Dashboard 也會顯示最後更新時間，讓使用者知道目前畫面中的資料是否為近期資料。


本專案的特色不只是顯示股價，而是將股價變化與新聞事件進行對照。分析流程如下：

先觀察股價是否出現明顯上漲或下跌。
再查看同一天或前後幾天的新聞情緒變化。
接著檢查是否有重大國際事件或產業新聞。
最後判斷股價波動可能受到哪些因素影響。

可能影響科技股的事件包含：

美國聯準會利率決策
通膨數據公布
科技公司財報
AI 產業發展消息
半導體供應鏈變化
國際貿易限制
地緣政治衝突
大型科技公司產品發表會
企業裁員、併購或投資消息

舉例來說，如果某段時間 Nvidia 股價明顯上升，同時新聞情緒以正向為主，且新聞內容集中在 AI 晶片需求增加，則可以推測市場對 AI 產業成長具有較高期待。相反地，如果 Tesla 股價下跌，且新聞情緒偏負面，可能與財報不如預期、降價競爭或市場需求下降有關。
