# stock_linebot

This tool is a python-based TW stock data collection and calculation tool. 
Available functions are as follows:
- List Top 10 Price-to-Earning Ratio(PER) the day before
- List Top 10 trading volume the day before
- List Top 30 (EPS*15*4 - closing price)
- List Top 30 (five-day average - closing price)
- List Top 15 (three-day average - six-day average)
- List Top 10 (monthly average - closing price)
- Specified stock analysis

### Prerequisite

- python3
```shell
line-bot-sdk==2.0.1
requests==2.22.0
BeautifulSoup4==4.8.2
pandas==1.2.5
twstock==1.3.1
```

### How to use

Deploy source to Heroku and execute on Line.

or

Execute based on the command line:
```
Usage:
    python3 app.py
```

