import multiprocessing

NUM_OF_THREADS = 10
FILE_NAME = "finalMissIds.txt"

source = open(FILE_NAME, "r")
id = []

#####################################################################
# in this code by using the phenotypes id in the "FILE_NAME".txt file
# we weill download its .fastq files from ENA databese
#####################################################################
firstContent = source.readline()
while firstContent != "":
    id.append(firstContent[0: len(firstContent) - 2])
    firstContent = source.readline()

generatedUrl = ""


# def studyAccesion(id):
    # import urllib2
    # import requests
    # contents = urllib2.urlopen("https://www.ebi.ac.uk/ena/data/view/" + id).read()
    # res = requests.post("https://www.ebi.ac.uk/ena/data/view/" + id)
    # print res.text


def urlFinder(url, sleepNow=False):
    print (url)
    try:
        import urllib2

        generatedUrl = 'https://www.ebi.ac.uk/ena/data/view/' + url + '%26display%3Dxml'

        # try:
        #     studyAccesion(url)
        # except:
        #     print "getting the accession was unsuccessful for" + url

        print generatedUrl
        contents = urllib2.urlopen(generatedUrl).read()
        # print contents
        url = ""
        for i in range(0, len(contents)):
            if contents[i:(i + 24)] == "<DB>ENA-FASTQ-FILES</DB>":
                for j in range(i, len(contents)):
                    if contents[j:(j + 4)] == "http":
                        for k in range(j, len(contents)):
                            url = url + contents[k]
                            if contents[k + 1] == ']':
                                return fileDownloader(url)

        return "Error" + url
    except:
        if sleepNow == False:
            print "start sleeeeeeeeeeeeeeeep for " + url
            import time
            time.sleep(1800)
            print "finish sleeeeeeeeeeeeeeeep for " + url
            urlFinder(url, True)
        else:
            with open("missIdForDownload.txt", "a+") as txt_file:
                txt_file.write(url + '\n')
            print "was't able to download data for : " + url


def fileDownloader(url):
    import wget
    import urllib2
    contents = urllib2.urlopen(url).read()
    urls = []

    fUrl = ""
    find = 0
    for i in range(0, len(contents)):
        if find == 1:
            break
        if contents[i: (i + 4)] == "ftp.":
            for j in range(i, len(contents)):
                fUrl = fUrl + contents[j]
                if contents[(j - 8):j + 1] == ".fastq.gz":
                    urls.append(fUrl)
                    fUrl = ""
                    break

    for i in range(0, len(urls)):
        print urls[i]
        wget.download("http://" + urls[i])
        print ("done")


def main():
    pool = multiprocessing.Pool(processes=NUM_OF_THREADS)
    pool.map (urlFinder, (id[i] for i in range(0, len(id))))


main()