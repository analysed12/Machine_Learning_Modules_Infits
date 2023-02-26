# Data Handling  

### Requirements     
  -> Source directory containing different class folders, inside of which contains images and annotations.    
  -> Class names are unique so as to avoid file overwriting during train test split where each filename will be an iteration of the class name.    
  -> Annotation and image file name are exactly the same (obviously except the extension)    
  -> The three ipynb files : Data preparation, Data Repair, Data Cleaning are in the same directory.  
  -> 'good_xml_file' have only one object node in it. [here example.xml]  
  -> Don't create destination directory beforehand or have contents in them. It will be removed during runtime.
  
### Functionalities

  #### Data Repair 
  Data Repair fixes   
    xml files with improper bounding boxes,     
    extracts bounding boxes from txt, json annotation files and writes them onto an xml file.   
  This is done by taking in the format of a 'good_xml_file' and writing over the details as required.   
  It is to be noted that 'good_xml_file' have only one object node in it since we append object nodes depending on corrupted annotation file's bounding box count.   
  i.e If the count of bounding box coordinates are 8, it means two objects. So we append object node once.  
  
  #### Data Prepare 
  Data Prepare removes     
    annotation files without images,   
    images without annotation files,  
    json, txt files,   
    images files with improper extensions,    
    folders inside class folders except folders named ['Label','annotation']     
  from the class directory onto the disparity directory. It also deletes class folders without any file in them.   
  
  #### Data Cleaning  
  Creates destination directory and copies the proper files there.   
  Removes folders having with less than 4 files in destination directory since it can't be split into train and test. [4 files means 2 annotations + 2 images which is the     minimum]  
  Splits files in class folders into train and test in the ratio 80% 20%.  
  
 
### Usage   
  Data Cleaning need only be run since it calls the respective functions from the other two notebooks.    
  Source directory -> The directory in which we have the class folders    
  Disparity directory -> The directory we store files that are not suitable for train/test split.    
  Destination directory -> The clean files will be copied to this directory where they will be split.    
  Image Extension List -> extensions of images we would like to see in the train/test folder.    
  Annotation Extension List -> extensions of annotations we would like to see in the train/test folder.    
  text -> UNIQUE string that is not present in any filenames or classnames so that during renaming, we don't replace any files. It will be removed after a count has been assigned.    

### Notes    
  Data Repair fixes json files, txt files assuming they have bounding boxes in the format (xcenter,ycenter,width,height) and normalized (xcenter,ycenter,width,height) respectively.    
  The only feature we need from an annotation file is the bounding box coordinates everything else will be filled automatically or extracted from the image.    
  

