# Baidu Image Crawler
   :rocket: A simple command-line script for search and download images from [Baidu Image Search Engine](images.baidu.com)

## Dependencies
  * Python 2.7
  * OpenCV     :octocat:*(All downloaded images will be verified by OpenCV, to gurantee image file is OK)*
  ``` Shell
  # Install OpenCV library
  sudo apt-get install -y libopencv-dev
  sudo apt-get install -y python-opencv
  ```
  
  ## Usage
  ``` Shell
  python image_crawler.py $Image_Description $Search_Page_Begin_ID $Search_Page_End_ID
  ```
  * Parameters :
    * **$Image_Description** : Description of image, example : dog, cat, rabbit, etc
    * **$Search_Page_Begin_ID** (optional) : Each page of search present 60 images, which page do you want to start the crawling
    * **$Search_Page_End_ID** (optional) : which page do you want to end the crawling
    <br>
  * Outputs : All images will be download a folder named `$IMAGE_DESCRIPTION` in current directory.
    
  ## Example
  Here is a example to present how to crawl image about `美女` :
  ``` Shell
  python image_crawler.py 美女 0 128
  ```
  Here is what we got, a folder named `美女` that full of pictures :
    
  ![image](https://github.com/KaffeeCat/BaiduImageCrawler/blob/master/demonstration.jpg?raw=true)
