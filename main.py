import pandas as pd
import argparse
import matplotlib.pyplot as plt

#LAYER 4 DATABASE
def layer4database():
    df = pd.read_csv("US_Accidents_Dec21_updated.csv")
    return df

df = layer4database()

#LAYER 3 PERSISTENCE
def layer3state(stateFilter):
    def isStateMatching(string):
        return string == stateFilter
    filtered = df["State"].apply(isStateMatching)
    filteredDf = df[filtered]
    return filteredDf

#LAYER 2 BUSINESS
def layer2state(stateFilter, daystateFilter, weekdayFilter):
    stateDf = layer3state(stateFilter)
    if daystateFilter != "":
        def isDaystateMatching(string):
            return string == daystateFilter
        filtered = stateDf["Sunrise_Sunset"].apply(isDaystateMatching)
        stateDf = stateDf[filtered]
    
    if weekdayFilter != "":
        def isWeekdayMatching(string):
            return string == int(weekdayFilter)
        dates = pd.to_datetime(df["Start_Time"], format="ISO8601")
        tempDf = stateDf
        tempDf["DayOfWeek"] = dates.dt.dayofweek
        filtered = tempDf["DayOfWeek"].apply(isWeekdayMatching)
        stateDf = tempDf[filtered]

    return stateDf

#LAYER 1 PRESENTATION
def layer1graph(stateToGraph, hourBool, weekdayString, daystateString):
    dataframe = layer2state(stateToGraph, daystateString, weekdayString)
    if dataframe.empty:
        print("No data in dataframe. Please verify your parsed values!")
    else:
        print("Remember that Week Days are represented as numbers! (Monday = 0 ... Sunday = 6)")
        dates = pd.to_datetime(df["Start_Time"], format="ISO8601")
        if not hourBool:
            dataframe["DayOfWeek"] = dates.dt.dayofweek
            counted = dataframe["DayOfWeek"].value_counts(sort=False).sort_index()
            counted.plot.bar()
            plt.show()
        else:
            dataframe["HourOfWeek"] = dates.dt.hour
            counted = dataframe["HourOfWeek"].value_counts(sort=False).sort_index()
            counted.plot.bar()
            plt.show()


def layer1main():
    parser = argparse.ArgumentParser(prog = 'UsAccidents', description = 'Analysis of US accidents depending on location and time.')
    parser.add_argument('--State', required = True, type = str, help = "Enter state as string mandatory (Example: --State OH)")
    parser.add_argument('--Daystate', required = False, type = str, help = "Enter state of day (Day/Night)")
    parser.add_argument('--Hour', required = False, type = str, help = "Enter a letter to graph hours (y/n)")
    parser.add_argument('--Weekday', required = False, type = str, help = "Enter the weekday as number (Monday = 0 ... Sunday = 6)")

    inputs = parser.parse_args()
    hourBool = False
    weekdayBool = True

    if type(inputs.Hour) != type(None):
        if inputs.Hour.lower() == "y":
            hourBool = True
    if type(inputs.Weekday) != type(None):
        weekdayString = inputs.Weekday
    else:
        weekdayString = ""
    if type(inputs.Daystate) == type(None):
        daystateString = ""
    else:
        daystateString = inputs.Daystate

    layer1graph(inputs.State, hourBool, weekdayString, daystateString)
    #func(Inputs.Estado)

if __name__ == "__main__":
    layer1main()