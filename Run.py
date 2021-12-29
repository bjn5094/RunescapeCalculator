from SQL_LOAD import SQL_LOAD
from cs50 import get_string, SQL, get_int
from SQL_PREP import SQL_PREP
from SQL_ITERATE import SQL_ITERATE
import math

# Connect to my database
db = SQL("sqlite:///database.db")

# Ask for a Username so we know what character to look up on the High Scores
username = get_string("Username: ")

# Ask how many levels we are interested in gaining
levels_needed = get_int("How many levels do you need?: ")

# Execute SQL_LOAD function to refresh db with data from webpage
SQL_LOAD(username)

# Performs all my SQL commands to prepare the downloaded data and calculate/populate known values from my tables in database.
SQL_PREP()


# At this point in time, we could look at the Stats table and we would see all of our current skills and how long each would take to level.

# When I look at my results, I want to see each level up so this is just making that variable so I can increment later.
level_counter = 1

# At the end I want to sum up how long the levels will take, so I am making a variable and setting it to 0 here.
total_time = 0

# I want to loop through this function for every level that is required per the user.

for i in range(levels_needed):

    # Query the Stats database and pull the row (aka skill) that has the lowest "HoursToLevel" value by sorting by that and limiting to 1
    quickest = db.execute("SELECT * from Stats WHERE HoursToLevel IS NOT NULL ORDER BY HoursToLevel  LIMIT 1")

    if len(quickest) != 1:
        print("The data did not import properly from the High Scores.  Try again in a few minutes")
        exit()

    # From my row that is returned, pull out a few values that are of interest.
    quickestSkill = quickest[0]["Skill"]
    quickestHours = quickest[0]["HoursToLevel"]
    quickestExpNeeded = quickest[0]["ExpNeeded"]
    quickestNextLevel = quickest[0]["NextLevel"]
    quickestID = quickest[0]["ID"]

    # Print the information for that skill.
    print(f"{level_counter} - {quickestSkill}: {quickestHours} hours to gain {quickestExpNeeded} experience for Level {quickestNextLevel}.")

    # Increment my counter for the next iteration
    level_counter = level_counter + 1
    # Add the time to level that iteration to my running track of time
    total_time = total_time + quickestHours

    # Here I need to update my Stats and assume that the user leveled up that skill.  This allows me to iterate for the next quickest skill to level up.
    # Update the CurExp and CurLevel for that skill which are equal to the old NextLevel and NextExp values
    # Also need to increment NextLevel the way I have my iteration functions setup.
    db.execute("UPDATE STATS SET CurLevel = NextLevel, CurExp = NextExp, NextLevel = NextLevel + 1 WHERE ID = :tempID", tempID=quickestID)

    # We now have refreshed our information in our Stats page and it assumes we leveled up that skill
    # We need to now perform some more SQL transactions to do the same process as before to calculate the new time to level for every skill.

    # SQL_ITERATE just repeats the functions we did earlier, but excludes some of the commands that were setting up the table the first time.
    SQL_ITERATE()


final_time = round(total_time, 2)
# Display how long it will take to gain that many levels
print(f"It will take you a total time of {final_time} hours to gain {levels_needed} level(s).")