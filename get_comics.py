from bs4 import BeautifulSoup
import requests
from datetime import date
from datetime import timedelta
import sqlite3
from pathlib import Path

DB_PATH = ''.join((Path(__file__).parent.resolve(True).as_uri(), '/comics.db'))

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

def save_to_db(comic_data,con):
    try:
        with con:
            con.execute('insert or replace into dilbert values (?,?)',comic_data)
            print(f'Saved for {comic_data[0]}.')
    except Exception as e:
        raise e

        
def fetch_comic(comic_date:str):
    try:
        print(f'Fetching comic data for {comic_date}...',end='')
        header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}

        req = requests.get(f'https://dilbert.com/strip/{comic_date}',headers=header)
        bs = BeautifulSoup(req.text,'html5lib')
        
        tag = bs.find('img',attrs={'class':'img-comic'})
        comic_url = tag['src']

        # comic_blob = requests.get(comic_url).content
        comic_data = (comic_date,comic_url)
        return comic_data
    except Exception as e:
        raise e


def update_comics(con):
    msg = ''
    try:
        row = con.execute('select max(date) from dilbert').fetchone()
        dt0 = date.fromisoformat(row[0]) + timedelta(1)
    except Exception as e:
        msg += e
        msg += '\n'
        dt0 = date.fromisoformat('1989-04-16')
        msg += 'Unable to get the latest date for comics in the DB, starting from the beginning (1989-04-16).\n'
    
    dt = date.today()
    msg = f'\nFetching from {dt0}.\n'
    
    while dt0 <= dt:
        try:
            comic_data = fetch_comic(dt0)
            save_to_db(comic_data,con)
            dt0 = dt0 + timedelta(1)
        except Exception as e:
            msg += '\n'
            msg += e
    
    msg += f'\nFetched till {dt0}\n'
    msg = msg + '\nSync complete.\n'
    return msg

def get_dates(year:str,month:str)->list:
    dates = []
    with con:
        cur.execute('select date from dilbert where date like (?) order by date;',(f'{year}-{month}-%',))
        for r in cur:
            dates.append(r[0])
    return dates


def get_months(year:str)->list:
    months = []
    with con:
        cur.execute('select distinct strftime("%m",date) as Month from dilbert where date like (?) order by Month;',(f'{year}-%',))
        for r in cur:
            months.append(r[0])
    return months


def get_years()->list:
    years = []
    with con:
        cur.execute('select distinct strftime("%Y",date) as YEAR from dilbert order by YEAR;')
        for r in cur:
            years.append(r[0])
    return years


def get_bookmarks()-> list:
    bookmarks = []
    with con:
        cur.execute('select date from bookmarks;')
        for r in cur:
            bookmarks.append(r[0])
    return bookmarks


def get_link(date:str) -> str:
    link = ''
    with con:
        cur.execute('select url from dilbert where date = ?',(date,))
        for r in cur:
            link = str(r[0])
    return link


def get_picture(url:str):
    comic_blob = requests.get(url).content
    return comic_blob


def main():
    try:
        update_comics(con)
        # print(get_link('2014-08-14'))
        # print(get_picture('https://assets.amuniversal.com/b8d55ea0f33101318277005056a9545d'))
        con.close()
    except Exception as e:
        print(type(e))
        print(e)
    except KeyboardInterrupt:
        print('\n\nUgh! Interrupted by user...\n\n')
    finally:    
        con.close
    
    
if __name__ == '__main__':
    main()
