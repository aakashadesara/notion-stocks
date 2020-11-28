## 📈 Notion x Stocks
In the past, I've used Spreadsheets + Jupyter notebooks to analyze stock data (and I probably will continue to do so) but I thought it'd be cool to make an auto-population Notion page of stock information. 

If you think this is interesting, check out my other Notion hacks using [Notion-Py](https://github.com/jamalex/notion-py) like _[Notion x Sheets](https://github.com/aakashadesara/notion-google-sheets-sync)_ and _[Notion x News](https://github.com/aakashadesara/notion-news)_.

![Notion Stocks Demo Screenshot](/demo.png)

### How to Use Notion x Stocks
1. Get your Notion V2 Token by visiting your Notion page from a browser and copy the token_v2 Cookie. Replace `<YOUR_NOTION_TOKEN_V2>` with the cookie.

2. Make a new empty Notion page and replace `<YOUR_NOTION_PAGE_LINK>` in `stocks.py` with the link of the new page. 

3. And you should be good to go! Now just run `python stocks.py` and your news will update when the script starts, and then it will continue to update every 6 hours.

### Potential future changes
- [ ] Batch delete all rows before re-populating stock data
- [ ] Mutli-thread Stock update calls (once batch re-population is available)
- [ ] Parse / display sector using a `multi_select` instead of regular text

If you want to help, feel free to fork + make a pull request. Contact me on Twitter [@aakashadesara](https://twitter.com/aakashadesara) before you work on something big so we do not have multiple people working on the same changes.

### Thanks
Special thanks to the folks working on the [Notion Python API](https://github.com/jamalex/notion-py) and to the people who made the Python yfinance library.
