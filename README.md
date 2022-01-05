# FinanceX - Quote, Buy and Sell Stocks

#### Description:

FinanceX is a minimal and responsive stock trading website that uses IEX Cloud API to quote, buy and sell stocks of various companies.

##### Project Structure:
    financeX/
    ├── static/
    |   ├── coins.svg
    │   ├── favicon.ico
    │   ├── script.js
    │   └── styles.css
    ├── templates/
    |   ├── change.html
    |   ├── details.html
    |   ├── error.html
    |   ├── history.html
    |   ├── home.html
    |   ├── index.html
    |   ├── layout.html
    |   ├── login.html
    │   └── register.html
    ├── app.py
    ├── financeX.db
    ├── IEX_Cloud.http
    ├── manage.py
    ├── README.md
    └── requirements.txt

##### Getting Started
1. Clone this repository and run `pip install -r requirements.txt`
2. Get API KEY from IEX Cloud
3. Create a .env file in the root of the project
4. Add Your API KEY in the .env file `API_KEY={Your_API_KEY}`
5. Finally execute `flask run` command

##### Built with
* Flask
* sqlite3
* HTML
* CSS
* JavaScript
* Figma (UI design)

##### Future scopes:
1. Payment gateway integration
