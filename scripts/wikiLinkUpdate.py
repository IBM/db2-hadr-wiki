from bs4 import BeautifulSoup
import sys

try:
	from googlesearch import search
except ImportError:
	print("No module named 'google' found")

# Enter the file path here 
filePath = "/Users/cathzhou/db2-hadr-wiki/docs/hadrTutorial.html"

# Reading from the file
HTMLFile = open(filePath, "r")
readHTML = HTMLFile.read()
contents = BeautifulSoup(readHTML, 'lxml')

# Initialize searching pre-condition
condition = "IBM db2 HADR "

# Initialize wiki (old) version and current version
oldVersion = "11.1"
curVersion = "11.5"

# Prefix for link
oldLinkPrefix = "https://www.ibm.com/docs/en/db2/"+oldVersion+"?topic="
searchCondition = "https://www.ibm.com/docs/en/db2/"+curVersion+"?topic="

print('Starting to modify file ', filePath)

# Redirect output to output file
original_stdout = sys.stdout
outFile = open('output.txt', 'w')
sys.stdout = outFile

# Start finding links in file
for a in contents.find_all('a'):
    tag = str(a.text)
    keyword = condition+tag
    oldLink = a.get("href")
    if oldLink is not None and oldLinkPrefix in oldLink:
        print("Searching for: ", keyword)
        print("- Old link:", oldLink)
        for j in search(keyword, tld="co.in", num=10, stop=10, pause=2):
            if searchCondition in j:
                topic = j.split("topic=", 1)[1]
                newLink = searchCondition+topic
                print("- New link:", newLink)
                a['href'] = newLink
                break
        # Alternative: if topic is still the same, update without search
        # topic = oldLink.split("topic=", 1)[1]
        # newLink = searchCondition+topic
        # print("- New link:", newLink)
        # a['href'] = newLink

sys.stdout = original_stdout
# Write file with new link into webpage
webfile = open(filePath, "wb")
webfile.write(contents.prettify("utf-8"))
webfile.close()