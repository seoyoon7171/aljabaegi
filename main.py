import os
import csv
import requests
from bs4 import BeautifulSoup
from save import save_to_file
import re
import csv



os.system("clear")
alba_url = "http://www.alba.co.kr"

group_company = {'name': '', 'jobs': []}

company_names=[] #알바천국 타이틀
company_urls =[]  #상세페이지 링크

def save_to_file(group_company):

  file = open(f"{group_company['name']}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["place", "title", "time", "pay", "date"])
  for job in group_company['jobs']:
    writer.writerow(list(job.values()))

def main():
  result= requests.get(f"{alba_url}")
  soup = BeautifulSoup(result.text, "html.parser")
  results = soup.find("div",{"id":"MainSuperBrand"}).find_all("li")
  for rr in results:
    find_company_name(rr)
    find_company_url(rr)    

def find_company_name(rr):
  company= rr.find("span", {"class":"company"})
  if company is None:
    None
  else:
    company_names.append(company.string) 

def find_company_url(rr):
  company_url = rr.find("a", {"class":"goodsBox-info"})
  if company_url is None:
    None
  else:
    company_url=company_url.attrs['href']
    company_urls.append(company_url)

next_n ="&pagesize=50&areacd=&workaddr1=&workaddr2=&jobkind=&jobkindsub=&jobkindmulti=&gendercd=&agelimitcd=&agelimit=0&worktime=&weekdays=&searchterm=&paycd=&paystart=&payend=&workperiodcd=&workstartdt=&workenddt=&workchkyn=&workweekcd=&targetcd=&streetunicd=&streetstationcd=&unicd=&schnm=&schtext=&orderby=freeorder&acceptmethod=&eleccontract=&careercd=%20&lastschoolcd=&welfarecd=&careercdunrelated=&lastschoolcdunrelated=&strAreaMulti=&genderunrelated=&special=&hiretypecd=&totalCount="

def get_last_page():
  
  main()
  for comurl, comname in zip(company_urls, company_names):
    groupgroup(comurl,comname)

def groupgroup(comurl,comname):
  global resultss
  result= requests.get(comurl)
  soup = BeautifulSoup(result.text, "html.parser")
  results= soup.find("body").find("p", {"class":"jobCount"})
  if results is None:
    None
  else:
    resultss=results.get_text()
  i = int(re.findall('\d+', resultss)[0])
  last_page=int((i//50)+1)
  print(last_page,i, comname.replace(" ",""))
  for n in range(1,last_page+1):
    pages(n,comurl, i, comname)
  save_to_file(group_company)
  
  del group_company['jobs']
  group_company['jobs'] =[]

def pages(n, comurl, i, comname):
  url_n= f"{comurl}?page={n}{next_n}{i}"
  result= requests.get(url_n)
  soup = BeautifulSoup(result.text, "html.parser")
  results = soup.find("div", {"id":"NormalInfo"}).find("tbody").find_all("tr", {"class":""})
  results2 = soup.find("div", {"id":"NormalInfo"}).find("tbody").find_all("tr", {"class":"divide"})
  add_to_list(results, comname)
  add_to_list(results2,comname)
  return group_company

def add_to_list(results, comname):
  for rea in results:
    ret(rea, comname)

def ret(rea,comname):
  global aa, bb, cc, dd, ee
  if rea is None:
    None
  else: 
    a= rea.find("td", {"class":"local first"})
    if a is None:
      None
    else:
      aa= a.get_text().replace("\xa0"," ")
    b =rea.find("span", {"class":"company"})
    if b is None:
      None
    else:
      bb=b.get_text()
    c =rea.find("span", {"class":"time"})
    if c is None:
      None
    else:
      cc=c.get_text()
    d =rea.find("td", {"class":"pay"})
    if d is None:
      None
    else:
      dd=d.get_text()
    e =rea.find("td",{"class":"regDate last"})
    if e is None:
      None
    else:
      ee=e.get_text()
      job = {
      'place':str(aa), 
      'title':str(bb), 
      'time':str(cc), 
      'pay':str(dd),
      'date':str(ee)
      }
      group_company['name']= comname

      group_company['jobs'].append(job)


get_last_page()
