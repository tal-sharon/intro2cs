import pickle
import requests
import bs4
import sys
from urllib.parse import urljoin
from typing import Dict, List, Tuple, Union, Any
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
    return None


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


def map_links(lst: list, soup) -> Tuple[set, list]:
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


def page_rank() -> None:
    """
    ranks the pages popularity by number of links leading to the page from other pages
    :return:
    """
    dict_file, iterations, new_r, out_file, r = set_page_rank()
    sum_dict = sum_page_points(dict_file, new_r, r)
    r = ranking_iteration(dict_file, iterations, new_r, r, sum_dict)
    with open(out_file, 'wb') as rank_pkl:
        pickle.dump(r, rank_pkl)
    return None


def set_page_rank():
    """
    sets all the needed objects for the page_rank function
    :return: the needed parameters
    """
    iterations = int(sys.argv[2])
    dict_file = open(sys.argv[3], 'rb')
    dict_file = pickle.load(dict_file)
    out_file = sys.argv[4]
    r: Dict[str, float] = dict()
    new_r: Dict[str, float] = dict()
    return dict_file, iterations, new_r, out_file, r


def ranking_iteration(dict_file: dict, iterations: int, new_r: dict, r: dict, sum_dict: dict) -> dict:
    """

    :param dict_file: the original dict file of all the links from a page to another page
    :param iterations: the number of iterations for the ranking process
    :param new_r: a dictionary of the new and temp ranking
    :param r: a dictionary of the actual ranking
    :param sum_dict: a dictionary which sums the links between the pages in points method
    :return: the updated ranking dictionary
    """
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


def sum_page_points(dict_file: dict, new_r: dict, r: dict) -> dict:
    """
    gets the sum of links each page gets from other pages
    :param dict_file: the original dict file of all the links from a page to another page
    :param new_r: a dictionary of the new and temp ranking
    :param r: a dictionary of the actual ranking
    :return: the sum of links per page of all given pages
    """
    sum_dict: Dict[str, float] = dict()
    for index in dict_file:
        r[index] = 1
        new_r[index] = 0
        sum_dict[index] = 0
        for page_points in dict_file[index]:
            sum_dict[index] += dict_file[index][page_points]
    return sum_dict


def words_dict() -> None:
    """
    a function which creates a dictionary of all words on the webpages given and
    counts how many time each word appeared on each page
    :return: None
    """
    base_url = sys.argv[2]
    index_file = open(sys.argv[3], "r")
    out_file = sys.argv[4]
    url_lst = create_url_lst(index_file)
    pages_words = pages_word_count(base_url, url_lst)
    word_dict = initiate_word_dict(pages_words)
    word_dict = fill_word_dict(pages_words, word_dict)
    with open(out_file, 'wb') as words_pkl:
        pickle.dump(word_dict, words_pkl)


def fill_word_dict(pages_words: dict, word_dict: dict) -> dict:
    """
    reverses page_words dictionary to get a dictionary of all words from all the website and
    than count of many time each words appears in each page
    :param pages_words: a dictionary of all pages and the count of every word in the page
    :param word_dict: an empty dictionary of all the words in the site and the count of every word
            in each page of the index
    :return: a full word_dict
    """
    for word in word_dict:
        word_in_pages: Dict[str, int] = dict()
        for page in pages_words:
            if pages_words[page][word] > 0:
                word_in_pages[page] = pages_words[page][word]
        word_dict[word] = word_in_pages
    return word_dict


def initiate_word_dict(pages_words: dict) -> dict:
    """
    creates a new dictionary to reverse page_words dictionary to get a dictionary of all words from all the website and
    than count of many time each words appears in each page
    :param pages_words: a dictionary of all pages and the count of every word in the page
    :return: an empty dictionary of all the words in the site and the count of every word in each page of the index
    """
    word_dict: Dict[str, Dict[str, int]] = dict()
    for page in pages_words:
        for word in pages_words[page]:
            word_dict[word] = {}
    return word_dict


def pages_word_count(base_url: str, url_lst: list) -> dict:
    """
    the function count all the words in each page and records the data in a dictionary
    :param base_url: the base url of the site we are search in
    :param url_lst: the url list of the pages on the site
    :return: pages_words: a dictionary of all pages and the count of every word in the page
    """
    pages_words: Dict[str, Dict[str, int]] = dict()
    for url in url_lst:
        full_url = urljoin(base_url, url)
        response = requests.get(full_url)
        html = response.text
        soup = bs4.BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all("p")
        pages_words = word_counter(pages_words, paragraphs, url)
    return pages_words


def word_counter(pages_words: dict, paragraphs: list, url: str) -> dict:
    """
    counts how many times each word from the websites word dictionary appears in each page
    :param pages_words: a dictionary of all pages and the count of every word in the page
    :param paragraphs: the paragraphs of the html page
    :param url: the url of the html page
    :return: updated dictionary - page_words
    """
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


def search() -> None:
    """
    the function conducting a search of a user's query inside dictionaries based on webpages in a certain website
    and printing the search results
    :return: None
    """
    max_results, query, ranking_dict_file, words_dict_file = initiate_search()
    query_words_lst = make_query_lst(query, words_dict_file)
    if len(query_words_lst) == 0:
        return None
    max_pages_rank, max_pages_names = \
        relevant_pages(query_words_lst, ranking_dict_file, words_dict_file, max_results)
    query_word_rank = rank_by_word(query_words_lst, max_pages_names, words_dict_file)
    get_search_results(query_word_rank, ranking_dict_file, max_pages_names)
    return None


def initiate_search() -> Tuple[int, str, dict, dict]:
    """
    sets all the needed object and arguments for the search function
    :return: all the needed arguments, max_results length, user's query, ranking_dict_file, words_dict_file
    """
    query = sys.argv[2]
    ranking_dict_file = open(sys.argv[3], 'rb')
    ranking_dict_file = pickle.load(ranking_dict_file)
    words_dict_file = open(sys.argv[4], 'rb')
    words_dict_file = pickle.load(words_dict_file)
    max_results = int(sys.argv[5])
    return max_results, query, ranking_dict_file, words_dict_file


def get_search_results(query_word_rank: dict, ranking_dict_file: dict, relevant_pages_lst: list) -> None:
    """
    prints the final search results
    :param query_word_rank: a dictionary with the rank by word appearances
    :param ranking_dict_file: a dictionary with the rank by links 'popularity'
    :param relevant_pages_lst: a list of the relevant pages for the search results
    :return: a dictionary with the final rank sorted
    """
    final_rank_dict: Dict[str, int] = dict()
    final_rank_dict = make_final_rank(final_rank_dict, query_word_rank, ranking_dict_file, relevant_pages_lst)
    rank_lst = sorted(final_rank_dict.values())
    rank_lst = rank_lst[::-1]
    print_results(final_rank_dict, rank_lst, relevant_pages_lst)


def print_results(final_rank_dict: dict, rank_lst: list, relevant_pages_lst: list) -> None:
    """
    prints the final search results by rank from higher to lower
    :param final_rank_dict: a dictionary of the final rank
    :param rank_lst: the final search result list of ranks sorted
    :param relevant_pages_lst: the final search result list of page names not sorted
    :return:
    """
    printed = []
    for index, rank in enumerate(rank_lst):
        for page in relevant_pages_lst:
            if page in printed:
                pass
            elif final_rank_dict[page] == rank:
                print(page, rank)
                printed.append(page)
                break
            else:
                pass


def sort_final_rank(final_rank_dict: dict) -> list:
    """
    sorts the final rank from high to low
    :param final_rank_dict: a dictionary with the final ranks of the search results
    :return: a list of the final rank
    """
    rank_lst = []
    for rank in final_rank_dict:
        rank_lst.append(rank)
    rank_lst = sorted(rank_lst)
    rank_lst = rank_lst[::-1]
    return rank_lst


def make_final_rank(final_rank_dict: dict, query_word_rank: dict, ranking_dict_file: dict, relevant_pages_lst: list) \
        -> dict:
    """
    calculation of the final rank for the search results
    :param final_rank_dict: a dictionary of the final rank of the search results
    :param query_word_rank: a dictionary with the rank by word appearances
    :param ranking_dict_file: a dictionary with the rank by links 'popularity'
    :param relevant_pages_lst: a list of the relevant pages for the search results
    :return: an updated dictionary of the final ranking of the search results
    """
    for page in relevant_pages_lst:
        final_rank = ranking_dict_file[page] * query_word_rank[page]
        final_rank_dict[page] = final_rank
    return final_rank_dict


def rank_by_word(query_words_lst: list, relevant_pages_lst: list, words_dict_file: dict) -> dict:
    """
    get the minimal number of appearances of the words from the query in the page
    :param query_words_lst: thw words from the query
    :param relevant_pages_lst: the pages with the words from the query which are relevant for the search results
    :param words_dict_file: a dictionary with all the words from the webpages
    :return: a rank based on the number of times the words from the query appears inside the pages
    """
    query_word_rank: Dict[str, Any | int] = dict()
    for page in relevant_pages_lst:
        word_appear_rank = "Not ranked"
        for word in query_words_lst:
            word_appear_rank = get_ranked_word(page, word, word_appear_rank, words_dict_file)
        query_word_rank[page] = word_appear_rank
    return query_word_rank


def get_ranked_word(page: str, word: str, word_appear_rank: Union[str, int], words_dict_file: dict) -> int:
    """
    gets the minimal number a word from the query appeared in a certain page
    :param page: the page being checked
    :param word: the word being ranked
    :param word_appear_rank: the current minimal rank
    :param words_dict_file: a dictionary with all the words from the site and count of words in each page
    :return:
    """
    word_appear_temp = words_dict_file[word][page]
    if type(word_appear_rank) == str:
        word_appear_rank = word_appear_temp
    elif word_appear_temp < word_appear_rank:
        word_appear_rank = word_appear_temp
    else:
        pass
    return word_appear_rank


def relevant_pages(query_words_lst: list, ranking_dict_file: dict, words_dict_file: dict, max_results: int) \
        -> Tuple[list, list]:
    """
    get the relevant pages from all the webpages given, pages which has all the query words
    :param query_words_lst: a list of all the word from the user's query
    :param ranking_dict_file: a dictionary that ranks all the pages by popularity
    :param words_dict_file: a dictionary of all the words in the webpages
    :param max_results: the max length of search results
    :return: relevant_pages_rank: a list of the 'popularity' rank of the relevant pages,
                reversed_rank_dict: a dictionary with the rank as key and the name of the page as value.
    """
    relevant_pages_dict, relevant_pages_name = get_relevant_pages(query_words_lst, ranking_dict_file, words_dict_file)
    max_pages_names, max_pages_sorted = max_sort_relevant_pages(max_results, relevant_pages_dict, relevant_pages_name)
    return max_pages_sorted, max_pages_names


def max_sort_relevant_pages(max_results: int, relevant_pages_dict: dict, relevant_pages_name: list) \
        -> Tuple[list, list]:
    """
    creates new lists of the top ranked pages by popularity and max results number given by the user
    :param max_results: the number of max results asked by the user
    :param relevant_pages_dict: a dictionary of the relevant pages (name -> rank
    :param relevant_pages_name: a list of the relevant pages names
    :return: Tuple: max_pages_names - a list of top (max) results by names,
                    max_pages_sorted - a list of top (max) results by rank
    """
    page_sorted = sorted(relevant_pages_dict.values())
    max_pages_sorted = page_sorted[-1:(-1 * max_results) - 1:-1]
    max_pages_names = []
    for page in relevant_pages_name:
        if relevant_pages_dict[page] in max_pages_sorted:
            max_pages_names.append(page)
    return max_pages_names, max_pages_sorted


def get_relevant_pages(query_words_lst: list, ranking_dict_file: dict, words_dict_file: dict) -> Tuple[dict, list]:
    """
    gets the page with all the query words
    :param query_words_lst: a list with all the query words
    :param ranking_dict_file: a dictionary of the 'popularity' rank of the pages
    :param words_dict_file: a dictionary with all the words of the site and count of words in each page
    :return: Tuple: relevant_pages_dict - a dictionary of the relevant pages (name -> rank,
                    relevant_pages_name - a list of the relevant pages names
    """
    relevant_pages_name = []
    relevant_pages_dict: Dict[str, int] = dict()
    for page in ranking_dict_file:
        has_all_words = is_query_in_page(page, query_words_lst, words_dict_file)
        if has_all_words:
            relevant_pages_name.append(page)
            relevant_pages_dict[page] = ranking_dict_file[page]
    return relevant_pages_dict, relevant_pages_name


def is_query_in_page(page: str, query_words_lst: list, words_dict_file: dict) -> bool:
    """
    checks if all the words from the query are inside a certain webpage
    :param page: the webpage being checked
    :param query_words_lst: a list of words from the query
    :param words_dict_file: a dictionary mapping all the words in all webpages given
    :return: bool = True: if the page ha all words from th query, False: if not
    """
    has_all_words = True
    for word in query_words_lst:
        if page not in words_dict_file[word]:
            has_all_words = False
            return has_all_words
    return has_all_words


def make_query_lst(query: str, words_dict_file: dict) -> list:
    """
    makes a list with query words that are in the dictionary
    :param query: the query given by the user
    :param words_dict_file: the dictionary with all the words from the webpages
    :return: the list of thw words from the query which are in the dictionary
    """
    query_lst = query.split()
    query_words_lst = []
    for word in query_lst:
        if word in words_dict_file:
            query_words_lst.append(word)
    return query_words_lst


def main() -> None:
    """
    the main function, runs the correct function according to the command given
    :return: None
    """
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
