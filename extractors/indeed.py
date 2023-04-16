from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)


def get_page_count(keyword):
  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")

  browser = webdriver.Chrome(options=options)

  browser.get(f"https://kr.indeed.com/jobs?q={keyword}")
  soup = BeautifulSoup(browser.page_source, "html.parser")
  pagination = soup.find('nav', class_='ecydgvn0')
  # if pagination ==None:
  #   return 1
  #왜 pagination이 없는데도None이 아닐까?해서 보니 아무것도 없는 걸로 하나 있었네요?
  pages = pagination.find_all("div", recursive=False)
  count = len(pages)
  if count == 0:
    return 1
  elif count >= 5:
    return 5
  else:
    return count


def extract_indeed_jobs(keyword):
  pages = get_page_count(keyword)
  print("Found", pages, "pages")
  results = []
  for page in range(pages):
    base_url = "https://kr.indeed.com/jobs"
    final_url = f"{base_url}?q={keyword}&start={page*10}"
    print("Requesting", final_url)
    browser.get(final_url)

    soup = BeautifulSoup(browser.page_source, "html.parser")
    job_list = soup.find("ul", class_="jobsearch-ResultsList")
    jobs = job_list.find_all("li", recursive=False)
    # print(len(jobs))

    for job in jobs:
      zone = job.find("div", class_="mosaic-zone")
      if zone == None:
        anchor = job.select_one("h2 a")
        title = anchor['aria-label']
        link = anchor['href']
        company = job.find('span', class_="companyName")
        location = job.find('div', class_='companyLocation')
        job_data = {
          "link": f"https://kr.indeed.com{link}",
          "company": company.string.replace(",", " "),
          "location": location.string.replace(",", " "),
          "position": title.replace(",", " ")
        }
        results.append(job_data)
    # for result in results:
    #   print(result, "\n///////////\n")
  return results
