# Baidu Image Crawler
Search and download images from [Baidu Image Search Engine](images.baidu.com)

## Dependencies
  * Python 2.7
  * OpenCV
  ``` Shell
  # Install OpenCV library
  sudo apt-get install -y libopencv-dev
  sudo apt-get install -y python-opencv
  ```
  
  ## Usage
  ``` Shell
  python image_crawler.py $IMAGE_DESCRIPTION $SEARCH_BEGIN_PAGE_ID $SEARCH_END_PAGE_ID
  ```
  * Parameters :
    * `$IMAGE_DESCRIPTION` : Description of image, example : dog, cat, rabbit, etc
    *  (optional) `$SEARCH_BEGIN_PAGE_ID` : Each page of search present 60 images, which page do you want to start the crawling
    *  (optional) `$SEARCH_END_PAGE_ID` : which page do you want to end the crawling
    <br>
  * Outputs : All images will be download a folder named `$IMAGE_DESCRIPTION` in current directory.
    
  ## Example
  Here is a example to present how to crawl image about `柳岩` :
  ``` Shell
  python image_crawler.py 柳岩 0 128
  ```
