from src.data_loader import load_data

#Function 1
'''
This function should be able to decipher the number that equals the "company" in the table that is companyName string and return that integer
in that row. Also test for edge cases, if that is empty or has no "company" in that column, it should return a value of 0.
'''
def getMissionCountByCompany(companyName: str) -> int:
    df = load_data()
    if df.empty or "Company" not in df.columns:
        return 0
    company_missions = df[df["Company"] == companyName]
    mission_count = len(company_missions)
    return mission_count

#Function 2
'''
This function should be able to get the percentage success rate of missions that were successful rounded to the nearest 2. Also check the edge 
cases like, if empty or has no company or missionstatus in columns or has no missions, should return value of 0.0.
'''
def getSuccessRate(companyName: str) -> float:
    df = load_data()
    if df.empty or "Company" not in df.columns or "MissionStatus" not in df.columns:
        return 0.0
    company_missions = df[df["Company"] == companyName]
    if company_missions.empty:
        return 0.0
    successful_missions = company_missions[company_missions["MissionStatus"] == "Success"]
    success_rate = (len(successful_missions) / len(company_missions)) * 100
    return round(success_rate, 2)

#Function 3
'''
This function should be able to get the mission names as a list by sorting the missinos by date chronologically. This should be done after 
filtering missions into dates that are range inclusive. Also, edge cases like, if empty or no date in columns or missions not in columns, should
return no list. 
'''
def getMissionsByDateRange(startDate: str, endDate: str) -> list:
    df = load_data()
    if df.empty or "Date" not in df.columns or "Mission" not in df.columns:
        return []
    date_filtered = df[(df["Date"] >= startDate) & (df["Date"] <= endDate)]
    missions_sorted = date_filtered.sort_values("Date")
    missions_names = missions_sorted["Mission"].tolist()
    return missions_names

#Function 4 
'''
This function should be able to convert tables to a tuples list of only the top n companies sorting by highest mission count and alphabetically
by company name. The table should be converted to two columns, company name and mission count. Edge cases like, empty or no company in columns or n is less
than or equal to 0.
'''
def getTopCompaniesByMissionCount(n: int) -> list:
    df = load_data()
    if df.empty or "Company" not in df.columns or n<=0:
        return []
    mission_counts = df["Company"].value_counts()
    mission_counts = mission_counts.reset_index()
    mission_counts.columns = ["Company", "MissionCount"]
    mission_counts = mission_counts.sort_values( by = ["MissionCount", "Company"], ascending=[False, True])
    top_companies = mission_counts.head(n)
    return list(top_companies.itertuples(index=False, name=None))

#Function 5
'''
This function should be able to get a complete dictionary of mission status counts. Edge cases should be checked, empty, or if the mission status
is in the columns or not. 
'''
#returns dictionary of mission statuses
def getMissionStatusCount() -> dict:
    df = load_data()
    if df.empty or "MissionStatus" not in df.columns:
        return {"Success": 0, "Failure": 0, "Partial Failure": 0, "Prelaunch Failure": 0}
    status_counts = df["MissionStatus"].value_counts().to_dict()
    required_statuses = ["Success", "Failure", "Partial Failure", "Prelaunch Failure"]
    for status in required_statuses:
        if status not in status_counts:
            status_counts.setdefault(status, 0)
    return status_counts

#Function 6
'''
This function should filter the missions launched in given year and match to the rows. Check the edge cases as well which are, empty or
if Date is not in the columns, should get 0.
'''
def getMissionsByYear(year: int) -> int:
    df = load_data()
    if df.empty or "Date" not in df.columns:
        return 0
    year_missions = df[df["Date"].dt.year == year]
    mission_count = len(year_missions)
    return mission_count

#Function 7
'''
This function should be able to get the most used rocket by checking the usage count and show alphabetically. Edge cases like empty and rocket in the columns 
needs to be checked.
'''
def getMostUsedRocket() -> str:
    df = load_data()
    if df.empty or "Rocket" not in df.columns:
        return ""
    rocket_counts = df["Rocket"].value_counts()
    max_usage = rocket_counts.max()
    most_used = rocket_counts[rocket_counts == max_usage].index.tolist()
    most_used_sorted = sorted(most_used)
    return most_used_sorted[0]

#Function 8
'''
This function should be able to get the percent of average missions per year by checking the mission launched in a year range and then count the 
years for it. The edge cases as well should be checked including, empty or if date is in columns or if end year is smaller than the start year. 
'''
def getAverageMissionsPerYear(startYear: int, endYear: int) -> float:
    df = load_data()
    if df.empty or "Date" not in df.columns or endYear < startYear:
        return 0.0
    filtered = df [(df["Date"].dt.year >= startYear) & (df["Date"].dt.year <= endYear)]
    total_years = endYear - startYear + 1
    if total_years <= 0:
        return 0.0
    average = len(filtered) / total_years
    return round(average, 2)

