##############################################
# Author: Sagar Suri
# Class: CCT 111, Fall 2019
# Analytical Visualization Project
#
# Description: This program selects data about measles
# immunication rates from the measles.csv file provided by the
# World Health Organization. 
# It can select data for years from (1980-2017) inclusive

##############################################


import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def a4():
    """
    The primary function for Part 1
    Prompts the user regarding what information they would like, 
    writes that information to a csv file, and finally prints out a report 

    Optional Visualization Code is commented out. Pictures of 4 visualizaitions
    are present in the accompanying essay.
    
    Parameter: n/a
    Returns: None
    """

    # Initial User Inputs 
    output_name = input("Please enter the name of the file you would like to output: ")
    year = input('Please select a year between 1980-2017 (inclusive): ')
    desired_income_level = input("Please enter an income level: (1-4 inclusive): ")

    # Dictionary for easy mapping
    income_dict = {"1": "WB_LI",
                    "2": "WB_LMI",
                    "3": "WB_UMI",
                    "4":"WB_HI"}

    # Keep track of averages for visualizations for Figure 1 and Figure 2
    avg_list = []

    # Error checking and converting the year into an index from 2-39 (to access the countries in the CSV)
    if year.isnumeric():
        if int(year) in range(1980, 2018):
            year_index = abs(int(year) - 2017) + 2
        else:
            print("\nThat year is not present in this dataset (1980-2017 inclusive only).\n")
            quit()
    else: 
        if year.lower() != "all":
            print("\nThe only possible non-numeric input is < all >. \n")
            quit()
    

    try: 
        # Open the file for writing based on user input 
        output_name = output_name + ".csv"
        with open(output_name, 'w', newline='') as csvfile:
            income_writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Open the file for reading (measles.csv)
            with open("measles.csv") as read_file:
                csv_reader = csv.reader(read_file, delimiter=',')
                
                
                # There are few cases to consider for writing:
                
                # Case 1: Desired year and income level are both specific (not all)
                if (desired_income_level in income_dict) and year.lower() != "all":
                    # skip heading because we're writing our own
                    next(csv_reader)
                    income_writer.writerow(['Country', 'World_Bank_Income_Level', str(year)])

                    for row in csv_reader:
                        # Write only the matching level for the specified year
                        if income_dict[desired_income_level] == row[1]:
                            income_writer.writerow([  row[0], row[1], row[year_index]  ])
                        

                # Case 2: ALL years for a specific income level
                elif (desired_income_level in income_dict) and (year.lower() == "all"):
                    # Copy the measles.csv heading since we're reporting all years
                    income_writer.writerow(next(csv_reader))
                    
                    for row in csv_reader:
                        # Write the whole row if the income level matches
                        if income_dict[desired_income_level] == row[1]:
                            income_writer.writerow(row)
                    

                # Case 3: Single year and all income levels
                elif desired_income_level.lower() == "all" and year.lower() != "all":
                    # skip heading because we're writing our own
                    next(csv_reader)
                    income_writer.writerow(['Country', 'World_Bank_Income_Level', str(year)])
                    
                    for row in csv_reader:
                        # Write every income level for the specified year
                        income_writer.writerow([  row[0], row[1], row[year_index]  ])
                        

                # Case 4: All years for all income levels
                else:
                    # Copy the measles.csv heading since we're reporting all years
                    income_writer.writerow(next(csv_reader))
                    
                    for row in csv_reader:
                        # Write the whole row
                        income_writer.writerow(row)
        
        # FINAL REPORT using Pandas to obtain statistics
        # Open the CSV we just created and wrote for the user
        df=pd.read_csv(output_name)
        print("\nFinal Report:")
      
        # If the data is for one year only:
        if year.lower() != "all":
            # using pandas to get count, averages, rows with min/max values
            count = df[year].count()
            average_percentage= round(df[year].mean(), 1)
            min_row = df.loc[df[year].idxmin()]
            max_row = df.loc[df[year].idxmax()]

            print("For the year {}, {} records:".format(year, count))
            print("Average percentage: ", average_percentage)
            print("Minimum (Country Percentage): ", min_row[0], int(min_row[2]))
            print("Maximum (Country Percentage): ", max_row[0], int(max_row[2]))
            print("\n")

        # Data for all years
        else: 
            for value in range(1980, 2018):
                year = str(value)
                # Same as first case but repeated for each year
                count = df[year].count()
                # count = df[year].count(axis=1, level=None, numeric_only=True)
                average_percentage= round(df[year].mean(), 1)
                avg_list.append(average_percentage)
                min_row = df.loc[df[year].idxmin()]
                max_row = df.loc[df[year].idxmax()]

                # For some reason min_row does not contain the correct minimums, so using these instead:
                minimum_percentage = df[year].min()
                maximum_percentage=df[year].max()

                print("For the year {}, {} records:".format(year, count))
                print("Average percentage: ", average_percentage)
                print("Minimum (Country Percentage): ", min_row[0], int(minimum_percentage))
                print("Maximum (Country Percentage): ", max_row[0], int(maximum_percentage))
                print("\n")
            #reset value of year for visualization
            year = "all"
        
        # PART 2 VISUALIZATION SECTION
        # This section contains optional functions for visualization
        
        plt.style.use('ggplot') # Plot theme 
       
        def figure1():
            '''
            Visualuzation for figure 1.
            Meant to be used for all years, all income levels input
            Parameter: n/a
            Returns: None
            '''

            title = ("Global Yearly Averages From 1980-2017")
            # set y axis to start at 0 and end at 100, no auto-adjustment
            plt.ylim(0, 100)
            # creative list for x-axis
            years = range(1980, 2018)
            # plot using the average list the program maintained.
            plt.plot(years, avg_list)

            #labels, titles, etc
            plt.xlabel('Years', fontsize=14)
            plt.ylabel('Percentages', fontsize=14)
            plt.xticks(fontsize=12, rotation=0)
            plt.title(title, fontsize=15)

            plt.show()

        def figure2():
            '''
            Visualuzation for figure 2.
            Meant to be used for all years, and a single income level (1-4)
            Parameter: n/a
            Returns: None
            '''

            title = ("Global Yearly Averages From 1980-2017: " + income_dict[desired_income_level])
            plt.ylim(0, 100)
            years = range(1980, 2018)
            plt.plot(years, avg_list)

            plt.xlabel('Years', fontsize=14)
            plt.ylabel('Percentages', fontsize=14)
            plt.xticks(fontsize=12, rotation=0)
            plt.title(title, fontsize=15)

            plt.show()
        
        def figure3():
            '''
            Visualuzation for figure 3.
            Meant to be used for all years, all income levels input
            Parameter: n/a
            Returns: None
            '''
            # Opening the measles file again
            with open("measles.csv") as read_file:
                csv_reader = csv.reader(read_file, delimiter=',')
                under = 0
                over = 0
                next(csv_reader)
                # Immunity Theshold is 93, just need how many countries are under/over 
                for row in csv_reader:
                    if int(row[year_index]) < 93:
                        under += 1
                    else: 
                        over += 1
            
            # Plot pie chart using the data from the loop above
            plt.title = ("Measles: How many countries hit the immunity threshold?")
            labels = 'Under Immunity Threshold', 'Over Immunity Threshold'
            sizes = [under, over]
            explode = (0, 0)  
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')
            plt.show()

  
        def figure4(country_input):
            '''
            Visualuzation for figure 4.
            Meant to be used for all years, all income levels input
            This can analyze averages for any country.

            Parameter: country_input
            Returns: None
            '''
            years = range(1980, 2018)
            percentage_list = []
            # Extracting data from one country from measles.csv
            with open("measles.csv") as read_file:
                csv_reader = csv.reader(read_file, delimiter=',')
                for row in csv_reader:
                    if row[0] == country_input:
                        i = 39
                        while i != 1:
                            # if there is data get it, otherwise add None
                            if row[i].isnumeric():
                                percentage_list.append(int(row[i]))
                            else: 
                                percentage_list.append(None)
                            i -= 1
            # Note: None was used because Nones are ignored in matplotlibs graph
            title = (country_input + " Immunization Rates Over Time")
            plt.ylim(0, 100)
            plt.plot(years, percentage_list)
            plt.xlabel('Years', fontsize=14)
            plt.ylabel('Percentages', fontsize=14)
            plt.xticks(fontsize=12, rotation=0)
            
            plt.title(title, fontsize=15)
            plt.show()
        
        # figure1()
        # figure2()
        # figure3()
        # figure4("Ukraine")
                       
    except FileNotFoundError:
        print("\nThe program could not open a CSV file. \n")

    
   


if __name__ == "__main__":
    a4()