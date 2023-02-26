# Faster RCNN

Classes_list.ipynb to generate classes_list.csv. From the csv file, we will get the list of classes which is needed for the model as a parameter.  
It just takes the names of the files in train/test and finds out which all classes exist. Since every file renamed as classname count.jpg, it won't be hard to extract.  

Train/test labels.csv is the file containing bounding boxes and image names. We create train/test dataset based on that.   

In google colab, we need to add the directory having train/test as a shortcut onto my drive. Then only can we access the files in drive thorugh colab.   

In Azure ML, we need to upload the train/test folders onto workingspacedirectory. 
