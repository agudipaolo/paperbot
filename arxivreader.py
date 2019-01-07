from datetime import datetime, timedelta
import time
import numpy as np
from bs4 import BeautifulSoup as bs
import urllib.request
import shelve

all_arxiv_section = ['astro-ph', 'cond-mat', 'gr-qc', 'hep-ex', 'hep-lat', 'hep-ph', 'hep-th',
                     'math-ph', 'nlin', 'nucl-ex', 'nucl-th', 'physics', 'quant-ph',
                     'math', 'CoRR', 'q-bio', 'q-fin', 'stat', 'eess', 'econ']


def get_arxiv_paper(date, days_back, section):
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    papers = []
    if date_obj == datetime.today().date():
        papers = get_paper_from_arxiv(date, 1, section)
        print("")
        days_back -= 1
        date_obj = date_obj + timedelta(days=-1)
    if days_back:
        with shelve.open("arxiv.papers") as arxivDB:
            for days in range(days_back):
                date_iter = date_obj + timedelta(days=-days)
                date_str = date_iter.strftime("%Y-%m-%d")
                if date_str in arxivDB and section in arxivDB[date_str]:
                    papers += arxivDB[date_str][section]
                else:
                    paper_iter = get_paper_from_arxiv(date_str, 1, section)
                    print(" saving!")
                    if date_str not in arxivDB:
                        arxivDB[date_str] = {section:paper_iter}
                    else:
                        dict_day = arxivDB[date_str]
                        dict_day[section] = paper_iter
                        arxivDB[date_str] = dict_day
                    arxivDB[date_str][section] = paper_iter
                    papers += paper_iter
    return papers


def get_paper_from_arxiv(date, days_back, section):
    source = urllib.request.urlopen('https://scirate.com/arxiv/' + section +
                                    '?date=%s&page=1&range=%d' % (date, days_back)).read()
    soup = bs(source, "html.parser")
    pages_scirate = {}
    pages_scirate['pages'] = []
    div_pages = soup.find_all("div", class_="pagination")
    for div_page in div_pages:
        a_href_pages = div_page.find_all('a')
        for a_href_page in a_href_pages:
            pages_scirate['pages'].append(a_href_page.contents[0])
    if (len(pages_scirate['pages']) > 1):
        max_page = int(pages_scirate['pages'][-2])
    else:
        max_page = 1
    print("arxiv " + section + "," + date + " :", max_page, "pages", end='')
    urls_list = []
    papers = []
    for p in range(1,max_page+1):
        url = 'https://scirate.com/arxiv/' + section + '?date=' + str(date) + \
              '&page=' + str(p) + '&range=' + str(days_back)
        source = urllib.request.urlopen(url).read()
        soup = bs(source, 'html.parser')
        listing_page = soup.find_all("div", class_="paperlist")
        for paper_soup in soup.find_all("li", class_="paper"):
            paper  = {}
            paper['title'] = str(paper_soup.find('div', class_="title").contents[0].contents[0])
            paper['authors'] = [str(author.contents[0]).strip(", ")
                                for author in paper_soup.find('div', class_="authors").contents
                                if str(author).strip()]
            paper['date'] = str(paper_soup.find('div', class_="uid").contents[0]).strip()
            paper['abstract'] = str(paper_soup.find('div', class_="abstract").contents[0])
            paper['arXivID'] = str(paper_soup.find('div', class_="uid").contents[-1]).strip()[6:]
            paper['datestr'] = datetime.strptime(paper['date'],
                                                 "%b %d %Y").strftime("%Y-%m-%d")
            papers.append(paper)
    return papers


def build_post_arxiv(papers_list, keywords, authors):
    prefered_keywords = np.load('prefered_keywords.npy')
    papers_post_list = []
    for paper in papers_list:
        included = 0
        for kw in keywords:
            if (kw.casefold() in paper['title'].casefold() or
                kw.casefold() in paper['abstract'].casefold()):
                papers_post_list.append([paper, "", ""])
                included = 1
                break
        for kw in authors:
            if included:
                break
            if (kw.casefold() in " ".join(paper['authors']).casefold()):
                papers_post_list.append([paper, "", ""])
                break

    for paper in papers_post_list:
        for before, kw, after in prefered_keywords:
            if (kw.casefold() in paper[0]['title'].casefold() or
                kw.casefold() in paper[0]['abstract'].casefold() or
                kw.casefold() in " ".join(paper[0]['authors']).casefold()):
                    paper[1] = before
                    paper[2] = after
                    break

    post_list = []
    for paper, before, after in papers_post_list:
        post_list.append(before + '*'+paper['title']+'*' + after + '\n' +
                         ", ".join(paper['authors']) + '\n' +
                         "https://scirate.com/arxiv/" + paper['arXivID'] + ' | ' +
                         "https://arxiv.org/abs/" + paper['arXivID'] + '\n')

    # removing duplicates
    post_list_aux = post_list
    post_list = []
    for item in post_list_aux:
        if item not in post_list:
            post_list.append(item)
    return post_list


def print_arxiv_paper(slack, date, N, sections, keywords=[], authors=[]):
    if not keywords:
        keywords = np.load('keywords.npy')
    if not authors:
        authors = np.load('keywords_authors.npy')
    papers = []
    for section in sections:
        papers += get_arxiv_paper(date, N, section)
    response = build_post_arxiv(papers, keywords, authors)
    print("N. response", len(response))
    if (len(response) == 0):
        slack.post('[no matches]')
    for rep in response:
        slack.post(rep)


def get_author_list_arxiv(year, keywords, sections):
    new_authors = []
    #try:
    for _ in [1]:
        year = year.strip()
        if year == time.strftime("%Y"):
            date_end = time.strftime("%Y-%m-%d")
        else:
            date_end = year + "-12-31"
        print(date_end)
        date_start = year + "-01-01"
        end_date = datetime.strptime(date_end, "%Y-%m-%d").date()
        begin_date = datetime.strptime(date_start, "%Y-%m-%d").date()
        N = (end_date - begin_date).days + 1
        print(N, sections)
        papers = []
        for section in sections:
            papers += get_arxiv_paper(date_end, N, section)

        print ()
        for paper in papers:
            for kw in keywords:
                if (kw.casefold() in paper['title'].casefold() or
                        kw.casefold() in paper['abstract'].casefold()):
                    new_authors += paper['authors']

    #except:
    #    pass

    return new_authors
