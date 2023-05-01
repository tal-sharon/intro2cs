import pickle
import requests
import bs4
import sys
from urllib.parse import urljoin
from typing import Dict, List, Tuple
import copy
from collections import Counter


##############################################################################
# FILE: moogle.py
# LAB: Intro2cs ex6 2021-2022
# WRITER: Tal Sharon, 315813980, talsharon
# DESCRIPTION: a Harry Potter search engine based on page rank algorithm
##############################################################################


def crawl() -> None:
    """
    a function which crawls through a certain website and maps the links between certain pages in it.
    :return: a dictionary mapping each page and it's links to the other pages
    """
    base_url = sys.argv[2]
    index_file = sys.argv[3]
    out_file = sys.argv[4]
    index = open(index_file, "r")
    url_lst = create_url_lst(index)
    traffic_dict = get_traffic_dict(base_url, url_lst)
    with open(out_file, 'wb') as traffic_pkl:
        pickle.dump(traffic_dict, traffic_pkl)


def create_url_lst(lst) -> List:
    """
    creates a list of html pages out of a text file
    :param lst: the text file
    :return: the list of all html pages from the text file
    """
    full_urls = []
    for line in lst:
        full_urls.append(line.strip())
    return full_urls


def get_links(base: str, url: str, lst: List) -> Dict:
    """
    gets all the links from a certain page and put it in a dictionary
    :param base: the base of the url
    :param url: the relative url of the html page
    :param lst: a list of all urls
    :return: a dictionary of linked pages per page
    """
    full_url = urljoin(base, url)
    page_traffic: Dict[str, int] = dict()
    response = requests.get(full_url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")
    linked_page_set, linked_pages_lst = map_links(lst, soup)
    page_traffic = count_links_dict(linked_page_set, linked_pages_lst, page_traffic)
    return page_traffic


def count_links_dict(linked_page_set: set, linked_pages_lst: List, page_traffic: Dict):
    """
    counts how many time a link appears in a certain page
    :param linked_page_set: a set of all the links inside the page (each link appears once)
    :param linked_pages_lst: a list of all links inside the page (a link can appear multiple times)
    :param page_traffic: a dict of all the links inside a page and their count
    :return: updated page_traffic dict
    """
    for link in linked_page_set:
        count = linked_pages_lst.count(link)
        page_traffic[link] = count
    return page_traffic


def map_links(lst: list, soup) -> Tuple[set,list]:
    """
    maps all the links inside a page
    :param lst: the list of all page names relevant for the mapping
    :param soup: the html content of the page
    :return: a set and a list of all the linked pages in the page
    """
    paragraphs = soup.find_all("p")
    linked_pages_lst = []
    for p in paragraphs:
        links = p.find_all("a")
        for link in links:
            target = link.get("href")
            if target in lst:
                linked_pages_lst.append(target)
    linked_page_set = set(linked_pages_lst)
    return linked_page_set, linked_pages_lst


def get_traffic_dict(base: str, lst: list) -> Dict:
    """
    gets the full traffic dictionary which maps every page in the index and
    gets the count of all the links of the index it is linked to
    :param base: the base url
    :param lst: the lst of all html pages
    :return: traffic dictionary
    """
    traffic_dict: Dict[str, Dict[str, int]] = dict()
    for url in lst:
        links = get_links(base, url, lst)
        traffic_dict[url] = links
    return traffic_dict


def page_rank():
    iterations = int(sys.argv[2])
    dict_file = open(sys.argv[3], 'rb')
    dict_file = pickle.load(dict_file)
    out_file = sys.argv[4]
    r: Dict[str, float] = dict()
    new_r: Dict[str, float] = dict()
    sum_dict = sum_page_points(dict_file, new_r, r)
    r = ranking_iteration(dict_file, iterations, new_r, r, sum_dict)
    with open(out_file, 'wb') as rank_pkl:
        pickle.dump(r, rank_pkl)
    return r


def ranking_iteration(dict_file, iterations, new_r, r, sum_dict):
    for iteration in range(iterations):
        for ranked in new_r:
            for pointer in r:
                if ranked in dict_file[pointer]:
                    new_r[ranked] += r[pointer] * dict_file[pointer][ranked] / sum_dict[pointer]
                else:
                    pass
        r = copy.deepcopy(new_r)
        for index in new_r:
            new_r[index] = 0
    return r


def sum_page_points(dict_file, new_r, r):
    sum_dict = dict()
    for index in dict_file:
        r[index] = 1
        new_r[index] = 0
        sum_dict[index] = 0
        for page_points in dict_file[index]:
            sum_dict[index] += dict_file[index][page_points]
    return sum_dict


def words_dict():
    base_url = sys.argv[2]
    index_file = open(sys.argv[3], "r")
    out_file = sys.argv[4]
    url_lst = create_url_lst(index_file)
    pages_words = pages_word_count(base_url, url_lst)
    word_dict = initiate_word_dict(pages_words)
    word_dict = fill_word_dict(pages_words, word_dict)
    with open(out_file, 'wb') as words_pkl:
        pickle.dump(word_dict, words_pkl)
    return word_dict


def fill_word_dict(pages_words, word_dict):
    for word in word_dict:
        word_in_pages = dict()
        for page in pages_words:
            if pages_words[page][word] > 0:
                word_in_pages[page] = pages_words[page][word]
        word_dict[word] = word_in_pages
    return word_dict


def initiate_word_dict(pages_words):
    word_dict: Dict[str, Dict[str, int]] = dict()
    for page in pages_words:
        for word in pages_words[page]:
            word_dict[word] = {}
    return word_dict


def pages_word_count(base_url, url_lst):
    pages_words = dict()
    for url in url_lst:
        full_url = urljoin(base_url, url)
        response = requests.get(full_url)
        html = response.text
        soup = bs4.BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all("p")
        pages_words = word_counter(pages_words, paragraphs, url)
    return pages_words


def word_counter(pages_words, paragraphs, url):
    cnt = Counter()
    pages_words[url] = {}
    for paragraph in paragraphs:
        content = paragraph.text
        content = content.split()
        for i in range(len(content)):
            content[i] = content[i].strip(" ")
            content[i] = content[i].strip("\t")
            content[i] = content[i].strip("\n")
        for word in content:
            cnt[word] += 1
    pages_words[url] = cnt
    return pages_words


def search():
    max_results, query, ranking_dict_file, words_dict_file = initiate_search()
    query_words_lst = make_query_lst(query, words_dict_file)
    if len(query_words_lst) == 0:
        return None
    relevant_pages_rank, reversed_rank_dict = relevant_pages(query_words_lst, ranking_dict_file, words_dict_file)
    relevant_pages_rank = sorted(relevant_pages_rank)
    relevant_pages_rank = relevant_pages_rank[-1:(-1 * max_results) - 1:-1]
    max_results_lst = []
    for page in range(max_results):
        max_results_lst.append(reversed_rank_dict[relevant_pages_rank[page]])
    query_word_rank = rank_by_word(query_words_lst, max_results_lst, words_dict_file)
    final_rank_dict = get_search_results(max_results, query_word_rank, ranking_dict_file, max_results_lst)
    return final_rank_dict


def initiate_search():
    query = sys.argv[2]
    ranking_dict_file = open(sys.argv[3], 'rb')
    ranking_dict_file = pickle.load(ranking_dict_file)
    words_dict_file = open(sys.argv[4], 'rb')
    words_dict_file = pickle.load(words_dict_file)
    max_results = int(sys.argv[5])
    return max_results, query, ranking_dict_file, words_dict_file


def get_search_results(max_results, query_word_rank, ranking_dict_file, relevant_pages_lst):
    final_rank_dict = dict()
    final_rank_dict = make_final_rank(final_rank_dict, query_word_rank, ranking_dict_file, relevant_pages_lst)
    rank_lst = sort_final_rank(final_rank_dict)
    for index, rank in enumerate(rank_lst):
        if index < max_results:
            print(final_rank_dict[rank], rank)
        else:
            break
    return final_rank_dict


def sort_final_rank(final_rank_dict):
    rank_lst = []
    for rank in final_rank_dict:
        rank_lst.append(rank)
    rank_lst = sorted(rank_lst)
    rank_lst = rank_lst[::-1]
    return rank_lst


def make_final_rank(final_rank_dict, query_word_rank, ranking_dict_file, relevant_pages_lst):
    for page in relevant_pages_lst:
        final_rank = ranking_dict_file[page] * query_word_rank[page]
        final_rank_dict[final_rank] = page
    return final_rank_dict


def rank_by_word(query_words_lst, relevant_pages_lst, words_dict_file):
    query_word_rank: Dict[str, List[int]] = dict()
    for page in relevant_pages_lst:
        word_appear_rank = "Not ranked"
        word_appear_temp = 0
        for word in query_words_lst:
            word_appear_temp = words_dict_file[word][page]
            if type(word_appear_rank) == str:
                word_appear_rank = word_appear_temp
            elif word_appear_temp < word_appear_rank:
                word_appear_rank = word_appear_temp
            else:
                pass
        query_word_rank[page] = word_appear_rank
    return query_word_rank


def relevant_pages(query_words_lst, ranking_dict_file, words_dict_file):
    relevant_pages_rank = []
    reversed_rank_dict = dict()
    for page in ranking_dict_file:
        has_all_words = is_query_in_page(page, query_words_lst, words_dict_file)
        if has_all_words:
            reversed_rank_dict[ranking_dict_file[page]] = page
            relevant_pages_rank.append(ranking_dict_file[page])
    return relevant_pages_rank, reversed_rank_dict


def is_query_in_page(page, query_words_lst, words_dict_file):
    has_all_words = True
    for word in query_words_lst:
        if page not in words_dict_file[word]:
            has_all_words = False
            break
    return has_all_words


def make_query_lst(query, words_dict_file):
    query_lst = query.split()
    query_words_lst = []
    for word in query_lst:
        if word in words_dict_file:
            query_words_lst.append(word)
    return query_words_lst


def main():
    if sys.argv[1] == "crawl":
        crawl()
    elif sys.argv[1] == "page_rank":
        page_rank()
    elif sys.argv[1] == "words_dict":
        words_dict()
    elif sys.argv[1] == "search":
        search()
    else:
        pass


if __name__ == '__main__':
    main()
