
# 🧠 Alpaca 策略评分自动交易系统

该项目支持基于多策略（EMA 回调、布林带突破、RSI + MACD）打分，筛选高概率交易信号并自动挂单，含完整可视化面板、策略回测与每日定时挂单系统。

---

## 📁 文件说明

| 文件名                          | 描述 |
|----------------------------------|------|
| `alpaca_strategy_autotrade.py`   | 多策略信号判断 + 自动挂单主面板 |
| `alpaca_strategy_allinone.py`    | 批量评分、多股筛选、定时逻辑入口 |
| `alpaca_strategy_scoring.py`     | 策略评分系统（≥2分可挂单） |
| `alpaca_backtest.py`             | 回测策略组合历史盈亏和胜率 |
| `run_daily_scoring.py`           | 每日评分 + 挂单执行脚本（部署用） |

---

## 🛠 依赖安装

```bash
pip install -r requirements.txt
```

内容：
```
streamlit
yfinance
ta
alpaca-trade-api
pandas
```

---

## 🚀 运行方式

### 1. 可视化策略交易面板（Streamlit）

```bash
streamlit run alpaca_strategy_autotrade.py
```

或运行 allinone 脚本整合页：

```bash
streamlit run alpaca_strategy_allinone.py
```

### 2. 每日自动挂单脚本

定时运行 `run_daily_scoring.py` 可部署在：
- 本地定时任务（crontab / Windows 计划任务）
- GitHub Actions / PythonAnywhere

---

## 🔒 使用前请设置你的 Alpaca API Key：
修改以下字段：

```python
API_KEY = "YOUR_ALPACA_API_KEY"
API_SECRET = "YOUR_ALPACA_SECRET_KEY"
```

---

## 📈 可选：策略评分历史回测

```bash
streamlit run alpaca_backtest.py
```

---

## 🧠 后续建议

- 添加数据库记录历史订单
- 加入 telegram / 邮箱通知模块
- 优化多因子权重评分
