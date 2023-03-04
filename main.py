from bs4 import BeautifulSoup
import requests
#import time
import gspread

index = 0# Index of the post

def get_data(html_text):
    global index
    soup = BeautifulSoup(html_text, 'lxml')#Parsing the HTML
    
    headers = soup.find_all('div', class_='inside-article')# Get all the headers of the posts

    for header in headers:
        banner_tag = header.find('div',class_ = 'post-image')# Check if the post has a banner
        post_date = header.div.span.find('time', class_='entry-date published').text# Get the date the post was published
        post_title = header.find('h2', class_='entry-title').text# Get the title of the post
        post_link = header.h2.a['href']# Get the link to the post
        index+=1
        # Print the data on terminal
        print(f"'{post_title}' was posted on {post_date}")
        print(f"Link: {post_link}")
        if banner_tag:
            banner = "Yes"
            print("Banner: Yes")
        else:
            banner = "No"
            print("Banner: No")
        print('')

        gc = gspread.service_account(filename='creds.json')
        sh = gc.open('scrapedtopics').sheet1
        sh.append_row([index, post_title, str(post_date), str(post_link), banner])

def get_title():
    URL = ['https://ux360.design/', 'https://ux360.design/page/']# URLs to be scraped
    for url in range(0,2):
        if url == 0:# Check if the URL is the first page
            html_text = requests.get(URL[url]).text
            get_data(html_text)
        else:# If not, loop through the pages
            for i in range(2, 7):
                html_text = requests.get(URL[url] + str(i) + '/').text
                get_data(html_text)
        

if __name__ == '__main__':
    #while True: # Uncomment this line to run the script continuously
        get_title()
        #Uncomment the following lines to run the script after some delay again
        #time_wait = 24
        #print(f"Waiting {time_wait} hours before checking again...")
        #time.sleep(time_wait * 60 * 60)