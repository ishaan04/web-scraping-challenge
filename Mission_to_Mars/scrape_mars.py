from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, redirect
from splinter import Browser
import pandas as pd
import scrape_mars

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ####Red planet science####
    redplanet_url = "https://redplanetscience.com/"
    browser.visit(redplanet_url)

    #setup beautiful soup 
    redplanet_html = browser.html
    redplanet_soup = bs(redplanet_html, 'html.parser')

    #select the latest news title and article
    article_date = redplanet_soup.find("div", class_="list_date").text
    article_title = redplanet_soup.find("div", class_="content_title").text
    article_paragraph = redplanet_soup.find("div", class_="article_teaser_body").text

    ###Space Images####
    spaceimages_url = "https://spaceimages-mars.com"
    browser.visit(spaceimages_url)

    ###setup beautiful soup ####
    spaceimages_html = browser.html
    spaceimages_soup = bs(redplanet_html, 'html.parser')

    #####create URL with image url####
    featured_image_url = spaceimages_soup.find_all("img")[1]["src"]

    ###Mars Facts#####
    marsfacts_url = "https://galaxyfacts-mars.com"
    browser.visit(marsfacts_url)

    #####scape website and load facts table into a dataframe####
    mars_facts = pd.read_html(marsfacts_url)
    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = ['Description', 'Mars', 'Earth']
    mars_facts_df = mars_facts_df.set_index('Description')

    mars_facts_df 
    mars_facts_url = mars_facts_df.to_html()
    mars_facts_url.replace("\n","") 

    ###Mars Hemisphere###
    mars_hemi_url = "https://marshemispheres.com/"
    browser.visit(mars_hemi_url)

    #####setup beautiful soup####
    mars_hemi_html = browser.html
    mars_hemi_soup = bs(mars_hemi_html, "html.parser")

    #####scrape website to identify the titles of each of the hemispheres####
    mars_hemi_title = mars_hemi_soup.findAll("h3")
    mars_hemi_images=[]

    for i in range(len(mars_hemi_title)-1):
        browser.links.find_by_partial_text(mars_hemi_title[i].text).click()
        html_x = browser.html
        soup_x = bs(html_x, "html.parser")
        
        mars_hemi_images.append({"title": mars_hemi_title[i].text, 
                                    "img_url": browser.links.find_by_partial_text('Sample')[0]['href']})
        browser.visit(mars_hemi_url)
    mars_hemi_images

    ##### Create dictionary for Mars information####
    mars_dict = {
        "News_Date":article_date,
        "News_Title":article_title,
        "News_Paragraph":article_paragraph,
        "featured_image_url":featured_image_url,
        "Mars_Facts":str(mars_facts),
        "Mars_Hemisphere_Images":mars_hemi_images
    }

    browser.quit()

    ##### Return results####
    print(mars_dict)
    return mars_dict

if __name__ == "__main__":
    scrape()
