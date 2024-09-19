import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import seaborn as sns
from sklearn.linear_model import LinearRegression

# HERE ARE ALL THE COLUMNS FROM Mens_Barebow IN ORDER
# Match ID, Archer 1 Name, Archer 2 Name, Archer 1 Score, Archer 2 Score, Archer 1 Xs, Archer 2 Xs, Archer 1 Target, Archer 2 Target, Archer 1 Riser, Archer 2 Riser, Winner, Year, Notes

# Load the data
def load_data():
    return pd.read_csv('Mens_Barebow.csv')

#average points per arrow
def plot_average_points_per_year(df):
    # Add Match Number column for each year
    df['Match Number'] = df.groupby('Year').cumcount() + 1
    
    # Calculate the average points per arrow
    df['Average Points per Arrow'] = (df['Archer 1 Score'] + df['Archer 2 Score']) / 24
    
    # Define the maximum match number as 7
    max_match_number = 7

    plt.figure(figsize=(10, 6))

    for year, data in df.groupby('Year'):
        num_matches = data['Match Number'].max()
        
        # Create a dictionary for scaling match numbers so the last match is at 7
        match_scale = {i: max_match_number - (num_matches - i) for i in range(1, num_matches + 1)}
        
        # Apply the scaling
        scaled_match_number = data['Match Number'].map(match_scale)
        
        plt.plot(scaled_match_number, data['Average Points per Arrow'], marker='o', label=f"{year}")

    plt.title('Average Points per Arrow per Match')
    plt.xlabel('Match')
    plt.ylabel('Average Points per Arrow')
    plt.xticks(range(1, max_match_number + 1))  # Ensure x-axis has labels 1 to 7
    plt.ylim(7, 10)  # Set y-axis range from 7 to 10
    plt.legend(title="Year")
    plt.grid(True)
    plt.show()

# Function to create the stacked line chart for total Xs per match per year
def plot_total_xs_per_year(df):
    # Add Match Number column for each year
    df['Match Number'] = df.groupby('Year').cumcount() + 1
    # Calculate the total Xs per match
    df['Total Xs'] = df['Archer 1 Xs'] + df['Archer 2 Xs']

    # Define the maximum match number as 7
    max_match_number = 7

    plt.figure(figsize=(10, 6))

    for year, data in df.groupby('Year'):
        num_matches = data['Match Number'].max()
        
        # Create a dictionary for scaling match numbers so the last match is at 7
        match_scale = {i: max_match_number - (num_matches - i) for i in range(1, num_matches + 1)}
        
        # Apply the scaling
        scaled_match_number = data['Match Number'].map(match_scale)
        
        plt.plot(scaled_match_number, data['Total Xs'], marker='o', label=f"{year}")

    # Set the title, labels, and grid
    plt.title("Total Xs per Match")
    plt.xlabel('Match #')
    plt.ylabel('Total Xs')
    plt.xticks(range(1, max_match_number + 1))  # Ensure x-axis has labels 1 to 7
    plt.ylim(0, 8)  # Set y-axis range from 0 to 8
    plt.legend(title="Year")
    plt.grid(True)
    
    # Show the plot
    plt.show()
# Bar chart with top 10 single performances (x-axis: archer name and the year in parenthesis, y-axis: average score per arrow)
def plot_top_performances(df):
    # Calculate average score per arrow for both archers
    df['Archer 1 Average Score per Arrow'] = df['Archer 1 Score'] / 12.0
    df['Archer 2 Average Score per Arrow'] = df['Archer 2 Score'] / 12.0
    
    # Create a DataFrame to hold the archer performances
    performances = pd.DataFrame({
        'Archer Name': pd.concat([df['Archer 1 Name'], df['Archer 2 Name']]),
        'Year': pd.concat([df['Year'], df['Year']]),
        'Average Score per Arrow': pd.concat([df['Archer 1 Average Score per Arrow'], df['Archer 2 Average Score per Arrow']])
    })

    # Sort by the average score per arrow in descending order and take the top 10
    top_performances = performances.sort_values(by='Average Score per Arrow', ascending=False).head(10)
    
    # Create labels for the x-axis (archer name and year)
    top_performances['Label'] = top_performances['Archer Name'] + ' (' + top_performances['Year'].astype(str) + ')'
    
    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(top_performances['Label'], top_performances['Average Score per Arrow'], color='skyblue')

    # Add a horizontal dashed line at y = 8.66 for competition average
    #TODO: FIX LABEL NOT SHOWING
    plt.axhline(y=8.66, color='red', linestyle='--', label='Competition Average (8.66)')
    
    # Set plot details
    plt.title('Top 10 Single Performances')
    plt.ylabel('Average Score per Arrow')
    plt.ylim(8, 10)  # Set y-axis range from 7 to 10
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to fit everything
    
    # Show the plot
    plt.show()

#Win percentage visual by riser brand, also mentioning how many total (unique) archers each has sponsored (ex: (percentage/progress chart) company X has won 25/54. so the circle is fillled to 46.2%). ONE CHART PER COMPANY.
def plot_win_percentage_by_riser(df):
    # Combine Archer 1 and Archer 2 data into one DataFrame
    riser_data = pd.concat([
        df[['Archer 1 Riser', 'Archer 1 Name', 'Winner']].rename(columns={'Archer 1 Riser': 'Riser', 'Archer 1 Name': 'Archer', 'Winner': 'Is Winner'}),
        df[['Archer 2 Riser', 'Archer 2 Name', 'Winner']].rename(columns={'Archer 2 Riser': 'Riser', 'Archer 2 Name': 'Archer', 'Winner': 'Is Winner'})
    ])

    # Apply row-wise comparison to determine if the archer is the winner
    riser_data['Is Winner'] = riser_data.apply(lambda row: row['Is Winner'] == row['Archer'], axis=1)

    # Group by Riser to calculate win percentage and count unique archers
    riser_stats = riser_data.groupby('Riser').agg(
        Wins=('Is Winner', 'sum'),  # Count the number of wins
        Total_Matches=('Is Winner', 'count'),  # Count the total number of matches for each riser
        Unique_Archers=('Archer', 'nunique')  # Count the number of unique archers
    )
    
    # Calculate win percentage
    riser_stats['Win Percentage'] = (riser_stats['Wins'] / riser_stats['Total_Matches']) * 100
    
    # Plot a circular progress chart for each riser
    for riser, stats in riser_stats.iterrows():
        # Create a figure
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'aspect': 'equal'})
        
        # Create the progress chart
        win_percentage = stats['Win Percentage']
        wedges, texts = ax.pie([win_percentage, 100 - win_percentage], startangle=90, colors=['skyblue', 'lightgray'], wedgeprops={'width': 0.4})

        # Add the text at the center of the pie
        plt.text(0, 0, f'{riser}\n{win_percentage:.1f}%', ha='center', va='center', fontsize=16)

        # Add the title mentioning the number of unique archers
        plt.title(f'{riser}: {int(stats["Unique_Archers"])} different archers\n{int(stats["Wins"])}/{int(stats["Total_Matches"])} matches won', fontsize=14)

        # Display the chart
        plt.show()


# Bar chart with top 5 best individual performers across all matches
def plot_best_individual_performers(df):
    # Calculate average score per arrow for both archers
    df['Archer 1 Average Score per Arrow'] = df['Archer 1 Score'] / 12.0
    df['Archer 2 Average Score per Arrow'] = df['Archer 2 Score'] / 12.0
    
    # Combine data for both archers into one DataFrame
    performances = pd.concat([
        df[['Archer 1 Name', 'Year', 'Archer 1 Average Score per Arrow']].rename(columns={'Archer 1 Name': 'Archer', 'Archer 1 Average Score per Arrow': 'Average Score per Arrow'}),
        df[['Archer 2 Name', 'Year', 'Archer 2 Average Score per Arrow']].rename(columns={'Archer 2 Name': 'Archer', 'Archer 2 Average Score per Arrow': 'Average Score per Arrow'})
    ])
    
    # Group by archer and calculate the overall average score per arrow across all matches
    average_scores = performances.groupby('Archer').agg(
        Average_Score=('Average Score per Arrow', 'mean'),  # Average score across all matches
        Years=('Year', lambda x: ', '.join(map(str, sorted(set(x)))))  # Collect all years in parentheses
    )
    
    # Sort by average score and take the top 5
    top_performers = average_scores.sort_values(by='Average_Score', ascending=False).head(5)
    
    # Create labels for the x-axis (archer name with years in parentheses)
    top_performers['Label'] = top_performers.index + ' (' + top_performers['Years'] + ')'
    
    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(top_performers['Label'], top_performers['Average_Score'], color='lightgreen')
    
    #TODO: FIX LABEL NOT SHOWING
    plt.axhline(y=8.66, color='red', linestyle='--', label='Competition Average (8.66)')
    
    # Set plot details
    plt.title('Top 5 Best Individual Performers')
    plt.ylabel('Average Score per Arrow')
    plt.ylim(8.2, 10)  # Set y-axis range to match typical scores
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for readability
    plt.tight_layout()  # Adjust layout
    
    # Show the plot
    plt.show()

# Function to create bar chart for top 10 most accurate performers aka the most Xs per match AVERAGE (minimum 2 matches)
def plot_top_accurate_performers(df):
    # Calculate total Xs for both archers
    df['Archer 1 Total Xs'] = df['Archer 1 Xs']
    df['Archer 2 Total Xs'] = df['Archer 2 Xs']
    
    # Combine data for both archers into one DataFrame
    xs_data = pd.concat([
        df[['Archer 1 Name', 'Year', 'Archer 1 Total Xs']].rename(columns={'Archer 1 Name': 'Archer', 'Archer 1 Total Xs': 'Total Xs'}),
        df[['Archer 2 Name', 'Year', 'Archer 2 Total Xs']].rename(columns={'Archer 2 Name': 'Archer', 'Archer 2 Total Xs': 'Total Xs'})
    ])
    
    # Group by archer and calculate the average Xs per match and the number of matches
    accuracy_stats = xs_data.groupby('Archer').agg(
        Average_Xs=('Total Xs', 'mean'),
        Match_Count=('Total Xs', 'size')
    )
    
    # Filter out archers with fewer than 2 matches
    accuracy_stats = accuracy_stats[accuracy_stats['Match_Count'] >= 2]
    
    # Sort by average Xs per match in descending order and take the top 10
    top_accurate_performers = accuracy_stats.sort_values(by='Average_Xs', ascending=False).head(10)
    
    # Create labels for the x-axis (archer name and year)
    top_accurate_performers['Label'] = top_accurate_performers.index
    
    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(top_accurate_performers['Label'], top_accurate_performers['Average_Xs'], color='goldenrod')
    
    #TODO: FIX LABEL NOT SHOWING
    plt.axhline(y=1.375, color='red', linestyle='--', label='Competition Average (1.375)')
    
    # Set plot details
    plt.title('Top 10 Most Accurate Performers')
    plt.ylabel('Average Xs per Match')
    plt.xlabel('Archer')
    plt.ylim(0, 3)  # Set y-axis range to match typical Xs scores
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for readability
    plt.tight_layout()  # Adjust layout
    
    # Show the plot
    plt.show()


# Function to create a bar chart for archers with top 10 most matches played
def plot_top_match_counts(df):
    # Combine data for both archers into one DataFrame, treating each as a separate row
    match_counts = pd.concat([
        df[['Archer 1 Name']].rename(columns={'Archer 1 Name': 'Archer'}),
        df[['Archer 2 Name']].rename(columns={'Archer 2 Name': 'Archer'})
    ])
    
    # Group by archer and count the number of matches played
    match_counts = match_counts.groupby('Archer').size().reset_index(name='Match Count')
    
    # Sort by match count in descending order and take the top 10
    top_match_counts = match_counts.sort_values(by='Match Count', ascending=False).head(9)
    
    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(top_match_counts['Archer'], top_match_counts['Match Count'], color='coral')
    
    # Set plot details
    plt.title('Top Archers with Most Matches')
    plt.ylabel('Number of Matches')
    plt.xlabel('Archer')
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for readability
    plt.tight_layout()  # Adjust layout
    
    # Show the plot
    plt.show()

# top 3 longest winning streaks
def plot_top_winning_streaks(df):
    # Create a DataFrame to hold each archer's winning streaks
    streaks = []

    # Iterate over each archer and find their winning streaks
    for archer in pd.concat([df['Archer 1 Name'], df['Archer 2 Name']]).unique():
        # Create a boolean column indicating if the archer won the match
        df['Is_Winner'] = df['Winner'] == archer
        
        # Identify the winning streaks
        df['Streak'] = (df['Is_Winner'] != df['Is_Winner'].shift()).cumsum()
        streak_data = df[df['Is_Winner']]
        
        # Count the length of each streak for this archer
        streak_lengths = streak_data.groupby('Streak').size()
        streaks.extend([(archer, length) for length in streak_lengths])

    # Convert the list to a DataFrame
    streaks_df = pd.DataFrame(streaks, columns=['Archer', 'Streak Length'])
    
    # Find the top 3 longest winning streaks
    top_streaks = streaks_df.groupby('Archer').agg(
        Top_Streak=('Streak Length', 'max'),
        Count_Streaks=('Streak Length', 'size')
    ).sort_values(by='Top_Streak', ascending=False).head(3)
    
    # Create labels for the x-axis (archer name and streak length)
    top_streaks['Label'] = top_streaks.index + ' (' + top_streaks['Top_Streak'].astype(str) + ' matches)'
    
    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(top_streaks['Label'], top_streaks['Top_Streak'], color='royalblue')
    
    # Set plot details
    plt.title('Top 3 Longest Winning Streaks')
    plt.ylabel('Streak Length (Number of Matches)')
    plt.xlabel('Archer')
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for readability
    plt.tight_layout()  # Adjust layout
    
    # Show the plot
    plt.show()


# Function to calculate and plot the percentage of returning archers
def plot_returning_archers(df):
    # Combine Archer 1 and Archer 2 data into one DataFrame
    archers_data = pd.concat([
        df[['Archer 1 Name', 'Year']].rename(columns={'Archer 1 Name': 'Archer'}),
        df[['Archer 2 Name', 'Year']].rename(columns={'Archer 2 Name': 'Archer'})
    ])

    # Get a list of all unique archers and the years they competed
    archers_years = archers_data.groupby('Archer')['Year'].apply(set).reset_index()
    
    # Determine returning archers (those who competed in more than one year)
    archers_years['Returning'] = archers_years['Year'].apply(lambda years: len(years) > 1)
    
    total_archers = len(archers_years)
    returning_archers = archers_years['Returning'].sum()

    # Calculate the percentage of returning archers
    percentage_returning = (returning_archers / total_archers) * 100

    # Plot a circular progress chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'aspect': 'equal'})
    
    # Create the progress chart
    wedges, texts = ax.pie([percentage_returning, 100 - percentage_returning], startangle=90,
                           colors=['lightgreen', 'lightgray'], wedgeprops={'width': 0.4})

    # Add the text at the center of the pie
    plt.text(0, 0, f'{percentage_returning:.1f}%\nReturning Archers', ha='center', va='center', fontsize=16)

    # Add the title
    plt.title(f'Total Archers: {total_archers}\nReturning Archers: {returning_archers}', fontsize=14)

    # Display the chart
    plt.show()

# Helper function to extract the last name, handling suffixes with regex
def extract_last_name(name):
    # Split the name by spaces
    name_parts = name.split()
    
    # Check if the last part is a Roman numeral (e.g., "III", "IV")
    if re.match(r'^(I|II|III|IV|V|VI|VII|VIII|IX|X)$', name_parts[-1]):
        # If it is, use the second-to-last part as the last name
        return name_parts[-2]
    else:
        # Otherwise, use the last part as the last name
        return name_parts[-1]

def plot_top_matches_by_points(df):
    # Calculate average score per arrow for each match (for both archers combined)
    df['Average Score per Arrow'] = (df['Archer 1 Score'] + df['Archer 2 Score']) / 24.0
    
    # Create a label for each match by concatenating the last names of Archer 1 and Archer 2, and the year
    df['Match Label'] = df['Archer 1 Name'].apply(extract_last_name) + ' v. ' + df['Archer 2 Name'].apply(extract_last_name) + ' (' + df['Year'].astype(str) + ')'
    
    # Sort matches by the highest average score per arrow and select the top 5
    top_matches = df.sort_values(by='Average Score per Arrow', ascending=False).head(5)
    
    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(top_matches['Match Label'], top_matches['Average Score per Arrow'], color='skyblue')
    
    #TODO: FIX LABEL NOT SHOWING
    plt.axhline(y=8.66, color='red', linestyle='--', label='Competition Average (8.66)')
    
    # Set plot details
    plt.title('Top 5 Matches in score')
    plt.ylabel('Average Score per Arrow')
    plt.xlabel('Match')
    plt.ylim(7, 10)  # Set y-axis range from 7 to 10
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to fit everything
    
    # Show the plot
    plt.show()


def plot_top_matches_by_accuracy(df):
    # Calculate total Xs for each match (sum of Archer 1 and Archer 2 Xs)
    df['Total Xs'] = df['Archer 1 Xs'] + df['Archer 2 Xs']
    
    # Create a label for each match by concatenating the last names of Archer 1 and Archer 2, and the year
    df['Match Label'] = df['Archer 1 Name'].apply(extract_last_name) + ' v. ' + df['Archer 2 Name'].apply(extract_last_name) + ' (' + df['Year'].astype(str) + ')'
    
    # Sort matches by the highest total Xs and select the top 5
    top_matches = df.sort_values(by='Total Xs', ascending=False).head(5)
    
    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(top_matches['Match Label'], top_matches['Total Xs'], color='skyblue')
    
    # Set plot details
    plt.title('Top 5 Matches in Xs')
    plt.ylabel('Total Xs')
    plt.xlabel('Match')
    plt.ylim(0, top_matches['Total Xs'].max() + 2)  # Add some buffer to y-axis for better visibility
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to fit everything
    plt.show()

# Function to plot archer performance by 1-spot vs 3-spot
def plot_1spot_vs_3spot(df):
    # Calculate average score per arrow for each archer
    df['Archer 1 Average Score per Arrow'] = df['Archer 1 Score'] / 12.0
    df['Archer 2 Average Score per Arrow'] = df['Archer 2 Score'] / 12.0
    
    # Combine Archer 1 and Archer 2 data into one DataFrame
    archer_data = pd.concat([
        df[['Archer 1 Target', 'Archer 1 Average Score per Arrow']].rename(columns={'Archer 1 Target': 'Target Type', 'Archer 1 Average Score per Arrow': 'Average Score per Arrow'}),
        df[['Archer 2 Target', 'Archer 2 Average Score per Arrow']].rename(columns={'Archer 2 Target': 'Target Type', 'Archer 2 Average Score per Arrow': 'Average Score per Arrow'})
    ])
    
    # Separate data for 1-spot and 3-spot targets
    spot_1_data = archer_data[archer_data['Target Type'] == '1-spot']
    spot_3_data = archer_data[archer_data['Target Type'] == '3-spot']
    
    # Calculate average score per arrow for both target types
    avg_1spot = spot_1_data['Average Score per Arrow'].mean()
    avg_3spot = spot_3_data['Average Score per Arrow'].mean()
    
    # Create a bar plot
    plt.figure(figsize=(8, 6))
    plt.bar(['1-Spot', '3-Spot'], [avg_1spot, avg_3spot], color=['blue', 'orange'])
    
    plt.title('1-Spot vs 3-Spot Targets (2024)')
    plt.ylabel('Average Score per Arrow')
    plt.ylim(7, 10)  # Set y-axis range from 7 to 10
    plt.show()


# Function to calculate and plot percentage of archers who won after hitting more Xs
def plot_xs_wins_percentage(df):
    # Add a column to check if Archer 1 hit more Xs than Archer 2
    df['Archer 1 More Xs'] = df['Archer 1 Xs'] > df['Archer 2 Xs']
    
    # Add a column to check if Archer 2 hit more Xs than Archer 1
    df['Archer 2 More Xs'] = df['Archer 2 Xs'] > df['Archer 1 Xs']

    # Exclude matches where both archers hit the same number of Xs
    df_filtered = df[df['Archer 1 Xs'] != df['Archer 2 Xs']].copy()  # Use .copy() to avoid SettingWithCopyWarning

    # Add columns to check if the winner had more Xs
    df_filtered.loc[:, 'Archer 1 Won'] = df_filtered['Winner'] == df_filtered['Archer 1 Name']
    df_filtered.loc[:, 'Archer 2 Won'] = df_filtered['Winner'] == df_filtered['Archer 2 Name']

    # Count the number of matches where the winner had more Xs
    xs_wins = (
        (df_filtered['Archer 1 More Xs'] & df_filtered['Archer 1 Won']) |
        (df_filtered['Archer 2 More Xs'] & df_filtered['Archer 2 Won'])
    ).sum()

    # Total number of matches where one archer had more Xs
    total_matches_with_more_xs = len(df_filtered)

    # Calculate the percentage of wins where the archer had more Xs
    xs_wins_percentage = (xs_wins / total_matches_with_more_xs) * 100

    # Plot a circular progress chart to visualize the percentage
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'aspect': 'equal'})

    # Create the progress chart
    wedges, texts = ax.pie([xs_wins_percentage, 100 - xs_wins_percentage], startangle=90, colors=['skyblue', 'lightgray'], wedgeprops={'width': 0.4})

    # Add text at the center of the pie
    plt.text(0, 0, f'{xs_wins_percentage:.1f}%', ha='center', va='center', fontsize=16)

    # Set the title
    plt.title(f'Percentage of Matches Won with More Xs', fontsize=14)

    # Display the chart
    plt.show()


# Function to display the fact about the only 12 hit
def plot_only_12_hit():
    plt.text(0.5, 0.5, "Only 1 12 has been hit! Jonsson hit it to force a tiebreaker in the 2024 finals!", fontsize=12, ha='center')
    plt.title('A single 12!')
    plt.show()

# Function to display the fact about zero matches without Xs and average Xs per match
def plot_zero_x_matches(df):
    zero_x_matches = (df['Archer 1 Xs'] + df['Archer 2 Xs'] == 0).sum()
    avg_xs_per_match = df[['Archer 1 Xs', 'Archer 2 Xs']].sum().sum() / len(df)

    plt.text(0.5, 0.5, f"There have been {zero_x_matches} matches where no one hit an X.\n"
                       f"The average number of Xs per match is {avg_xs_per_match:.2f}.",
             fontsize=12, ha='center')
    plt.title('Zero Xs!')
    plt.show()

# Function to display the average score per arrow across all matches
def plot_average_score_per_arrow(df):
    total_score = df['Archer 1 Score'].sum() + df['Archer 2 Score'].sum()
    total_arrows = 4 * len(df)
    avg_score_per_arrow = total_score / total_arrows

    plt.text(0.5, 0.5, f"The average score per arrow across all matches is {avg_score_per_arrow:.2f}.",
             fontsize=12, ha='center')
    plt.title('High quality!')
    plt.show()

# Function to display the list of archers by win percentage
def list_archers_by_win_percentage(df):
    # Combine Archer 1 and Archer 2 data into one DataFrame
    archer_data = pd.concat([
        df[['Archer 1 Name', 'Winner']].rename(columns={'Archer 1 Name': 'Archer', 'Winner': 'Is Winner'}),
        df[['Archer 2 Name', 'Winner']].rename(columns={'Archer 2 Name': 'Archer', 'Winner': 'Is Winner'})
    ])
    
    # Add a column to determine if the archer is the winner
    archer_data['Is Winner'] = archer_data.apply(lambda row: row['Is Winner'] == row['Archer'], axis=1)

    # Group by archer to calculate win percentage and count total matches
    archer_stats = archer_data.groupby('Archer').agg(
        Wins=('Is Winner', 'sum'),  # Count the number of wins
        Total_Matches=('Is Winner', 'count')  # Count the total number of matches
    )
    
    # Calculate win percentage
    archer_stats['Win Percentage'] = (archer_stats['Wins'] / archer_stats['Total_Matches']) * 100
    
    # Sort by win percentage and get the top 5 archers
    top_archers = archer_stats.sort_values(by='Win Percentage', ascending=False).head(5)
    
    # Display the top 5 archers
    print("Top 5 Archers by Win Percentage:")
    print(top_archers[['Win Percentage']])

#scatter plot
def plot_all_performances(df):
    # Calculate average Xs and average score per arrow for each archer
    archer_performance = pd.concat([
        df[['Archer 1 Name', 'Archer 1 Xs', 'Archer 1 Score']].rename(columns={
            'Archer 1 Name': 'Archer',
            'Archer 1 Xs': 'Xs',
            'Archer 1 Score': 'Score'
        }),
        df[['Archer 2 Name', 'Archer 2 Xs', 'Archer 2 Score']].rename(columns={
            'Archer 2 Name': 'Archer',
            'Archer 2 Xs': 'Xs',
            'Archer 2 Score': 'Score'
        })
    ])

    # Group by archer and calculate average Xs and average score per arrow
    archer_stats = archer_performance.groupby('Archer').agg(
        Average_Xs=('Xs', 'mean'),
        Average_Score_per_Arrow=('Score', lambda x: x.mean() / 12.0)
    ).reset_index()

    # Prepare data for linear regression
    X = archer_stats[['Average_Xs']].values
    y = archer_stats['Average_Score_per_Arrow'].values
    
    # Fit linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict y values for the regression line
    x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    y_pred = model.predict(x_range)
    
    # Create jitter
    jitter_strength_x = 0.1  # Adjust as needed
    jitter_strength_y = 0.1  # Adjust as needed
    archer_stats['Jitter_X'] = np.random.uniform(-jitter_strength_x, jitter_strength_x, size=len(archer_stats))
    archer_stats['Jitter_Y'] = np.random.uniform(-jitter_strength_y, jitter_strength_y, size=len(archer_stats))
    
    # Create scatter plot
    plt.figure(figsize=(12, 8))
    plt.scatter(
        archer_stats['Average_Xs'] + archer_stats['Jitter_X'],
        archer_stats['Average_Score_per_Arrow'] + archer_stats['Jitter_Y'],
        color='blue',
        label='Archers'
    )

    # Plot the linear regression line
    plt.plot(x_range, y_pred, color='red', linestyle='--', label='Linear Regression')

    # Annotate each point based on conditions
    for i, row in archer_stats.iterrows():
        x = row['Average_Xs'] + row['Jitter_X']
        y = row['Average_Score_per_Arrow'] + row['Jitter_Y']
        if (y > 8.888 and x > 1.5) or (x > 2) or (y < 8) or (y == 0 and y > 8.5):
            plt.annotate(row['Archer'], (x, y),
                         textcoords="offset points", xytext=(0,5), ha='center')

    # Set labels and title
    plt.xlabel('Average Number of Xs')
    plt.ylabel('Average Score per Arrow')
    plt.title('Average Xs vs Average Score per Arrow')
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()
    
def plot_heatmap(df):
    # Calculate average Xs and average score per arrow for each archer
    archer_performance = pd.concat([
        df[['Archer 1 Name', 'Archer 1 Xs', 'Archer 1 Score']].rename(columns={
            'Archer 1 Name': 'Archer',
            'Archer 1 Xs': 'Xs',
            'Archer 1 Score': 'Score'
        }),
        df[['Archer 2 Name', 'Archer 2 Xs', 'Archer 2 Score']].rename(columns={
            'Archer 2 Name': 'Archer',
            'Archer 2 Xs': 'Xs',
            'Archer 2 Score': 'Score'
        })
    ])

    # Group by archer and calculate average Xs and average score per arrow
    archer_stats = archer_performance.groupby('Archer').agg(
        Average_Xs=('Xs', 'mean'),
        Average_Score_per_Arrow=('Score', lambda x: x.mean() / 12.0)
    ).reset_index()

    # Prepare data for linear regression
    X = archer_stats[['Average_Xs']].values
    y = archer_stats['Average_Score_per_Arrow'].values
    
    # Fit linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict y values for the regression line
    x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    y_pred = model.predict(x_range)
    
    # Create scatter plot with heatmap
    plt.figure(figsize=(12, 8))
    
    # Scatter plot with KDE heatmap
    sns.kdeplot(
        data=archer_stats,
        x='Average_Xs',
        y='Average_Score_per_Arrow',
        cmap='Blues',
        fill=True,
        thresh=0.1,
        alpha=0.3
    )
    plt.scatter(
        archer_stats['Average_Xs'],
        archer_stats['Average_Score_per_Arrow'],
        color='blue',
        edgecolor='k',
        alpha=0.7
    )

    # Plot the linear regression line
    plt.plot(x_range, y_pred, color='red', linestyle='--', label='Linear Regression')

    # Set labels and title
    plt.xlabel('Average Number of Xs')
    plt.ylabel('Average Score per Arrow')
    plt.title('Average Xs vs Average Score per Arrow')
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()

def plot_average_score_per_year(df):
    # Calculate the average score per arrow for each match
    df['Average Score per Arrow'] = (df['Archer 1 Score'] + df['Archer 2 Score']) / 24

    # Group by year to calculate the average score per arrow for each year
    yearly_avg_score = df.groupby('Year')['Average Score per Arrow'].mean()

    # Define the range of years from 2018 to 2024
    years = range(2018, 2025)

    # Filter only the years that exist in the dataset
    available_years = yearly_avg_score.index.intersection(years)
    yearly_avg_score = yearly_avg_score.loc[available_years]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(available_years, yearly_avg_score, marker='o', linestyle='-', color='b', label='Average Score per Arrow')

    # Perform linear regression
    x_values = np.array(available_years)
    y_values = yearly_avg_score.values
    slope, intercept = np.polyfit(x_values, y_values, 1)  # Perform linear regression (degree 1)

    # Calculate regression line
    reg_line = slope * x_values + intercept

    # Plot the regression line
    plt.plot(x_values, reg_line, color='r', linestyle='--', label=f'Regression Line (slope={slope:.2f})')

    # Set plot labels and title
    plt.title('Tournament-wide Average Score per Arrow', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Average Score per Arrow', fontsize=12)
    
    # Ensure the x-axis includes all years from 2018 to 2024
    plt.xticks(years)
    plt.ylim(7, 10)  # Adjust the y-axis range if necessary
    plt.grid(True)
    plt.legend()

    # Show the plot
    plt.show()

def plot_average_xs_per_year(df):
    # Calculate the total number of Xs per match (Archer 1 Xs + Archer 2 Xs)
    df['Total Xs'] = df['Archer 1 Xs'] + df['Archer 2 Xs']

    # Group by year to calculate the average number of Xs per match for each year
    yearly_avg_xs = df.groupby('Year')['Total Xs'].mean()

    # Define the range of years from 2018 to 2024
    years = range(2018, 2025)

    # Filter only the years that exist in the dataset
    available_years = yearly_avg_xs.index.intersection(years)
    yearly_avg_xs = yearly_avg_xs.loc[available_years]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(available_years, yearly_avg_xs, marker='o', linestyle='-', color='b', label='Average Xs per Match')

    # Perform linear regression
    x_values = np.array(available_years)
    y_values = yearly_avg_xs.values
    slope, intercept = np.polyfit(x_values, y_values, 1)  # Perform linear regression (degree 1)

    # Calculate regression line
    reg_line = slope * x_values + intercept

    # Plot the regression line
    plt.plot(x_values, reg_line, color='r', linestyle='--', label=f'Regression Line (slope={slope:.2f})')

    # Set plot labels and title
    plt.title('Tournament-wide Average Xs per Match', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Average Xs per Match', fontsize=12)
    
    # Ensure the x-axis includes all years from 2018 to 2024
    plt.xticks(years)
    plt.ylim(0, 8)  # Adjust the y-axis range if necessary (depending on Xs distribution)
    plt.grid(True)
    plt.legend()

    # Show the plot
    plt.show()

#main
def main():
    # Load the dataset
    df = load_data()

    # Menu to choose analysis
    while True:
        print("\nBarebow Archery Analysis Menu:")
        print("1. Average Points per Match per Year")
        print("2. Total Xs per Match per Year")
        print("3. Top 10 Performances by Average Score per Arrow")
        print("4. Win Percentage by Riser Brand")
        print("5. Best Individual Performers")
        print("6. Top 10 Most Accurate Performers")
        print("7. Top 10 Most Matches")
        print("8. Top 5 Longest Winning Streaks")
        print("9. Percentage of Returning Archers")
        print("10. Top 5 Matches by Total Points")
        print("11. Top 5 Matches by Accuracy (Xs)")
        print("12. 1-Spot vs 3-Spot Performance (2024)")
        print("13. Percentage of Wins with More Xs")
        print("14. Only 12 Hit Fact") # Fixed the missing option number
        print("15. Zero X Matches and Average Xs per Match")
        print("16. Average Score per Arrow Across All Matches")
        print("17. List Archers by Win Percentage")
        print("18. Scatter plot")
        print("19. Heat map")
        print("20. Average Score per Arrow per Year")
        print("21. Average Xs per Year")
        print("0. Exit")
        
        # Get user input
        choice = input("Choose an option (0 to exit): ")

        # Call the corresponding function
        if choice == '1':
            plot_average_points_per_year(df)
        elif choice == '2':
            plot_total_xs_per_year(df)
        elif choice == '3':
            plot_top_performances(df)
        elif choice == '4':
            plot_win_percentage_by_riser(df)
        elif choice == '5':
            plot_best_individual_performers(df)
        elif choice == '6':
            plot_top_accurate_performers(df)
        elif choice == '7':
            plot_top_match_counts(df)
        elif choice == '8':
            plot_top_winning_streaks(df)
        elif choice == '9':
            plot_returning_archers(df)
        elif choice == '10':
            plot_top_matches_by_points(df)
        elif choice == '11':
            plot_top_matches_by_accuracy(df)
        elif choice == '12':
            plot_1spot_vs_3spot(df)
        elif choice == '13':
            plot_xs_wins_percentage(df)
        elif choice == '14':  # Fixed the missing option number
            plot_only_12_hit()
        elif choice == '15':
            plot_zero_x_matches(df)
        elif choice == '16':
            plot_average_score_per_arrow(df)
        elif choice == '17':
            list_archers_by_win_percentage(df)
        elif choice == '18':
            plot_all_performances(df)
        elif choice == '19':
            plot_heatmap(df)
        elif choice == '20':
            plot_average_score_per_year(df)
        elif choice == '21':
            plot_average_xs_per_year(df)
        elif choice == '0':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
