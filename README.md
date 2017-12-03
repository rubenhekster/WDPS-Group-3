# wdps2017
Web Data Processing Systems 2017 (VU course XM_40020)

# Assignment 1: Large Scale Entity Linking
The goal of this assignment was to take an input containing WARC files and process this input. The processing should contain a NER part as well as an entity linking component.

General Note: As you may notice, there are two repositories containing code from our group. 
There is this one which contains Python code and another one containing Java code.
The repository containing Java code is available under: "https://github.com/khehn/WDPS-Java.git"
And Benno should be added as a contributor there. 

IMPORTANT: The Java repository contains the final solution to our project.

But why did we use a second repository?
The reason for that was, that there have been problems deploying third party python library to the cluster. Due to this issue, it was not possible to test the solution in a real cluster setting. Therefore we couldn't be sure if our solution will maybe crash on a real cluster or not. 
To overcome this issue, we recoded our solution in Java.

We devided the assigments in three different steps:

## 1) Reading the WARC file from the HDFS
To read the WARC files from HDFS, we used the function newAPIHadoopFile togehter with a custom delimiter which we set to: "WARC/1.0". This can be adapted in the run.sh file if needed. This gives us as a result an RDD containing single WARC records as elements, which can then be parsed and cleaned. 
## 2) Parsing the HTML content to make it useable
As we parsed the WARC records using a dedicated library, we were able to remove all the WARC related overhead from the files. But the HTML tags still remained. Since they do not contain useful information, we removed them using the Jericho HTML parser.
## 3) Extract Named Entities from the text
The next step was to extract named entities from the text. For that task, we decided to use the Stanford CoreNLP library. Locally it worked fine, but as we tested it the first time in a real cluster setting on more than just the sample data, we experienced OutOfMemory errors, causing the program to crash. After some longer research on this topic we found out, that that could have been related to long sentences on the web pages. It could be, that through some mistakes the HTML parser makes on unclean text, really long sentences are created. These sentences cause the CoreNLP tools to acquire more and more memory until the program runs out of memory and crashes. To avoid this issue, we decided to have a maximum length of text to annotate at once of 10000 chars. If the text is long, we split it and process in two chunks. 
After we did that, the OutOfMemory erros were gone.
## 4) Link entities to Freebase
To link the entities to the Freebase, we used the following approach:
  1) We searched on the Elasticsearch instance potentially interesting candidates. (Candidate Generation)
  2) For these candidates we calculated their popularity score based on their occurence
  3) We furthermore calculated a similarity score using the dice coefficient and the hamming distance.
  4) We combined these the similarity score and the popularity score and ranked the potential candidates accordingly to get
     the most promising freebase id
  5) We generated the necessary output file.

## NOTES ON HOW TO RUN THE SOLUTION
