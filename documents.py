# NYC Taxi Reference Documents
# These will be embedded and used for RAG

DOCUMENTS = [
    {
        "title": "NYC Taxi Fare Structure",
        "content": """
        NYC taxi fares are calculated based on distance and time.
        The base fare is $2.50 when the meter starts.
        The rate is $0.50 per 1/5 mile or $0.50 per 60 seconds in slow traffic.
        There is a $0.50 MTA State Surcharge on all trips.
        There is a $0.30 Improvement Surcharge on all trips.
        Peak hour surcharge of $1.00 applies Monday to Friday 4pm to 8pm.
        Overnight surcharge of $0.50 applies 8pm to 6am daily.
        Tolls are added to the fare automatically.
        Tips are not included in the meter fare.
        Credit card tips average around $2.71 per trip.
        Cash tips are given directly to driver and not recorded.
        """
    },
    {
        "title": "NYC Borough Guide",
        "content": """
        New York City has five boroughs.
        Manhattan is the most densely populated borough and generates highest taxi revenue.
        Manhattan has the most taxi pickups and dropoffs due to business district.
        Brooklyn is the most populated borough with 2.6 million residents.
        Brooklyn trips are often longer distance than Manhattan trips.
        Queens is the largest borough by area and home to JFK and LaGuardia airports.
        Airport trips from Queens generate higher fares due to longer distances.
        The Bronx is the northernmost borough and has fewer taxi trips.
        Staten Island is the least populated borough connected by ferry.
        Staten Island has very few yellow taxi trips due to distance.
        """
    },
    {
        "title": "NYC Taxi Payment Analysis",
        "content": """
        In 2015 cash was the dominant payment method for NYC taxis.
        Cash payments represented 62% of all taxi trips.
        Credit card payments represented 38% of all taxi trips.
        Cash average fare was $13.51 per trip.
        Credit card average fare was $12.28 per trip.
        Cash riders tend to take slightly longer trips on average.
        Credit card tips averaged $2.71 per trip.
        Cash tips are not recorded in the system.
        Disputed trips represent less than 0.1% of all trips.
        No charge trips represent about 0.3% of all trips.
        No charge trips include driver errors and VIP rides.
        Credit card tips are higher because passengers are prompted
        on the card machine to add a tip automatically.
        The card machine suggests tip percentages of 20, 25 or 30 percent.
        This automatic prompting leads to more consistent tipping.
        Cash riders give tips directly to driver without any prompting.
        No suggestion means cash riders tip less consistently.
        This is why credit card tips average $2.71 while cash tips
        are rarely recorded in the system.
        Many cash riders do tip but the amount is not captured digitally.
        Credit card payment makes tipping easier and more automatic.
        Studies show digital payment prompts increase tipping behavior.
        """
    },
    {
        "title": "NYC Taxi Trip Patterns",
        "content": """
        NYC taxis are busiest between 8pm and 10pm on weekdays.
        The peak hour for taxi trips is 9pm with over 61000 trips.
        The quietest time is 5am with only 11000 trips per hour.
        Morning rush hour shows increased demand from 7am to 9am.
        Evening rush hour shows peak demand from 6pm to 10pm.
        Average trip duration is 15.23 minutes.
        Average trip distance is 3.80 miles.
        Most NYC taxi trips are short distance under 5 miles.
        Long distance trips over 10 miles represent airport and outer borough trips.
        Weekend patterns differ from weekday with later peak hours.
        """
    },
    {
        "title": "NYC Taxi Data Overview",
        "content": """
        The NYC taxi dataset contains real trip data from 2015.
        Total trips in the dataset is 993708 after data cleaning.
        Original raw data contained 1000660 trips before cleaning.
        Data cleaning removed trips with zero fare amount.
        Data cleaning removed trips with zero passenger count.
        Data cleaning removed trips with zero distance.
        Total revenue from all trips is approximately 16 million dollars.
        Average fare per trip is 13.05 dollars.
        The data covers yellow taxi trips in New York City.
        Yellow taxis can pick up passengers anywhere in NYC.
        """
    }
]