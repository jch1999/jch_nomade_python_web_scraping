from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from extractors.gameJob import extract_gameJobs_jobs

keyword=input("What do you want to search for?")

indeed=extract_indeed_jobs(keyword)
wwr=extract_wwr_jobs(keyword)
gameJob=extract_gameJobs_jobs(keyword)

jobs=indeed+wwr+gameJob

file=open(f"{keyword}.csv","w",encoding="utf-8-sig")

file.write("Position,Company,Location,URL\n")

for job in jobs:
  file.write(f"{job['position']},{job['company']},{job['location']},{job['link']}\n")
file.close()

jobs=extract_gameJobs_jobs(keyword)
print(jobs)
