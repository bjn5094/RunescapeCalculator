# This function called SQL_PREP cleans up the data imported from the website and updates values that are either known or can be calculated.

from cs50 import SQL


def SQL_PREP():
    # connect to the database
    db = SQL("sqlite:///database.db")

    # Stats table contains the following columns:
    # ID - This is just a lookup column.  ID for each skill from 0 - 24
    # Skill - Known values.  Have a table called "SkillList" in my database which maps an ID to the Skill Number.  This order is constant
    # Rank - Imported from the highscores
    # CurLevel - Imported from the highscores
    # CurExp - Imported from the highscores
    # NextLevel - Imported from highscores by adding 1 to CurLevel
    # NextExp - Each level has a known value of total experience needed.  A table called LevelExp in my database stores this information.
    # ExpNeeded - The difference between NextExp and CurExp is how much experience is needed to get to the next level
    # SkillRate - There is a table called ExpRates that stores a value (Experiene Per Hour) for each of the 23 skills at each of the 99 skill levels
    # For example, if I look at the table, I can see that at Level 24 Fishing, I can expect to gain roughly 15,000 Experience per hour.
    # HoursToLevel - This is calculated by looking at how much experience is needed (ExpNeeded) and how much experience can be gained/hour at that level (SkillRate)

   # The ID column in Stats is NULL by default.  Here I am just updating the values by setting them equal to the temporary ID assigned to Skill when I was importing information
    db.execute("UPDATE Stats SET id = Skill")

    # This updates the Stats table and populates the proper "Skill" name by comparing to a SkillList lookup table in my database
    db.execute("UPDATE Stats SET Skill = (SELECT skill_Name FROM SkillList t2 WHERE t2.skill_ID = Stats.ID)")

    # This updates the Stats table and populates NextExp by looking for my next level number in my lookup table called LevelExp
    db.execute("UPDATE Stats SET NextExp = (SELECT CumExp FROM LevelExp t2 WHERE t2.Level = Stats.NextLevel) ")

    # This calculates how much Experience is Needed to gain a level by substracting CurExp from NextExp which are already known at this point
    db.execute("UPDATE Stats SET ExpNeeded = NextExp - CurExp")

    # This updates the Stats table with the SkillRate (Experience per Hour) that one can gain for each skill at it's current level.
    db.execute("UPDATE Stats SET SkillRate = (SELECT Rate FROM ExpRates t2 WHERE t2.RateLevel = Stats.CurLevel AND t2.RateSkill = Stats.Skill)")

    # Calculates how many hours is needed to level up each skill and stores that value
    db.execute("UPDATE Stats SET HoursToLevel = ROUND(ROUND(ExpNeeded, 2) / ROUND(SkillRate, 2), 2)")

