# After the GATHER_STATS() function, we have a list that with 24 length (Total + each of the 23 skills).  We need to load this list into our Stats table in SQL database.db

from GATHER_STATS import GATHER_STATS
from cs50 import SQL
import re


# Here we make a function called SQL_LOAD that takes our username as input so we can pass it to list()
def SQL_LOAD(username):

    # Configure CS50 Library to use SQLite database
    db = SQL("sqlite:///database.db")

    # We are removing any information from my Stats table as we are going to start with a blank canvas
    db.execute("DELETE FROM Stats")
    # Stats table contains the following columns:
    # ID
    # Skill
    # Rank
    # CurLevel
    # CurExp
    # NextLevel
    # NextExp
    # ExpNeeded
    # SkillRate
    # HoursToLevel

    # We are creating a new variable which is equal to our list from the GATHER_STATS function. (not sure if needed, but helpful during troubleshooting)
    output = GATHER_STATS(username)

    # Making a variable to keep track of rows for when I am inserting into SQL
    counter = 0

    # It is important to call out the structure of my list 'output' at this time.  Below are a few example rows
    #       Rank, Level, Experience.
    #       154758, 1924, 129932299                 This is my overall rank and sum of Levels/Experience of all 23 skills
    #       168040,99,13042245                      First line corresponds to the Attack Skill.  Rank 168,040 at level 99 with a bit over 13 million exp
    #       144521,72,940629                        I skipped a few lines, but here I am level 72 in Runecrafting with just under a million exp

    # Now I am going through each row in my output (aka my list of information)
    for row in output:

        # I am making a variable called count to count how many commas in each row.  If I have 2 commas for each row, it means I can parse out my 3 pieces of information
        count = row.count(',')

        # If I have 2 commas it means all my information is here
        if count == 2:
            # Make temporary variables for each piece of information from my row, by parsing between commas
            x_temp, y_temp, z_temp = row.split(',', 3)

            # Now I need to prep some values to load into SQL
            # Making a tempary variable for NextLevel which is the current level from my row + 1
            a_temp = int(y_temp) + 1
            # Making a variable for a temporary skill ID which is the row number.  I later override this with the actual Skill Name
            skill_temp = str(counter)
            # Increment my counter for next time
            counter = counter + 1

            # Now I am inserting into my SQL Table called Stats with all the information from the highscores
            db.execute("INSERT INTO Stats (Skill, Rank, CurLevel, CurExp, NextLevel) VALUES(:skill, :x, :y, :z, :a)",
                       skill=skill_temp,
                       x=x_temp,
                       y=y_temp,
                       z=z_temp,
                       a=a_temp)
        # If a row does not have two commas, it means something went wrong when downloading the data.  Prompt user to try again and exit script
        else:
            print("Something went wrong when downloading from the High Scores.  Try again in a few minutes. (High Scores unavailable)")
            # print(output)
            exit()