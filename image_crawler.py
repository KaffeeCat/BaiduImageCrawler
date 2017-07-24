#!/usr/bin/python  
#-*-coding:utf-8-*-  

# ------------------------------
# Filename : image_crawler.py
# Author : Wang Kang
# E-mail : prince.love@live.cn
# Date : 2017-7-21
# Purpose : To crawl images in BISE(Baidu Image Search Engine)
# How to use : Change the image descripe words in 'search_word'
# Dependencies (OpenCV):
#   sudo apt-get install -y libopencv-dev
#   sudo apt-get install -y python-opencv
# ------------------------------
import urllib, socket
import sys, os, cv2, Queue

# ------------------------------
# Set the search word here

search_word = unicode('劳力士','utf8')  # Descripe the image what you want to search
search_page_index_begin = 0   # Search result page index (begin)
search_page_index_end = 256   # Search result page index (end)
socket.setdefaulttimeout(5.0)   # how long do you want to wait a image download (seconds)
max_retry_times = 5     # how many times do you want to retry access the website or download file

if len(sys.argv) >= 2 :
    search_word = unicode(sys.argv[1],'utf8')

if len(sys.argv) >= 3 :
    search_page_index_begin = int(sys.argv[2])

if len(sys.argv) >= 4 :
    search_page_index_end = int(sys.argv[3])

print 'Search words : ' + search_word
#-------------------------------
# Form an website link by search word
image_index = search_page_index_begin*60# (each search page present 60 images)
url_base = 'http://image.baidu.com/search/' + 'flip?tn=baiduimage&ie=utf-8&word=' +urllib.quote(search_word.encode('utf8')) + '&pn='

# Create a directory for current task
if not os.path.exists(search_word) :
    os.mkdir(search_word)

#-------------------------------
# Download image to local path
def download_image(image_url, store_path):
    
    #-------------------------------
    # Method 1 : Download file by urllib.urlretrieve
    try :
        # Method 1 : Download the file
        file_name,file_content = urllib.urlretrieve(image_url, store_path)
        
        # Check whether image correct (if failed, try method 2)
        image = cv2.imread(file_name)
        if image is not None :
            return file_name, image

    except Exception, e:
        print e;

    #-------------------------------
    # Method 2 : Download file by system downloader(t3 = retry 3 times)
    os.system("wget -t3 -c " + image_url + " -O " +store_path)
    return store_path, cv2.imread(store_path)

#-------------------------------
# Find all image url in HTML content
def find_all_image_url(html) :
    image_object_prefix = '"objURL":"'  # This is the image object prefix of Baidu Image
    image_object_prefix_len = len(image_object_prefix)
    next_search_begin = 0
    image_url_queue = Queue.Queue();

    while True :
        # Find the image object prefix
        image_object_begin = html.find(image_object_prefix, next_search_begin)

        # If find nothing, stop search
        if image_object_begin < 0 :
            break

        # Fetch the image url
        image_object_end = html.find('"', image_object_begin+image_object_prefix_len)
        image_url = html[image_object_begin+image_object_prefix_len:image_object_end]

        # Fetch the image filename suffix
        image_file_suffix = '.jpg'
        image_file_suffix_loc = image_url.rfind('.')
        if image_file_suffix >= 0 :
            image_file_suffix = image_url[image_file_suffix_loc:len(image_url)]

        if len(image_file_suffix) > 5 : # if suffix is too long, shorten them (if it is *.jpg?width=xxx&height=xxx)
            image_file_suffix = '.jpg'

        image_url_queue.put([image_url, image_file_suffix])

        # Update next search begin location
        next_search_begin = image_object_end

    return image_url_queue

#-------------------------------
# Start search
for i in range(search_page_index_begin,search_page_index_end):
    
    url = url_base + str(image_index)

    # Try to fetch the html content
    for try_access_times in range(1,max_retry_times) :
        try :
            html = urllib.urlopen(url).read()
            try_access_times = 0
            break   # fetch content successed
        except Exception, e:
            print 'Try to access url : ' + url + ' ' + str(try_access_times) + ' times'
            try_access_times += 1
            if try_access_times < 8 :
                continue
            else :
                break

    
    # Fetch all image's url in HTML
    image_url_queue = find_all_image_url(html)

    # Download all image fetched from HTML
    while not image_url_queue.empty() :
        image_url, image_file_suffix = image_url_queue.get()

        # Give it a name in local storage
        local_file_name = search_word.encode('utf8')+'/'+str(image_index)+image_file_suffix

        # Forward to next image index
        image_index += 1
        
        # Download the image
        print '# ------------------------------------------'
        print '# Image No.' + str(image_index)
        print '# Image URL : ' + image_url
        for try_download_times in range(1,max_retry_times) :
            file_name, image = download_image(image_url, local_file_name)
            if file_name is not None and image is not None :
                print '# Download successed, image size = ' + str(image.shape[0]) + 'x' + str(image.shape[1]) + 'x' + str(image.shape[2])
                break
            else:
                print '# Download failed, Try to download image ' + str(try_download_times) + ' times'
                if os.path.exists(local_file_name) :
                    os.remove(local_file_name)


    # Forward to next page (each search page present 60 images)
    image_index += 60
