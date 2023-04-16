from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)


def extract_gameJobs_jobs(keyword):
  base_url = "https://www.gamejob.co.kr/Recruit/joblist?menucode=searchtot&searchtype=all&searchstring="
  final_url = f"{base_url}{keyword}"
  browser.get(final_url)
  soup = BeautifulSoup(browser.page_source, "html.parser")

  result = []

  job_list = soup.find("ul", class_="list cf")
  jobs = job_list.find_all('li', recursive=False)  #혹시 모르니 recursive는 False로
  jobs.pop(-1)
  for job in jobs:
    company = job.find("strong").string.replace(",", " ")
    description = job.find("div", class_="description")
    anchor = description.find('a')
    link = anchor['href']
    # location=anchor['onclick'].find('IsNullOrWhiteSpace')
    position = anchor.text.replace(",", " ")

    job_data = {
      "link": f"https://www.gamejob.co.kr{link}",
      "company": company,
      "location": None,
      "position": position
    }
    result.append(job_data)

  company_name = soup.find_all('div', class_='company noLogo')
  company_info = soup.find_all('div', class_='tit')
  for i in range(len(company_name)):
    company = company_name[i].find('strong').string.replace(",", " ")
    print(company)
    link = company_info[i].find('a')['href']
    position = company_info[i].find('a').find('strong').string.replace(
      ",", " ")
    info = company_info[i].find('p', class_='info').find_all('span')
    location = info[2].string.replace(",", " ")
    job_data = {
      "link": f"https://www.gamejob.co.kr{link}",
      "company": company,
      "location": location,
      "position": position
    }
    result.append(job_data)
  return result
