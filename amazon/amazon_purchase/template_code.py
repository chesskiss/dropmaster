from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
#import subprocess  # to run batch
import io
import os

#gets a string and an index, returns substring bound by quotes that also contains the specified index char
#examples:
#mystring: 123"blue"'456'"bloo"789
#j: 8 => output: blue
#j: 10 => output: '456'
#j: 18 => output: bloo
#output: blue
def str_inquote(mystring, j):
    start = j
    end = j
    while mystring[end] != '"':
        end += 1
    while mystring[start] != '"':
        start -= 1
    return mystring[start + 1: end]


def javaclick(WebD, path):
    element = WebD.find_element("xpath",path)
    WebD.execute_script("arguments[0].click();", element)


def panoptologin(WebD, user, password):
    WebD.get("https://moodle2223.technion.ac.il/auth/oidc")
    time.sleep(1)
    #https://panoptotech.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx#folderID=%22a1092a79-1131-4120-8067-ad8900e65fa8%22
    #WebD.find_element("xpath","//*[@id='page-wrapper']/nav/ul[2]/li[2]/div/span/a").click()
    #time.sleep(1)
    #WebD.find_element("xpath","// *[ @ id = 'region-main'] / div[2] / div[1] / div[1] / div / div / div / div / div[1] / a").click()
    #time.sleep(1)

    WebD.find_element("name","loginfmt").send_keys(user)
    #WebD.find_element_by_xpath("//input[@type='submit']").click()

    WebD.find_element("xpath","//input[@type='password']").send_keys(password)
    time.sleep(1)
    WebD.find_element("xpath","//input[@type='submit']").click()
    time.sleep(15)
    WebD.find_element("xpath","//input[@name='DontShowAgain']").click()
    #WebD.find_element_by_xpath("//input[@type='submit']").click()


def CSlogin(WebD, user, password):
    WebD.get("https://grades.cs.technion.ac.il")
    time.sleep(1)
    WebD.find_element_by_name("ID").send_keys(user[:user.find("@")])
    WebD.find_element_by_xpath("//input[@type='password']").send_keys(password)
    WebD.find_element_by_xpath("//input[@type='submit']").click()

    Xpath = "//form/table/tbody/tr/td[13]/table/tbody/tr[2]/td[2]/a"
    javaclick(WebD, Xpath)

    Xpath = '//div[1]/div/div/div[2]/div[2]/div[1]/a[6]'
    javaclick(WebD, Xpath)

    Xpath = "//div[1]/div/div/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[3]/td[3]/a"
    javaclick(WebD, Xpath)

    Xpath = "//div[1]/div/div/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[2]/td[3]/a"
    javaclick(WebD, Xpath)


# jumps ahead in a panopto video time stamp
def timelineJump(WebD, pixels):
    # video timeline element
    #Xpath = "/html/body/form/div[3]/div[9]/div[8]/main/div/div[4]/div/div[1]/div[5]/div/div[4]"
    #elem = WebD.find_element("xpath",Xpath)
    elem = WebD.find_element("id","positionBar")
    # click on (int)pixels pixels from the start of the timeline
    WebD.execute_script("arguments[0].style = 'left: " + str(pixels) + "px;'", elem)
    time.sleep(1)
    elem.click()


def CleanFiles(names):
    for name in names:
        f1 = open(name, "w+", encoding='utf-8')
        f1.write("")  # delete all file content
        f1.close()


#gets the download links for the video and audio and puts them in primaryLink and secondaryLink accordingly
def extractReg(WebD, primaryLink, secondaryLink):
    global firstload
    global splitClassroom
    try:
        timelineJump(WebD, 300)
    except:
        try:
            print("300 no work, try 200")
            timelineJump(WebD, 200)
        except:
            try:
                print("200 no work, try 100")
                timelineJump(WebD, 100)
            except:
                try:
                    print("100 no work, try 50")
                    timelineJump(WebD, 50)
                except:
                    print("all timeline jumps failed")
    elem = WebD.find_element("xpath","//*")
    oneVideoHTML = io.StringIO(elem.get_attribute("outerHTML"))
    tempLine2 = oneVideoHTML.readline()
    while bool(tempLine2):
        if bool(tempLine2.find('id="primaryVideo"') != -1):
            if bool(tempLine2.find('src="') != -1):
                ci = tempLine2[tempLine2.find('src="') + 5]
                if bool(ci == 'h'):  # checks if the link is regular http or blob (m3u8)
                    primaryLink = str_inquote(tempLine2, tempLine2.find('src="') + 10)
        if bool(tempLine2.find('id="secondaryVideo"') != -1):
            if bool(tempLine2.find('src="') != -1):
                splitClassroom = True
                ci = tempLine2[tempLine2.find('src="') + 5]
                if bool(ci == 'h'):
                    secondaryLink = str_inquote(tempLine2, tempLine2.find('src="') + 10)
        tempLine2 = oneVideoHTML.readline()
    return [primaryLink, secondaryLink]


def extractM3U8(WebD, primaryLink, secondaryLink):
    global firstload
    global splitClassroom
    logs = WebD.get_log("performance")  # NETWORK PACKETS FOR M3U8
    time.sleep(1)

    f1 = open("Packets.txt", "w+", encoding='utf-8')
    print(logs, file=f1)
    f1.close()
    f1 = open("Packets.txt", "r", encoding='utf-8')
    if not splitClassroom:
        secondaryLink = "NONE"

    tempLine2 = f1.readline()  # f1 is given as a huge single line for some reason
    if (primaryLink == "") or (secondaryLink == ""):  # one of the links was not found, it is m3u8
        while bool(tempLine2):
            index = tempLine2.find("index.m3u8")
            while bool(index != -1):
                tempLink = str_inquote(tempLine2, index)
                #hot fix: make sure link starts with 'http'
                if tempLink[0] == 'h':
                    if bool(primaryLink == ""):
                        primaryLink = tempLink
                    else:
                        if primaryLink != tempLink:
                            secondaryLink = tempLink
                tempLine2 = tempLine2[index + 4:]  # trim so you dont find the same link again
                index = tempLine2.find("index.m3u8")
                time.sleep(1)
            tempLine2 = f1.readline()
    f1.close()
    return [primaryLink, secondaryLink]

def addLink(videoName, primaryLink, secondaryLink):
    videoName = videoName.replace(':', "")
    f2 = open("Links.txt", "a+", encoding='utf-8')
    f2.write(videoName + "\n")
    f2.write(primaryLink + "\n")
    f2.write(secondaryLink + "\n")
    f2.close()

def main_F():
    try:
        config = open("config.txt", "r")
        username = config.readline()
        userpass = config.readline()
        config.close()
    except:
        print("no config.txt file found, enter username and userpass as input:")
        username = input("type in user email:")
        userpass = input("type in moodle/panopto password:")

    panoptoURL = input("type in panopto course web page:")
    # courseName is only used if a single video is provided
    courseName = "compM"#input("type in course name (english only):")
    #flag true if computer science site link is found
    CS = False
    if panoptoURL[panoptoURL.find("https://") + 8] == "g":
        CS = True


    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    #chrome_options = webdriver.ChromeOptions();
    #chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
    #driver = webdriver.Chrome("./chromedriver.exe", desired_capabilities=capabilities, options=chrome_options, )
    ser = Service(r"./chromedriver.exe")
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(15)
    #driver.execute_script("go('Courses', 'Sub', 5);")
    #driver.find_element_by_xpath("//input[@href='javascript:go('Courses','Sub',5)']").click()

    #logging in:
    panoptologin(driver, username, userpass)
    if not CS:
        #get opens a link
        driver.get(panoptoURL + "&sortAscending=true")

        time.sleep(2)
        # execute java script for CS site navigation
        driver.execute_script(
            "Panopto.Login.checkStorageAccess();window.location.search += ((window.location.search.indexOf('?') == -1) ? '?' : '&') + 'instance=TechnionAuthentication'; return false;")  # noqa"
        time.sleep(2)
        driver.get(panoptoURL + "&sortAscending=true")
    else:
        CSlogin(driver, username, userpass)


    time.sleep(1)

    CleanFiles(["Packets.txt", "Links.txt"])

    elem = driver.find_element("xpath","//*")
    time.sleep(10)
    allVideosHTML = io.StringIO(elem.get_attribute("outerHTML"))
    tempLine = allVideosHTML.readline()
    i = 0

    linksearchstr = '<a href="https://p'
    if not CS:
        linksearchstr = '<a class="detail-title" href="http'

    global firstload
    global splitClassroom
    firstload = True
    while bool(tempLine):
        if bool(tempLine.find(linksearchstr) != -1):
            splitClassroom = False
            Links = ["", ""]
            i += 1

            link = str_inquote(tempLine, tempLine.find("href") + 7)
            #print(tempLine)
            print(allVideosHTML.readline())
            print(allVideosHTML.readline())
            nameline = (allVideosHTML.readline())
            videoName = nameline[nameline.find("<span>") + 6:nameline.find("</span>")]
            print(videoName)
            driver.get(link)
            #videoName =
            if CS and firstload:
                time.sleep(2)
                driver.execute_script(
                    "Panopto.Login.checkStorageAccess();window.location.search += ((window.location.search.indexOf('?') == -1) ? '?' : '&') + 'instance=TechnionAuthentication'; return false;")  # noqa"
            firstload = False

            time.sleep(3)
            Links = extractReg(driver, Links[0], Links[1])
            Links = extractM3U8(driver, Links[0], Links[1])
            addLink(videoName, Links[0], Links[1])

            time.sleep(1)
        tempLine = allVideosHTML.readline()

    # subprocess.call([r'C:\Users\Ron\Desktop\Test\current_date.bat'])

    #if firstload is true here - we assume the user entered a single panopto video instead of a panopto folder
    if firstload:
        nameline = (allVideosHTML.readline())
        videoName = nameline[nameline.find("<span>") + 6:nameline.find("</span>")]
        splitClassroom = False
        Links = ["", ""]
        time.sleep(3)
        Links = extractReg(driver, Links[0], Links[1])
        Links = extractM3U8(driver, Links[0], Links[1])
        #addLink(courseName, Links[0], Links[1])
        addLink(videoName, Links[0], Links[1])

    os.remove("Packets.txt")
    time.sleep(1)
    driver.quit()


main_F()
