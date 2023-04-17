from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)


def get_page_count(keyword, index=0):
  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")

  browser = webdriver.Chrome(options=options)

  browser.get(f"https://kr.indeed.com/jobs?q={keyword}&start={index*10}")
  soup = BeautifulSoup(browser.page_source, "html.parser")
  pagination = soup.find('nav', class_='ecydgvn0')
  # if pagination ==None:
  #   return 1
  #왜 pagination이 없는데도None이 아닐까?해서 보니 아무것도 없는 걸로 하나 있었네요?
  pages = pagination.find_all("div", recursive=False)
  count = len(pages)
  if count == 0:
    return 1
  elif count <= 5:
    return 5
  elif count > 5:
    if index != 0:
      return 5
    return_page = 5
    index = 2
    while get_page_count(keyword, index) != 4:
      if index == 9:
        print(f"{keyword} research more than 10 pages!")
        return 10
      index = index + 1
      return_page = return_page + 1
    return return_page
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
        #오늘 다시 실행해보니 잘 가져오던 location 정보를 가져오지 못하기 시작했다. start=90일때 주로 발생, 80일 때 한번 발생...
        #렘이나 cpu를 너무 많이 쓰나? 아니면 제한시간을 초과했나?
        #찾는데 2시간 걸렸나? 한놈이 ""로 감싸져있는데 이건가?
        #확인해보니 얘가 문제 맞는데...왜 어젠 됬던거지? 내가 제대로 확인을 안 했던건가?일단 못 가져오면 None으로 처리해야 겠네..

        job_data = {
          "link": f"https://kr.indeed.com{link}",
          "company": company.string.replace(",", " "),
          "location": location.string,
          "position": title.replace(",", " ")
        }
        results.append(job_data)
    # for result in results:
    #   print(result, "\n///////////\n")
  return results
