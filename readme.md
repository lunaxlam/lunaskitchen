# **Luna's Kitchen**

<p align="center">
  <img 
    width="600"
    src="img/menu.png"
  >
</p>

## **Summary**
*Luna's Kitchen* is a terminal-based recipe generator Python program that uses the requests and BeautifulSoup4 modules to webscrape data from [Allrecipes](https://www.allrecipes.com/) to populate a recipe title, recipe description summary, link to recipe URL, and recipe details including serving size, ingredients list, and instructions list. 

Users have the ability to read and write a recipe and the recipe ingredients to a "my recipes list" and "shopping list" .txt files. 

## **Tech Stack**
Backend: Python<br/>
Libraries: [Requests](https://pypi.org/project/requests/), [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

## **Features**
### **Search for Recipes**
<img width="300" src="img/getrecipe.png"><br>

### **View Results**
<img width="600" src="img/viewresults.png"><br>

### **View Recipe**
<img width="600" src="img/viewrecipe.png"><br>

### **Save Recipe and Save Recipe Ingredients**
<img width="600" src="img/saverecipe.png"><br>

### **View All Saved Recipes**
<img width="600" src="img/viewsavedrecipes.png"><br>

### **Display Shopping List by Recipe**
<img width="600" src="img/viewshoppinglist.png"><br>


## **Installation**
To run *Luna's Kitchen*:

Clone or fork the [repository](https://github.com/lunaxlam/lunaskitchen.git)

```
https://github.com/lunaxlam/lunaskitchen.git
```

In the project directory, create and activate a virtual environment:

```
virtualenv env
source env/bin/activate
```

Install the project dependencies:
```
pip3 install -r requirements.txt
```

Run the application:

```
python3 lunaskitchen.py
```

You can now access *Luna's Kitchen*! Happy cooking.