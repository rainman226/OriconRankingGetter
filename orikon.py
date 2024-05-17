import datetime
import requests
import argparse
import csv
import json

from bs4 import BeautifulSoup


# type(ja,jsなど)とyyyyとmmからランキングページリストを取得
# Get ranking page list from type (ja, js, etc.), yyyy and mm
def getPageList(type,year,month):
	url = "https://www.oricon.co.jp/rank/RankNavigationCalendar.php?kbn="+type+\
		"&type=w&date="+str(year)+"-"+str(month)+"-1&url_date="+str(year)+"-"+str(month)+"-1&trigger=change"
#	print(url+"\n")
	html = requests.get(url).content
	soup = BeautifulSoup(html, "html.parser")
	options = soup.find("div",class_="block-rank-search-box")
	options = options.find("div",class_="wrap-select-week")
	options = options.find("select").find_all("option")
	result=[]
	for option in options:
		result.append(option.get("value"))
#	print(result)
	return result

#指定URLのランキングページから、max_pageで指定したページ数分取得
#Get the number of pages specified by max_page from the ranking page of the specified URL.
def getRanking(url, week, max_page=1):
    result = []
    for i in range(max_page):
        result.extend(parsePage(url + "p/" + str(i + 1) + "/"))
    return week, result

#指定URLのページをパース
#Parsing pages with specified URLs
def parsePage(url):
    result = []
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.find_all("section")
    for section in sections:
        data = section.find("div", class_="inner")
        if data.find("a") is not None:
            data = data.find("a")
            link = "https://www.oricon.co.jp" + data.get("href")
        else:
            link = ""
        title = data.find("div").find("h2").text.strip()
        artist = data.find("div").find("p").text.strip()
        date = data.find("div").find("ul").find("li").text.strip()
        date = date[date.find("2"):date.find("2") + 10]
        result.append({
            'artist': artist,
            'title': title,
            'date': date,
            'url': link
        })
    return result


def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['Artist', 'Title', 'Date', 'URL'])  # No 'Week' in the headers
        for week, entries in data.items():
            # Optional: you can add a comment row to separate weeks
            writer.writerow([f'Week: {week}', '', '', ''])  # A row to indicate the start of a new week
            for entry in entries:
                writer.writerow([entry['artist'], entry['title'], entry['date'], entry['url']])
				


def write_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)



def output_results(data, filename, format):
    if format == 'csv':
        write_to_csv(data, filename)
    elif format == 'json':
        write_to_json(data, filename)
    else:
        print(data)

def main():
    parser = argparse.ArgumentParser(description='Tool to fetch weekly single and album rankings from Oricon.')
    parser.add_argument('-t', '--type', type=str, help='Ranking type (ja, js, etc.)', required=True)
    parser.add_argument('-y', '--year', type=int, help='Year of the ranking', required=True)
    parser.add_argument('-m', '--month', type=int, help='Month of the ranking', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output file name, including path if needed')
    parser.add_argument('-f', '--format', type=str, choices=['csv', 'json'], help='Output format (csv or json)')

    args = parser.parse_args()

    # Assume argparse setup is already done and args parsed
    pages = getPageList(args.type, args.year, args.month)
    all_results = {}
    for page in pages:
        week, data = getRanking(page, page)  # Assuming 'page' contains a week identifier
        all_results[week] = data

    if args.output and args.format:
        output_results(all_results, args.output, args.format)
    else:
        for week, entries in all_results.items():
            print(f"Week: {week}")
            for entry in entries:
                print(f"{entry['artist']}\t{entry['title']}\t{entry['date']}\t{entry['url']}")

if __name__ == "__main__":
    main()