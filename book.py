# for scraping books
from bs4 import BeautifulSoup as bs
import requests
# to identify emoji unicode characters
import emoji


def is_emoji(text):
    """This function returns True if there is an emoji in the given string else False"""
    return bool(emoji.get_emoji_regexp().search(text))

def link_to_get(link):
    """This function will get the url of the image & book download direct link using the given link for book download"""
    response = requests.get(link)
    th_html = bs(response.text , "html.parser")
    td_all = th_html.find_all("td" ,id ="info")
    td_all = td_all[0]
    td_a = td_all.find_all("a")
    link_href = td_a[1].get("href")
    img_link_td = td_all.find("img" ,alt="cover")
    img_link_src = img_link_td.get("src")
    img_link = f"http://library.lol{img_link_src}"
    return [link_href, img_link]

def book_get(name, res=25):
    """This function returns the list of books for the given name

        You can give in name : 
                        1. title of book
                        2. isbn of book
                        3. author of book
                        4. publisher of book
        
        res :
                1. 25
                2. 50
                3. 100

        Results:
                    [   0.Book Name, 
                        1.Author, 
                        2.Size, 
                        3.Book Type, 
                        4.Book Link, 
                        5.Book Image Link]"""
    Books = []
    if is_emoji(name) == True:
        return "Error: emoji"
    name = name.replace(" ", "+")
    # getting request and response
    url = f"http://libgen.is/search.php?req={name}&lg_topic=libgen&open=0&view=simple&res={res}&phrase=1&column=def&sort=extension&sortmode=DESC"
    response = requests.get(url)
    bs_html = bs(response.text , "html.parser")
    
    # scraping the site for response
    table = bs_html.find_all("table")
    table = table[2]
    table_rows = table.find_all("tr")
    a = len(table_rows)
    table_rows.pop(0)
    # print(url, "\n\n")
    if a > 1 :
        for i in table_rows :
            # make book list
            book_lst = []
            # getting all table datas
            table_datas = i.find_all("td")
            # book name
            book_name = table_datas[2].get_text()
            # author name
            author = table_datas[1].get_text()
            # getting link to book
            link_row = table_datas[9]
            a = link_row.find("a" , href = True)
            link = a.get("href")
            # getting image url & direct book download link
            link_all = link_to_get(link)
            # getting size of book
            size_row = table_datas[7]
            size = size_row.get_text()
            # getting type of book
            type_row = table_datas[8]
            type_ofit = type_row.get_text()
            book_lst.append(book_name)
            book_lst.append(author)
            book_lst.append(size)
            book_lst.append(type_ofit)
            book_lst.append(link_all[0])
            book_lst.append(link_all[1])
            Books.append(book_lst)
        return Books

    else:
        return "Error: no results found"


            
    
# a = book_get("Rich Dad Poor Dad",3)
# for i in a :
#     print(f"\n\nName : {i[0]}\nAuthor : {i[1]}\nSize : {i[2]}\nFormat : {i[3]}\nLink : {i[4]}\nImage : {i[5]}\n\n")