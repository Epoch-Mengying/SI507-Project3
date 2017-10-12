from bs4 import BeautifulSoup
import unittest
import requests

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.
def get_from_cache(url,file_name):
    try:
        html = open(file_name, 'r').read()
    except:
        html = requests.get(url).text
        f = open(file_name,"w")
        f.write(html)
        f.close()
    return html

html = get_from_cache("http://newmantaylor.com/gallery.html","cat.html")    
soup = BeautifulSoup(html, "html.parser")
# print(soup.prettify())
img_tag = soup.find_all("img")
for image in img_tag:
    print (image.get('alt', "No alternative text provided!"))


######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable 
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, but if you prefer to build up the code to do this scraping and caching yourself, that is OK.

def get_from_cache(url,file_name):
    try:
        html = open(file_name, 'r').read()
    except:
        html = requests.get(url).text
        f = open(file_name,"w")
        f.write(html)
        f.close()
    return html

main_page_html = get_from_cache("https://www.nps.gov/index.htm","nps_gov_data.html")


# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure 
# that the rest of the program can access.

# TRY: 
# To open and read all 3 of the files
try:
    arc_html = open(arkansas_data.html,'r').read()
    cal_html = open(california_data.html,'r').read()
    mi_html = open(michigan_data.html, 'r').read()
    
# But if you can't, EXCEPT:
except:    
    # Create a BeautifulSoup instance of main page data 
    # Access the unordered list with the states' dropdown
    main_soup = BeautifulSoup(main_page_html,'html.parser')
    states = main_soup.find('ul',{"class":"dropdown-menu SearchBar-keywordSearch"})

    # Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method
    all_states = states.find_all('li')

    # Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li, instead of the full li objects
    all_states_href = [x.find('a')['href'] for x in all_states]

    # Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's, using the accumulator pattern & conditional statements
    our_href = []
    our_destination = ['ar','mi','ca']
    for state in all_states_href:
        if any(x == state[7:9] for x in our_destination):
            our_href.append(state)
           
    # Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL in a variable.
    NPS = "https://www.nps.gov"
    ark_url = NPS + our_href[0]
    cal_url = NPS + our_href[1]
    mi_url = NPS + our_href[2]

## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm", Michigan's is "http://www.nps.gov/state/mi/index.htm" -- so if you compare that to the values in those href attributes you just got... how can you build the full URLs?

    # Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
    # (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)
    # And then, write each set of data to a file so this won't have to run again.
    ark_html = get_from_cache(ark_url,"arkansas_data.html")
    cal_html = get_from_cache(cal_url,"california_data.html")
    mi_html = get_from_cache(mi_url,"michigan_data.html")



######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?
ark_soup = BeautifulSoup(ark_html, 'html.parser')
cal_soup = BeautifulSoup(cal_html, 'html.parser')
mi_soup = BeautifulSoup(mi_html, 'html.parser')

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...
# print("-"*80, "ark")
# print (ark_soup.prettify())
# print("-"*80, "california")
# print (cal_soup.prettify())
# print("-"*80, "mi")
# print (mi_soup.prettify())


# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...





## Define your class NationalSite here:
class NationalSite(object):
    def __init__(self,soup_object):
        self.location = soup_object.find('h4').text
        self.name = soup_object.find('h3').text
        
        if soup_object.find('h2') is not None:
            self.type = soup_object.find('h2').text
        else:
            self.type = None
           
        if soup_object.find('p') is not None:
            self.description = soup_object.find('p').text
        else:
            self.description = ""
        
        if soup_object.find('ul') is not None:
            all_lists = soup_object.find('ul').find_all('a')
            if any(item.text == "Basic Information" for item in all_lists): 
                basic_info_link = [item for item in all_lists if item.text == "Basic Information"].find('a')['href']
                # print ("@@@", basic_info_link)
                basic_info_html = requests.get(basic_info_link).text
                basic_info_soup = BeautifulSoup(basic_info_html,'html.parser')
                if basic_info_soup.find('div',{"class": "physical-address"}) is not None:
                    self.address = basic_info_soup.find('div',{"class": "physical-address"}).find['span'].text
                else:
                    self.address = ""
            else:
                self.address = ""
           

            
    
    def __str__(self):
        return "{} | {}".format(self.name, self.location)
        
    def get_mailing_address(self):
        return self.address
        
    def __contains__(self, name):
        return name in self.name



## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:

# f = open("sample_html_of_park.html",'r')
# soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
# sample_inst = NationalSite(soup_park_inst)
# f.close()
# print (sample_inst.get_mailing_address)

######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.
arkansas_natl_sites = [NationalSite(item) for item in ark_soup.find('ul', {"id":"list_parks"}).find_all('div',{"class":"col-md-9 col-sm-9 col-xs-12 table-cell list_left"})]
california_natl_sites = [NationalSite(item) for item in cal_soup.find('ul', {"id":"list_parks"}).find_all('div',{"class":"col-md-9 col-sm-9 col-xs-12 table-cell list_left"})]
michigan_natl_sites = [NationalSite(item) for item in mi_soup.find('ul', {"id":"list_parks"}).find_all('div',{"class":"col-md-9 col-sm-9 col-xs-12 table-cell list_left"})]

##Code to help you test these out:
# for p in california_natl_sites:
#     print ("#"*80)
#     print(p)
# for a in arkansas_natl_sites:
#     print(a)
# for m in michigan_natl_sites:
#     print(m)



######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!

