"""
Luna's Kitchen is a recipe generator program that uses the requests and 
BeautifulSoup4 modules from bs4 to webscrape data from the web to populate 
a recipe title, recipe description summary, link to recipe URL, and recipe 
details including serving size, ingredients list, and instructions list. 

Users also have the ability to save the recipe and URL to a dictionary and 
save recipe ingredients to a list; any saved results are written to a txt file.
"""
from bs4 import BeautifulSoup

import requests

import time  # to add some suspense

# A dictionary to store saved recipes
my_recipes = {}

# A list to store saved recipe ingredients
my_shopping_list = []


def draw_border():
    """create a pretty border"""

    print("-" * 45)
    print()


def welcome():
    """greet user"""

    print()
    print(("\U0001F319 " * 3) + " Welcome to Luna's Kitchen " + (" \U0001F319" * 3))  
    
    draw_border() 


def display_menu():
    """display navigation options to user"""

    print("\U0001F319 Menu Options:")
    print("[V]iew Saved Recipes")
    print("[G]et a Recipe")
    print("[D]isplay Shopping List")
    print("[Q]uit Kitchen")
    print()


def select_menu():
    """validate user input based on navigation options per display_menu()"""

    # display navigation options to user
    display_menu()

    # prompt user for menu selection and store input into variable
    select_menu = input("Enter menu option: \n> ").lower().strip()
    print()

    # validate input
    if select_menu == "v" or "view" or "g" or "get" or "d" or "display" or "q" or "quit":
        return select_menu
    else:
        print("Sorry, that wasn't an option. Try again.")
        print()


def say_goodbye():
    """thank and wish the user goodbye"""

    print(("\U0001F319 ") + " Thanks for visiting Luna's Kitchen! Goodbye. " + (" \U0001F319"))
    print("")


def get_URL():
    """
    Ask user for input to generate a recipe URL to allow the calling of requests 
    and BeautifulSoup. Use .find() method to generate and print to console 
    appropriate recipe title, summary, and URL link to recipe.
    
    Return: url
    """

    # create an ingredient variable to store user input
    ingredient = input("Enter an ingredient or recipe: \n> ").lower()

    # tokenize user input for later creation of final URL variable 
    ingredients = ingredient.split()  

    # create a query string base URl variable to store into the URL variable to later pass as argument for requests.get() method to scrape web page info
    # query string base URL will be used to pass through requests.get() method
    url = "https://www.allrecipes.com/search/results/?search="  

    # concatenate each list elements of the ingredient variable with the URL variable to generate the final URL variable
    for ingredient in ingredients: 
        url = url + ingredient + "+"

    # final query string URL variable
    url = f"{url}recipe"

    # display to user the updated URL
    print()
    print(f"Searching... ")
    print()

    # return url so when get_URL() function is called, the return result can be used in other functions
    return url


def find_all_recipes():
    """locate all recipe matches from get_URL() function by using BeautifulSoup methods to locate page elements and store results of findings into global variables to use in other functions"""

    # call the get_URL() function and assign return results to url variable to use in requests.get() method
    url = get_URL()

    # call the requests.get() method on the URL variable to initiate HTTP GET request
    result = requests.get(url) 

    # create a doc variable and call the BeautifulSoup function on the result variable to parse the HTML elements of the page
    doc = BeautifulSoup(result.text, "html.parser")  # fetches and parses the HTML content data as text

    # set a recipe_title variable as a global variable so display_recipes() and view_recipe()functions can call it later
    global recipe_title

    # create a recipe_title variable and call the .find_all() method on the doc variable to locate all matching titles of the recipe by analyzing tag and attribtue elements. Store the result in recipe_title
    recipe_title = doc.find_all("h3", class_="card__title") 

    # set a recipe_summary variable as a global variable so other functions can display_recipes() function and view_recipe() function can call it later
    global recipe_summary

    # create a recipe_summary variable and call the .find_all() method on the doc variable to locate all matching summaries of the recipe by analyzing tag and attribute elements. Store the result in recipe_summary
    recipe_summary = doc.find_all("div", class_="card__summary")

    # set a recipe_link variable as a global variable so display_recipes() and view_recipe() functions can call it later
    global recipe_link

    # create a recipe_link variable and call the .find_all() method on the doc variable to locate all matching links of the recipe by analyzing tag and attribute elements. Store the result in recipe_link
    recipe_link = doc.find_all("a", class_="card__titleLink", href=True)  # if using.find() method, add ["href"] at the end to retrieve only link

    # create "new_" lists to temporarily store by appending text only/no HTML element versions for each recipe info return
    new_recipe_title = []
    new_recipe_summary = []
    new_recipe_link = []

    # iterate through each recipe info link to return text and eliminate leading and trailing white spaces. append the results to the temporary lists and then reassign to original variables for consistency
    for recipe in recipe_title:
        recipe = recipe.get_text().strip().upper()  # .get_text() method allows us to pull only the text and no HTML tag elements; .strip() returns result without any leading or trailing whitespaces; .upper() returns the result in all uppercase
        new_recipe_title.append(recipe)
        recipe_title = new_recipe_title

    for summary in recipe_summary:
        summary = summary.get_text().strip()
        new_recipe_summary.append(summary)
        recipe_summary = new_recipe_summary

    for link in recipe_link:
        link = link.get('href')  # stores only the URL link
        new_recipe_link.append(link)
        recipe_link = new_recipe_link  # there are duplicate URLs that were appended to the recipe_link list variable that needs to be cleaned-up

    # use list comprehensive method to remove duplicates from recipe_link list variable and store non-duplicate entries in clean_recipe_link; reassign clean_recipe_link back to recipe_link when done
    clean_recipe_link = []

    [
        clean_recipe_link.append(link) for link in recipe_link
        if link not in clean_recipe_link
    ]

    recipe_link = clean_recipe_link


def display_recipes():
    """ask user for input to determine number of recipes to display along with corresponding recipe title, recipe summary, and recipe link"""

    while True:

        # draw a border to begin next display section
        draw_border()

        # get the total length of recipe_title() to determine max count for display
        total_recipe_count = len(recipe_title)

        # share display result to user
        print(f"Found: {total_recipe_count} Recipes")
        print()

        # set a display_count variable as a global variable for later use in find_recipe() function
        global display_count

        # ask user for input for how many recipes to display in console
        display_count = int(
            input(f"How many recipes would you like to view? Enter a number, 0 to {total_recipe_count}. \n> "))
        print()
        print()

        # if user indicates 0 recipes to display, exit
        if display_count == 0:
            break
        # elif user indicates >0 and <= count available for display, pass input in range() and display results
        elif display_count > 0 and display_count <= total_recipe_count:
            count = 1  # start Recipe # display at 1

            time.sleep(2)  # add some suspense

            for i in range(display_count):

                print(f"Recipe #{count}: {recipe_title[i]}")
                print()
                print(f"Summary: {recipe_summary[i]}")
                print()
                print(f"Link: {recipe_link[i]}")
                print()
                # draw_border() to begin next section of display
                draw_border()

                count += 1
            print()

            # call view_recipe() function
            view_recipe()

            break
        else:
            print("Sorry, that wasn't an option. Try again.")
            print()


def view_recipe():
    """The view_recipe function executes continuously until broken. It asks the user for input to determine if the recipe serving, ingredients, and instruction info should be printed to the console. Uses the same methods in get_recipe() to find recipe-specific elements"""

    # create an endless loop asking the following until the user quits the program; use while True
    while True:
        # ask user if they would like to view recipe details
        view_recipe = input("Would you like to view a specific recipe? Enter yes or no: \n> ").lower().strip()
        print()

        # if user says "no" to viewing recipe:
        # break to quit the loop and exit the function
        if view_recipe == "n" or view_recipe == "no":
            break
        # elif user says "yes" to viewing recipe:
        elif view_recipe == "y" or view_recipe == "yes":

            # call find_recipe() function
            find_recipe()

            break
        else:
            # let user know input was not an option
            print("Sorry, that wasn't an option. Try again.")
            print()


def find_recipe():
    """use BeautifulSoup methods to find specific recipe page elements and displays recipe title, recipe servings, recipe ingredients, and recipe instructions to user; invokes the save_recipe() function if meets condition"""

    while True:
        # ask user to confirm recipe number for look-up
        recipe_number = int(input(f"Please enter recipe number, between Recipe #1 to Recipe #{display_count}: \n> "))

        print()

        # validate user input
        if recipe_number > 0 and recipe_number <= display_count:

            # create a get_recipe variable
            global my_recipe_link

            # recipe_link index begin at 0, so need to -1 from input
            my_recipe_link = recipe_link[recipe_number - 1]

            # call the requests.get() on recipe_link to initiate HTTP GET request
            get_recipe = requests.get(my_recipe_link)

            # create a recipe_doc variable and call the BeautifulSoup function on the get_recipe variable to parse the HTML elements of the page
            recipe_doc = BeautifulSoup(get_recipe.text, "html.parser")

            # create a global my_recipe_title variable
            global my_recipe_title

            # use .find() method to locate the recipe title info of the recipe by analyzing tag and attribute elements. Store the result into my_recipe_title
            my_recipe_title = recipe_doc.find("h1", class_="headline heading-content elementFont__display").text

            # create a recipe_servings variable and use .find() method to locate the servings info of the recipe by analyzing tag and attribute elements. Store the result into recipe_servings
            recipe_servings = recipe_doc.find("div", class_="recipe-adjust-servings__original-serving").string

            # set a global recipe_ingredients variable that other functions can call within their local scope
            global my_recipe_ingredients

            # create a recipe_ingredients variable and use .find() method to locate the ingredients info of the recipe by analyzing tag and attribute elements. Store the result into ingredients
            my_recipe_ingredients = recipe_doc.find("fieldset", class_="ingredients-section__fieldset").text

            # ln 84 to 92 cleans up the output by removing unnecessary whitespace from raw website output

            my_recipe_ingredients = my_recipe_ingredients.split('         ') and my_recipe_ingredients.split('      ') and my_recipe_ingredients.split(' ') and my_recipe_ingredients.split('   ')

            update_ingredients = []

            for i in my_recipe_ingredients:
                if i != '':
                    update_ingredients.append(i)

            my_recipe_ingredients = update_ingredients

            # create an instructions variable and use .find() method to locate the instructions info of the recipe by analyzing tag and attribute elements. Store the result into instructions
            instructions = recipe_doc.find("fieldset", class_="instructions-section__fieldset").text

            # ln 102 to 117 cleans up the output by removing unnecessary whitespace from raw website output

            instructions = instructions.split('      ')

            update_instructions = []

            for i in instructions:
                if "Advertisement" in i:
                    i = i.split(" ")
                    i.remove("Advertisement")
                    i = " ".join(i)
                if "  Step" in i:
                    i = i.split("  ")
                    i = "".join(i)
                if i != '      ':
                    update_instructions.append(i)

            instructions = update_instructions

            # draw_border() to start next section of display
            draw_border()

            # print recipe title to user
            print(f"Recipe #{recipe_number}: {my_recipe_title.upper()}")
            print()

            # print recipe_servings to user
            print(" Servings:")
            print(recipe_servings)
            print()

            # print recipe_ingredients as individual elements on their own line to console
            for ingredient in my_recipe_ingredients:
                print(ingredient)
                print()
            
            print()

            # print instructions as individual elements on their own line to console
            for instruction in instructions:
                print(instruction)
                print()

            # draw a border to begin next section of display
            draw_border()

            # call save_recipe() function
            save_recipe()

            break
        else:
            # let user know that wasn't an option
            print("Sorry, that wasn't an option. Try again.")
            print()


def my_saved_recipes():
    """display the saved recipes from the user's current session in Luna's Kitchen"""

    # check to see if my_recipes dictionary is empty. if empty, let user know
    if my_recipes == {}:
        print("No recipes currently saved.")
    # else: display recipes in my_recipes dictionary
    else:
        # draw a border to begin next section of display
        draw_border()
        # print My Recipes header to user
        print("\U0001F4D6 My Recipes:")

        # print count of each key: value pair and display key: value pair in own line
        count = 1
        for recipe in my_recipes:
            print(f"{count}: {recipe}, {my_recipes[recipe]}")
            count += 1
    print()


def write_shopping_list():
    """write items in my_shopping_list to myshoppinglist.txt file"""

    # call the open method to create a txt file and use it for writing
    outfile = open("myshoppinglist.txt", "a")

    # for each item in my_shopping list, write each item to the txt file
    for item in my_shopping_list:
        outfile.write(item + "\n")

    # close the file
    outfile.close()


def save_ingredients():
    """add the ingredients from the most recently viewed recipe to my_shopping_list and also checks to see if the same recipe's ingredients were previously already added"""

    # create an endless loop asking the following until the user quits the program; use while True
    while True:

        # ask user if they would like to save recipe ingredients and store into my_shopping_list list variable
        save_ingredient = input("Would you like to save the recipe ingredients to your shopping list? Enter yes or no: \n> ").lower().strip()
        
        print()

        # if no then break
        if save_ingredient == "n" or save_ingredient == "no":
            break
        # elif check to see if ingredients already exist in shopping list: if they already exist, let user know; otherwise, append to my_shopping_list
        elif save_ingredient == "y" or save_ingredient == "yes":

            in_list = False

            for item in my_shopping_list:
                if item == my_recipe_title:
                    in_list = True

            if in_list == True:
                print("Recipe ingredients previously added to shopping list!")
                print()

            if in_list == False:
                my_shopping_list.append(my_recipe_title.upper())
                for ingredient in my_recipe_ingredients:
                    my_shopping_list.append(ingredient)
                my_shopping_list.append("")
                print(
                    f"\U0001F389 Success! {my_recipe_title.strip().upper()} recipe ingredients saved to shopping list."
                )

            # call the write_shopping_list() function
            write_shopping_list()

            break
        else:
            # let user know input was not an option
            print("Sorry, that wasn't an option. Try again.")
            print()
    
    print()


def write_recipe():
    """write saved recipes from save_recipe() to myrecipes.txt file"""

    # call the open method to create a file and use it for writing
    outfile = open("myrecipes.txt", "a")

    # for each key in my_recipes, write each key, key[value] to the txt file
    for recipe in my_recipes:
        outfile.write(f"{recipe}, {my_recipes[recipe]} \n")

    # close the file
    outfile.close()


def save_recipe():
    """save the most recently viewed recipe into my_recipes dictionary with the "recipe_title: recipe_link" as the "key: value" pair"""

    # create an endless loop asking the following until the user quits the program; use while True:
    while True:

        # ask user if they want to save recipe for later
        save_recipe = input("Would you like to save this recipe for later? Enter yes or no: \n> ").lower().strip()
        print()

        # if no - break
        if save_recipe == "n" or save_recipe == "no":
            break
        # elif - store recipe_title: recipe_link in my_recipes dictionary
        elif save_recipe == "y" or save_recipe == "yes":
            # check to see if recipe already saved in my_recipes
            found = False

            if my_recipe_title in my_recipes:
                found = True

            if found == True:
                print(
                    f"\U0001F389 {my_recipe_title.strip().upper()} already saved to your recipes."
                )
                print()
                break

            # if recipe not already saved, save recipe to my_recipe
            if found == False:
                my_recipes[my_recipe_title.strip()] = my_recipe_link.strip()

                print(f"\U0001F389 Success: {my_recipe_title.strip().upper()} saved to your recipes.")
                print()

                # call the write_recipe() function
                write_recipe()

                # call the save_ingredients() function
                save_ingredients()

                break
        else:
            # let user know input was not an option
            print("Sorry, that wasn't an option. Try again.")
            print()


def display_shopping_list():
    """display the current list items in my_shopping_list to the user"""

    # check to see if my_shopping_list list variable is empty; if so, let user know
    if my_shopping_list == []:
        print("No items currently in shopping list.")
        print()
    # else, print each item in my_shopping_list on own line in console
    else:
        # draw_border() to set-up next section of display
        draw_border()

        # print My Shopping List header to user
        print("\U0001F4DD My Shopping List:")
        print()
        # print each item in my_shopping_list
        for item in my_shopping_list:
            print(f"{item}")


def main():
    """start up the program and walk the user through the navigation options throughout the program."""

    # call the welcome() function to greet user
    welcome()

    # create an endless loop asking the following until the user quits the program; use while True:
    while True:

        # call the select_menu() function to display menu options and ask user for menu selection input; return function results into my_select_menu variable
        my_select_menu = select_menu()  # sets my_selection variable to whatever was stored in return value when select_menu() function was called

        if my_select_menu == "q" or my_select_menu == "quit":
            say_goodbye()
            break
        elif my_select_menu == "v" or my_select_menu == "view":
            my_saved_recipes()
        elif my_select_menu == "g" or my_select_menu == "get":
            find_all_recipes()
            display_recipes()
        elif my_select_menu == "d" or my_select_menu == "display":
            display_shopping_list()


# checks to see if name of file matches to main; if so then call the main() function. This allows other programs to import the other functions of this file for their program to use.
if __name__ == "__main__":
    main()