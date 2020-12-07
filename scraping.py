
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager




# Set Executable Path & Initialize Chrome Browser


# Window User
Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path)



# Defining scrape & dictionary
def scrape_all():
    final_data = {}
    output = mars_news()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = featured_image()
   # final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = mars_facts()
    final_data["mars_hemisphere"] = hemisphere()

    return final_data



# ### Visit the NASA Mars News Site
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ### JPL Space Images Featured Image

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url


# ### Mars Facts

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()





# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

def hemisphere(browser):
    
    

   # 1. Use browser to visit the URL 
   url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
   browser.visit(url)



   from bs4 import BeautifulSoup
  # 2. Create a list to hold the images and titles.
   hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# HTML Object
   html_hemispheres = browser.html

# Parse HTML with Beautiful Soup
   soup = BeautifulSoup(html_hemispheres, 'html.parser')

# Retreive all items that contain mars hemispheres information
   items = soup.find_all('div', class_='item')


# Store the main_ul 
   hemispheres_main_url = 'https://astrogeology.usgs.gov'

# Loop through the items previously stored
   for i in items: 
    # Store title
       title = i.find('h3').text
    
    # Store link that leads to full image website
       partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
       browser.visit(hemispheres_main_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
       partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
       soup = BeautifulSoup( partial_img_html, 'html.parser')
    
    # Retrieve full image source 
       img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
       hemisphere_image_urls.append({"title" : title, "img_url" : img_url})


# In[35]:


# 4. Print the list that holds the dictionary of each image url and title.
   return hemisphere_image_urls




# 5. Quit the browser
browser.quit()


# In[ ]:





