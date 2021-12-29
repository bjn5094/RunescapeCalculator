# This just repeats some of the SQL commands we did earlier, excluding ones that were setting up the initial table.

from cs50 import SQL


def SQL_ITERATE():
    # connect to the database
    db = SQL("sqlite:///database.db")

    # This updates the Stats table and populates NextExp by looking for my next level number in my lookup table called LevelExp
    db.execute("UPDATE Stats SET NextExp = (SELECT CumExp FROM LevelExp t2 WHERE t2.Level = Stats.NextLevel) ")

    # This calculates how much Experience is Needed to gain a level by substracting CurExp from NextExp which are already known at this point
    db.execute("UPDATE Stats SET ExpNeeded = NextExp - CurExp")

    # This updates the Stats table with the SkillRate (Experience per Hour) that one can gain for each skill at it's current level.
    db.execute("UPDATE Stats SET SkillRate = (SELECT Rate FROM ExpRates t2 WHERE t2.RateLevel = Stats.CurLevel AND t2.RateSkill = Stats.Skill)")

    # Calculates how many hours is needed to level up each skill and stores that value
    db.execute("UPDATE Stats SET HoursToLevel = ROUND(ROUND(ExpNeeded, 2) / ROUND(SkillRate, 2), 2)")

