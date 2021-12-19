import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
      try:
        city = input("\nPlease pick which city you would like to explore(Chicago, New York City, or Washington): \n")
        if city.lower() in CITY_DATA.keys():
          break
        else:
          print("That is not a valid option, please try again.\n")
      except:
        print("That is not a valid input, please try again.\n")

    # TO DO: get user input for month (all, january, february, ... , june)
    monthlist = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    while True:
      try:
        month = input("\nWhat month would you like information from? (January through June, or type all for all months): \n").lower()
        if month.title() in monthlist:
          break
        else:
          print("That is not a valid option, please choose a month between January and June, or select all: \n")
      except:
        print("That is not a valid input, please try again.\n")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    daylist = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']
    while True:
      try:
        day = input("\nWhat day of the week would you like information from? (Select a day or type all for all days): \n").lower()
        if day.title() in daylist:
          break
        else:
          print("That is not a valid option, please choose a day of the week, or type all for all days: \n")
      except:
        print("That is not a valid input, please try again.\n")

    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print("The most popular month for travel is: {}".format(common_month))

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The most popular day of the week for travel is: {}".format(common_day))

    # TO DO: display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print("The most popular hour for travel is: {}".format(common_start_hour))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("Most common start station is: {}".format(common_start))

    # TO DO: display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("Most common end station is: {}".format(common_end))

    # TO DO: display most frequent combination of start station and end station trip
    most_common_combination = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).head(1)
    print("Most common combination of Start and End Station is: \n{}".format(most_common_combination))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: {}'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average travel time is: {}'.format(mean_travel_time))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    num_user_types = df['User Type'].value_counts()
    print('Number of user types: \n{}\n'.format(num_user_types))

    # TO DO: Display counts of gender
    try:
      num_gender = df['Gender'].value_counts()
      print('Number of uses from each gender: \n{}\n'.format(num_gender))

      # TO DO: Display earliest, most recent, and most common year of birth
      earliest_year = df['Birth Year'].min()
      print('Earliest year: {}'.format(earliest_year))

      most_recent_year = df['Birth Year'].max()
      print('Most recent year: {}'.format(most_recent_year))

      most_common_year = df['Birth Year'].mode()[0]
      print('Most common year: {}'.format(most_common_year))
    except:
      print('No gender or birth year information for this city.')

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)

def display_raw(df):
    # Ask if the user wants to see raw data then display 5 lines at a time
    step = 0
    choice = input('Would you like to view the raw data? Please choose Yes or No:\n').lower()
    # Print 5 lines of raw data if the user asks for it
    while True:
      if choice == 'yes':
        print(df.head(5))
        # Ask if the user would like to see more data, print the next 5 lines
        while True:
            choice = input('Would you like to see more data? Please choose Yes or No:\n').lower()
            if choice == 'yes':
              step += 5
              print(df[step:step+5])
            elif choice == 'no':
              break
            else:
              print('That is not a valid input, please try again.\n')
      elif choice == 'no':
          break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
