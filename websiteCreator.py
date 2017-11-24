'''
Created on Nov 23, 2017

@author: Shantanu Deshmukh
'''

try:
    import nltk
    import urllib2
    from bs4 import BeautifulSoup
    from ctypes.test.test_errno import threading
    import os
    import json
    import random
    import bodyTemplates
    import webbrowser
except:
    print "Few of the libraries are not imported.. Kidly re-check.."

random.seed(1024)

def preprocess(document):
    '''
    Pre processes the document, by extracting sentences, tokenizing words and pos tagging
    '''
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

class GoogleTextSearch(threading.Thread):
    '''
    Threaded google text search
    '''
    def __init__(self, q, textCorpus):
        threading.Thread.__init__(self)
        self.searchURL = "https://www.google.com/search?&q="+q.replace(" ","+")
        self.textCorpus = textCorpus
        self.q = q
    
    def run(self):
        try:
            print "Getting text for "+self.q
            header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
            res = get_soup(self.searchURL, header)
            url = res.find('h3',{'class':'r'}).find('a')['href']
            res = get_soup(url, header)
            text = ""
            count = 0
            for p in res.find_all('p'):
                if len(p.get_text()) < 150:
                    continue
                text+=p.get_text()
                if count == 15:
                    break
                count+=1
            self.textCorpus[self.q] = text
        except:
            #Handle all scraping errors like page not found, parsing errors, forbidden, etc
            pass
        
class FetchGoogleImages(threading.Thread):
    '''
    Threaded google image search and saver
    '''
    def __init__(self, q, imageID):
        threading.Thread.__init__(self)
        self.searchURL = "https://www.google.co.in/search?source=lnms&tbm=isch&q="+q.replace(" ","+")
        self.imageID = imageID
        self.q = q
        
    def run(self):
        try:
            print "Searching image for query",self.q
            path = os.getcwd()+"\\images\\"
            if not os.path.exists(path):
                os.makedirs(path)
            header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
            req = get_soup(self.searchURL, header)
            
            ActualImages=[]# Referred from https://stackoverflow.com/questions/35809554/how-to-download-google-image-search-results-in-python
            a = req.find("div",{"class":"rg_meta"})
            link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            ActualImages.append((link,Type))
                
            ###print images
            for i , (img , Type) in enumerate( ActualImages):
                try:
                    req = urllib2.Request(img, headers={'User-Agent' : header})
                    raw_img = urllib2.urlopen(req).read()
                    
                    filename = self.imageID
                    if len(Type)==0:
                        f = open(os.path.join(path, filename+".jpg"), 'wb')
                    else :
                        f = open(os.path.join(path , filename+"."+Type), 'wb')
                    
                    f.write(raw_img)
                    print "Image saved for ",self.q
                    f.close()
                except Exception as e:
                    pass
        except:
            #Handle all scraping errors like page not found, parsing errors, forbidden, etc
            pass
            

def createAndLaunchWebPage(name, webpageText):
    '''
    Creates webpage with given name and launches the browser
    '''
    path = os.getcwd()+"\\images\\"
    if not os.path.exists(path):
        os.makedirs(path)
    webPage = open(path+repr(name)+".html","w")
    webPage.write(webpageText)
    webPage.close()
    webbrowser.open_new_tab('file://' + os.path.realpath(path+repr(name)+".html"))

def getImage(i):
    '''
    returns ith image from all images
    '''
    return imageNames[i%len(imageNames)]+".jpg".replace(" ","+")

def getText(i, noOfwords=0):
    '''
    returns 'noOfwords' from ith text of the text corpus, if noOfWords = 0 returns whole text
    '''
    text = textCorpus[list(textCorpus)[i%len(imageNames)]]
    text = text.encode('ascii','ignore')
    if noOfwords!=0:
        words = text.split()
        if len(words) < noOfwords:
            return text
        else:
            return " ".join(word for word in words[0:noOfwords])
    return text   
    
def getMid(midTemplate, item1, item2, item3):
    '''
    returns mid element with mid template and 3 items followed by item
    '''
    mid = bodyTemplates.MIDS.values()[midTemplate]
    mid = mid.replace("$$image1$$",getImage(item1))
    mid = mid.replace("$$text1$$",getText(item1,100))
    mid = mid.replace("$$image2$$",getImage(item2))
    mid = mid.replace("$$text2$$",getText(item2,100))
    mid = mid.replace("$$image3$$",getImage(item3))
    mid = mid.replace("$$text3$$",getText(item3,100))
    return mid

#[banner1DNA,banner2DNA,midTemplateSequence[0,len(mid)]DNA,midDataSequence[0,len(data)]DNA]
def generateChromosome(imageNames):
    '''
    Chromosome contains 4 dna's, 2 for top and 2 for mid
    t - Template
    bt - Top banner template
    b1,b2 - Banner data
    ts - Mid Template sequence
    ds - Mid data sequence
    '''
    chromosome = {}
    t = random.randint(0,len(bodyTemplates.TEMPLATES)-1)
    bt = random.randint(0,len(bodyTemplates.TOPS)-1)
    b1 = random.randint(0,len(imageNames)-1)
    b2 = b1
    while True:
        if b1 != b2:
            break
        b2 = random.randint(0,len(imageNames)-1)
    midTemplates = bodyTemplates.MIDS
    ds = random.sample(xrange(len(imageNames)), len(imageNames)) 
    lenOfTS = len(ds)/3
    ts = []
    while lenOfTS!=0:
        lenOfTS-=1
        ts.append(random.randint(0,len(midTemplates)-1))
    chromosome['t'] = t
    chromosome['bt'] = bt
    chromosome['b1'] = b1
    chromosome['b2'] = b2
    chromosome['ts'] = ts
    chromosome['ds'] = ds
    return chromosome

def crossOverAndMutate(chromosome1, chromosome2, imageNames):
    '''
    Cross overs and mutates DNA's of the 2 chromosomes, to generate new list of 3 chromosome
    '''
    chromosomes = []
    for i in range(3):
        dominant = random.randint(0,1)
        if dominant == 1:
            chromosome = dict(chromosome1)
        else:
            chromosome = dict(chromosome2)
        randomSwap = random.randint(0,len(chromosome1)-1)
        swapKey = chromosome1.keys()[randomSwap]
        chromosome[swapKey] = chromosome2[swapKey]
        mutateOn = random.randint(0,10)
        if mutateOn < len(chromosome1):
            mutateKey = chromosome1.keys()[mutateOn]
            if mutateKey == 't':
                chromosome['t'] = random.randint(0,len(bodyTemplates.TEMPLATES)-1)
            elif mutateKey == 'bt':
                chromosome['bt'] = random.randint(0,len(bodyTemplates.TOPS)-1)
            elif mutateKey == 'b1':
                chromosome['b1'] = random.randint(0,len(imageNames)-1)
                while True:
                    if chromosome['b1'] != chromosome['b2']:
                        break
                    chromosome['b1'] = random.randint(0,len(imageNames)-1)
            elif mutateKey == 'b2':
                chromosome['b2'] = random.randint(0,len(imageNames)-1)
                while True:
                    if chromosome['b1'] != chromosome['b2']:
                        break
                    chromosome['b2'] = random.randint(0,len(imageNames)-1)
            elif mutateKey == 'ts':
                ds = random.sample(xrange(len(imageNames)), len(imageNames)) 
                lenOfTS = len(ds)/3
                ts = []
                while lenOfTS!=0:
                    lenOfTS-=1
                    ts.append(random.randint(0,len(bodyTemplates.MIDS)-1))
                chromosome['ts'] = ts
            elif mutateKey == 'ds':
                chromosome['ds'] = random.sample(xrange(len(imageNames)), len(imageNames))
        chromosomes.append(chromosome)
    
    return chromosomes
    
def convertChromosomeToHTML(chromosome, imageNames, title):
    '''
    Maps each element of DNA from the chromosome to appropriate sections in the website
    '''
    body = bodyTemplates.TEMPLATES.values()[chromosome['t']]

    #set top
    top = bodyTemplates.TOPS.values()[chromosome['bt']]
    top = top.replace("$$banner1$$",getImage(chromosome['b1']))
    top = top.replace("$$banner2$$",getImage(chromosome['b2']))
    top = top.replace("$$head1$$",getText(chromosome['b1'],10))
    top = top.replace("$$head2$$",getText(chromosome['b2'],50))
    body = body.replace("$$top$$",top)
    
    mid = ""
    dataCount = 0
    templateCount = 0
    while dataCount+3 < len(imageNames):
        template = bodyTemplates.MIDS.values()[chromosome['ts'][templateCount]]
        templateCount+=1
        template = template.replace("$$image1$$",getImage(chromosome['ds'][dataCount]))
        template = template.replace("$$text1$$",getText(chromosome['ds'][dataCount],100))
        dataCount+=1
        template = template.replace("$$image2$$",getImage(chromosome['ds'][dataCount]))
        template = template.replace("$$text2$$",getText(chromosome['ds'][dataCount],100))
        dataCount+=1
        template = template.replace("$$image3$$",getImage(chromosome['ds'][dataCount]))
        template = template.replace("$$text3$$",getText(chromosome['ds'][dataCount],100))
        dataCount+=1
        mid+=template
        
    body = body.replace("$$mid$$",mid)
    body = body.replace("$$title$$",title)
    
    return body
    


def dwnldDataAndCreateWebsite(raw, title):
    '''
    Download data to design websites
    '''
    print "Searching for entities in the text.."
    sentences = preprocess(raw)
    sentencesChunk = [nltk.ne_chunk(sentence) for sentence in sentences]
    threads = []
    global imageNames
    global textCorpus
    imageNames = []
    textCorpus = {}
    t = FetchGoogleImages(q=title,imageID=title)
    t.start()
    threads.append(t)
    t = GoogleTextSearch(title,textCorpus)
    t.start()
    threads.append(t)
    
    namedEntities = set()
    reParser = nltk.RegexpParser('''CHUNK: {<PERSON>}
                                            {<LOCATION>}
                                            {<FACILITY>}
                                            {<GPE>}''')  
         
    #Extracting interaction using regex                                                      
    for sentenceChunk in sentencesChunk:
        tree = reParser.parse(sentenceChunk)
        for subtree in tree.subtrees():
            if subtree.label() == 'CHUNK': 
                namedEntities.add(' '.join([list(name)[0] for name in subtree[0]]))
    
    namedEntities = list(namedEntities)
    
    if len(namedEntities) < 3:
        print "Too few entities found, kindly add in more text"
        return
    
    print "Scrapping data to create the website"
    	
    for i in range(10):
        index = random.randint(0,len(namedEntities))
        t = FetchGoogleImages(q=namedEntities[index]+title,imageID=namedEntities[index])
        t.start()
        threads.append(t)
        t = GoogleTextSearch(namedEntities[index]+title, textCorpus)
        t.start()
        threads.append(t)
        
    print "\nKindly be patient, threads are grabbing awesome images from the internet.. This will take some time.."
    for t in threads:
        t.join()
        
    print "Website data scrapped successfully, starting website creation.."

    for key in textCorpus.keys():
        imageNames.append(key[:key.index(title)])
    
    
    ####Genetic Algorithm to create website########
    webpageTemplate = bodyTemplates.WEBPAGETEMPLATE
    webpageTemplate = webpageTemplate.replace("$$title$$",title)

    i = 0
    initialPopulation = []
    while i<3:
        i+=1
        chromosome = generateChromosome(imageNames)
        initialPopulation.append(chromosome)
        body = convertChromosomeToHTML(chromosome, imageNames, title)
        html = webpageTemplate.replace("$$body$$",body)
        createAndLaunchWebPage("webPage"+repr(i), html)
            
    while True:
        print "Genetically curated web pages:"
        for k,chromosome in enumerate(initialPopulation):
            print repr(k+1)+". Webpage"+repr(k+1)+".html"
        
        i = 0
        j = 0
        try:    
            print "Select 2 of the 3 web pages you liked the most, I will genetically evolve them to create new ones.. \n(Enter comma seperated options e.g. >>> 1,2 or >>> 2,3 )"
            userInput = raw_input("If you liked a page and want to stop, enter 'e'; grab the liked webpage's html from the parent directory..\n>>> ")
            if userInput=='e':
                break
            i = userInput.split(",")[0]
            j = userInput.split(",")[1]
            try:
                i = int(i)
                j = int(j)
            except:
                print "Kindly enter only integer options!"
                continue
            if i==j:
                print "Kindly select 2 different options!"
                continue
            if i>3 or k>3:
                print "Kindly enter correct options!"
                continue
        except:
            print "Kindly enter correct userInput (comma seperated options e.g. >> 1,2 or >> 2,3 )"
            continue
        
        print "Displaying in the browser 3 freshly brewed pages using the pages you liked.."
        initialPopulation = crossOverAndMutate(initialPopulation[i-1], initialPopulation[j-1], imageNames)
        for l,chromosome in enumerate(initialPopulation):
            body = convertChromosomeToHTML(chromosome, imageNames, title)
            html = webpageTemplate.replace("$$body$$",body)
            createAndLaunchWebPage("webPage"+repr(l+1), html)
    
    

if __name__ == '__main__':
    print "Welcome to the Website Creating agent!"
    while True:
        print "Select the text file which has your data, from below:"

        dirs = next(os.walk('.'))[2]
        files = {}
        menu = ""
        folderNames=[]
        i = 0
        for fileName in dirs:
            if fileName.find('.txt') > 0:
                files[i] = fileName
                menu += repr(i+1)+". "+fileName+"\n"
                i += 1
        
        print menu
        
        userInput = raw_input(">>> ")
        try:
            userInput = int(userInput)
            if userInput == 0:
                print "Thank you!"
                break
            if userInput > len(files):
                raise KeyError
        except:
            print "Kindly select the correct option.."
            continue
        
        data = ""
        with open(files[userInput-1], 'r') as ufile:
            data = ufile.read().replace('\n', '')
            
        dwnldDataAndCreateWebsite(data, files[userInput-1][:files[userInput-1].find(".")])
        
    

