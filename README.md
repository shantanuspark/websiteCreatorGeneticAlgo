# websiteCreatorGeneticAlgo
This python script creates a website from a .txt file by recognizing entities(person, location, organization, etc.) from the file, searching and downloading those entities's information and creating a website out of it using genetic algorithm.

Execution:
Add .txt file containing the relevant information you want to be displayed on the website.
Run the WebsiteCreator.py

It will ask for the .txt file, which is to be used for creating the website.

I have included 2 sample .txt files(The Flash.txt and Stranger Things.txt) as samples(text copied from wikipedia). 

Working:
Using NLTK the script first finds all the entities in the file.
Performs google search on the eitities
Creates 3 sample(first generation) websites
Asks user to select the 2 websites he liked the most
Creates new 3 websites depending on the user input

Output:
Below is the sample output for Flash website
<img src="https://github.com/shantanuspark/websiteCreatorGeneticAlgo/blob/master/output_website.png" />
