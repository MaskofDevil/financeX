
![Logo](https://user-images.githubusercontent.com/66861616/151652382-b8b88b58-3208-4d3e-9285-21ad46f00cf1.png)

# FinanceX - Quote, Buy and Sell Stocks

FinanceX is a minimal and responsive stock trading website that uses IEX Cloud API to quote, buy and sell stocks of various companies.

## Screenshot

![financeX](https://user-images.githubusercontent.com/66861616/150557091-ce16d0e4-bda9-43ba-b3d8-18f4848cbbd8.png)

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
    ├── manage.py
    ├── README.md
    └── requirements.txt
    
## Features

- Fully responsive
- Realtime stock quotes
- Transaction History

## Run Locally
1. Clone this repository and run `pip install -r requirements.txt`
2. Get API KEY from IEX Cloud
3. Create a .env file in the root of the project
4. Add Your API KEY in the .env file `API_KEY={Your_API_KEY}`
5. Finally execute `flask run` command

## Tech Stack

**Client:** HTML, CSS, JavaScript, Jinja

**Server:** Flask, sqlite3

**API:** IEX Cloud

**UI Design:** Figma

## Roadmap:
- Payment gateway integration
- Pagination
- Bugfix

### ⭐ Star this repo
