import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, day, time of day, and bike type to analyze. not case sensitive

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) time_of_day - preferred time of day to filter by, or "all" to apply no time filter
        (str) bike_type - type of bike to filter by, or "all" to apply no bike type filter
    """
    print("Hello! Let's explore some US bikeshare data for Analysis!")
    
    city = input("Enter city name (chicago, new york city, washington): ").lower()
    while city not in CITY_DATA:
        city = input("Invalid city name. Please enter again (chicago, new york city, washington): ").lower()

    month = input("Enter month (all, january, february, ... , june): ").lower()
    day = input("Enter day of week (all, monday, tuesday, ... sunday): ").lower()
    time_of_day = input("Enter time of day (all, morning, afternoon, evening, night): ").lower()
    bike_type = input("Enter bike type (all, standard, electric): ").lower()

    print('-'*40)
    return city, month, day, time_of_day, bike_type

def load_data(city, month, day, time_of_day, bike_type):
    """
    Loads data for the specified city and filters by month, day, time of day, and bike type if applicable. not case sensitive.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) time_of_day - preferred time of day to filter by, or "all" to apply no time filter
        (str) bike_type - type of bike to filter by, or "all" to apply no bike type filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month, day, time of day, and bike type
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    if time_of_day != 'all':
        if time_of_day == 'morning':
            df = df[(df['hour'] >= 6) & (df['hour'] < 12)]
        elif time_of_day == 'afternoon':
            df = df[(df['hour'] >= 12) & (df['hour'] < 18)]
        elif time_of_day == 'evening':
            df = df[(df['hour'] >= 18) & (df['hour'] < 24)]
        elif time_of_day == 'night':
            df = df[(df['hour'] >= 0) & (df['hour'] < 6)]

    if bike_type != 'all' and 'Bike Type' in df.columns:
        df = df[df['Bike Type'].str.lower() == bike_type]

    return df

def display_raw_data(df):
    """Displays raw data 5 lines at a time upon user request."""
    start_loc = 0
    while True:
        display = input("Do you want to see 5 lines of raw data? Enter yes or no: ").lower()
        if display == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
        else:
            break

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].mode()[0]
    print(f'Most Common Month: {most_common_month}')

    most_common_day = df['day_of_week'].mode()[0]
    print(f'Most Common Day of Week: {most_common_day}')

    most_common_start_hour = df['hour'].mode()[0]
    print(f'Most Common Start Hour: {most_common_start_hour}')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    print(f'Most Commonly Used Start Station: {most_common_start_station}')

    most_common_end_station = df['End Station'].mode()[0]
    print(f'Most Commonly Used End Station: {most_common_end_station}')

    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'Most Frequent Combination of Start Station and End Station Trip: {most_common_trip}')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print(f'Total Travel Time: {total_travel_time} seconds')

    mean_travel_time = df['Trip Duration'].mean()
    print(f'Mean Travel Time: {mean_travel_time} seconds')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(f'Counts of User Types:\n{user_types}')

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f'\nCounts of Gender:\n{gender_counts}')

    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f'\nEarliest Year of Birth: {earliest_year}')
        print(f'Most Recent Year of Birth: {most_recent_year}')
        print(f'Most Common Year of Birth: {most_common_year}')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def main():
    while True:
        city, month, day, time_of_day, bike_type = get_filters()
        df = load_data(city, month, day, time_of_day, bike_type)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":

    main()
