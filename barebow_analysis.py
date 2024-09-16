import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# HERE ARE ALL THE COLUMNS FROM Mens_Barebow IN ORDER
# Match ID, Archer 1 Name, Archer 2 Name, Archer 1 Score, Archer 2 Score, Archer 1 Xs, Archer 2 Xs, Archer 1 Target, Archer 2 Target, Archer 1 Riser, Archer 2 Riser, Winner, Year, Notes

# Load the data
def load_data():
    return pd.read_csv('Mens_Barebow.csv')

#WORKING
#average points per arrow
def plot_average_points_per_year(df):
    # Add Match Number column for each year
    df['Match Number'] = df.groupby('Year').cumcount() + 1
    # Calculate the average points per arrow
    df['Average Points per Arrow'] = (df['Archer 1 Score'] + df['Archer 2 Score']) / 24

    max_match_number = 7  # The final match should be at x = 7

    plt.figure(figsize=(10, 6))

    for year, data in df.groupby('Year'):
        # Scale match numbers so that the final match is at `max_match_number`
        num_matches = data['Match Number'].max()
        scaled_match_number = data['Match Number'] * (max_match_number / num_matches)
        
        plt.plot(scaled_match_number, data['Average Points per Arrow'], marker='o', label=f"{year}")

    plt.title('Men\'s Barebow: Average Points per Arrow per match')
    plt.xlabel('Match')
    plt.ylabel('Average Points per Arrow')
    plt.xticks(range(1, max_match_number + 1))  # Ensure x-axis has labels 1 to 7
    plt.ylim(7, 10)  # Set y-axis range from 7 to 10
    plt.legend(title="Year")
    plt.grid(True)
    plt.show()

#WORKING
# Function to create the stacked line chart for total Xs per match per year
def plot_total_xs_per_year(df):
    df['Match Number'] = df.groupby('Year').cumcount() + 1
    df['Total Xs'] = df['Archer 1 Xs'] + df['Archer 2 Xs']

    max_match_number = 7  # The final match should be at x = 7

    plt.figure(figsize=(10, 6))

    for year, data in df.groupby('Year'):
        # Scale match numbers so that the final match is at `max_match_number`
        num_matches = data['Match Number'].max()
        scaled_match_number = data['Match Number'] * (max_match_number / num_matches)
        
        plt.plot(scaled_match_number, data['Total Xs'], marker='o', label=f"{year}")

    # Set the title, labels, and grid
    plt.title("Men's Barebow: Total Xs per Match")
    plt.xlabel('Match #')
    plt.ylabel('Total Xs')
    plt.xticks(range(1, max_match_number + 1))  # Ensure x-axis has labels 1 to 7
    plt.ylim(0, 8)  # Set y-axis range from 0 to 8
    plt.legend(title="Year")
    plt.grid(True)
    
    # Show the plot
    plt.show()

#WORKING
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
    plt.title('Top 10 Men\'s Barebow Single Performances (Average Score per Arrow)')
    plt.ylabel('Average Score per Arrow')
    plt.ylim(8.4, 10)  # Set y-axis range from 7 to 10
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to fit everything
    
    # Show the plot
    plt.show()

#WOKRING
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
    plt.title('Top 5 Best Individual Performers (Average Score per Arrow)')
    plt.ylabel('Average Score per Arrow')
    plt.ylim(8.2, 10)  # Set y-axis range to match typical scores
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for readability
    plt.tight_layout()  # Adjust layout
    
    # Show the plot
    plt.show()

#WORKING
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
    plt.title('Top 10 Most Accurate Performers (Average Xs per Match)')
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


# Function to plot top 5 longest winning streaks
def plot_top_winning_streaks(df):
    df['Win Streak'] = (df['Winner'] == df['Archer 1 Name']) | (df['Winner'] == df['Archer 2 Name'])

    streaks = df.groupby('Winner')['Win Streak'].apply(lambda x: x.cumsum()).nlargest(5)

    streaks.plot(kind='bar', figsize=(10, 6))
    plt.title('Lorem Ipsum: Top 5 Longest Winning Streaks')
    plt.xlabel('Archer Name')
    plt.ylabel('Longest Win Streak')
    plt.show()

# Function to calculate and plot the percentage of returning archers
def plot_returning_archers(df):
    archer_years = df.melt(id_vars=['Year'], value_vars=['Archer 1 Name', 'Archer 2 Name'],
                           var_name='Archer Role', value_name='Archer')

    returning_archers = archer_years.groupby('Archer')['Year'].nunique()
    returning_percentage = (returning_archers > 1).mean() * 100

    plt.figure(figsize=(6, 6))
    plt.pie([returning_percentage, 100 - returning_percentage], labels=['Returning', 'Non-Returning'], autopct='%1.1f%%')
    plt.title(f'Lorem Ipsum: {returning_percentage:.2f}% Returning Archers')
    plt.show()

# Function to calculate and plot the top 5 matches by total points
def plot_top_matches_by_points(df):
    df['Total Points'] = df['Archer 1 Score'] + df['Archer 2 Score']
    top_5_matches = df.nlargest(5, 'Total Points')

    top_5_matches.plot(x='Match ID', y='Total Points', kind='bar', figsize=(10, 6))
    plt.title('Lorem Ipsum: Top 5 Best Matches by Total Points')
    plt.xlabel('Match (Archer 1 vs Archer 2, Year)')
    plt.ylabel('Total Points')
    plt.show()

# Function to plot top 5 best matches by accuracy (Xs)
def plot_top_matches_by_accuracy(df):
    df['Total Xs'] = df['Archer 1 Xs'] + df['Archer 2 Xs']
    top_5_xs_matches = df.nlargest(5, 'Total Xs')

    top_5_xs_matches.plot(x='Match ID', y='Total Xs', kind='bar', figsize=(10, 6))
    plt.title('Lorem Ipsum: Top 5 Best Matches by Total Xs')
    plt.xlabel('Match (Archer 1 vs Archer 2, Year)')
    plt.ylabel('Total Xs')
    plt.show()

# Function to plot archer performance by 1-spot vs 3-spot
def plot_1spot_vs_3spot(df):
    df_2024 = df[df['Year'] == 2024]
    target_type = df_2024.groupby('Archer 1 Target')['Archer 1 Score'].sum() + df_2024.groupby('Archer 2 Target')['Archer 2 Score'].sum()

    target_type.plot(kind='bar', figsize=(10, 6))
    plt.title('Lorem Ipsum: 3-Spot vs 1-Spot Performance in 2024')
    plt.xlabel('Target Type')
    plt.ylabel('Average Score per Arrow')
    plt.show()

# Function to calculate and plot percentage of archers who won after hitting more Xs
def plot_xs_wins_percentage(df):
    df['More Xs Wins'] = (df['Archer 1 Xs'] > df['Archer 2 Xs']) & (df['Winner'] == df['Archer 1 Name']) | \
                         (df['Archer 2 Xs'] > df['Archer 1 Xs']) & (df['Winner'] == df['Archer 2 Name'])

    xs_wins_percentage = df['More Xs Wins'].mean() * 100

    plt.figure(figsize=(6, 6))
    plt.pie([xs_wins_percentage, 100 - xs_wins_percentage], labels=['Won with More Xs', 'Did Not Win'], autopct='%1.1f%%')
    plt.title(f'Lorem Ipsum: {xs_wins_percentage:.2f}% of Archers Won with More Xs')
    plt.show()

# Function to calculate and plot percentage of archers who lost after hitting more Xs
def plot_xs_losses_percentage(df):
    df['More Xs Losses'] = (df['Archer 1 Xs'] > df['Archer 2 Xs']) & (df['Winner'] == df['Archer 2 Name']) | \
                           (df['Archer 2 Xs'] > df['Archer 1 Xs']) & (df['Winner'] == df['Archer 1 Name'])

    xs_losses_percentage = df['More Xs Losses'].mean() * 100

    plt.figure(figsize=(6, 6))
    plt.pie([xs_losses_percentage, 100 - xs_losses_percentage], labels=['Lost with More Xs', 'Did Not Lose'], autopct='%1.1f%%')
    plt.title(f'Lorem Ipsum: {xs_losses_percentage:.2f}% of Archers Lost with More Xs')
    plt.show()

# Function to display the fact about the only 12 hit
def plot_only_12_hit():
    plt.text(0.5, 0.5, "Only 1 12 has been hit! Jonsson hit it to force a tiebreaker in the 2024 finals!", fontsize=12, ha='center')
    plt.title('Lorem Ipsum: Only 12 Hit Fact')
    plt.show()

# Function to display the fact about zero matches without Xs and average Xs per match
def plot_zero_x_matches(df):
    zero_x_matches = (df['Archer 1 Xs'] + df['Archer 2 Xs'] == 0).sum()
    avg_xs_per_match = df[['Archer 1 Xs', 'Archer 2 Xs']].sum().sum() / len(df)

    plt.text(0.5, 0.5, f"There have been {zero_x_matches} matches where no one hit an X.\n"
                       f"The average number of Xs per match is {avg_xs_per_match:.2f}.",
             fontsize=12, ha='center')
    plt.title('Lorem Ipsum: Zero X Matches and Average Xs')
    plt.show()

# Function to display the average score per arrow across all matches
def plot_average_score_per_arrow(df):
    total_score = df['Archer 1 Score'].sum() + df['Archer 2 Score'].sum()
    total_arrows = 4 * len(df)
    avg_score_per_arrow = total_score / total_arrows

    plt.text(0.5, 0.5, f"High quality! The average score per arrow across all matches is {avg_score_per_arrow:.2f}.",
             fontsize=12, ha='center')
    plt.title('Lorem Ipsum: Average Score per Arrow Across All Matches')
    plt.show()

# Function to display the list of archers by win percentage
def list_archers_by_win_percentage(df):
    wins = df.groupby('Winner').size()
    total_matches = df[['Archer 1 Name', 'Archer 2 Name']].melt()['value'].value_counts()
    win_percentage = (wins / total_matches).sort_values(ascending=False).fillna(0)

    print("Lorem Ipsum: List of Archers by Win Percentage")
    print(win_percentage)

# Function to display the list of archers who have switched riser companies
def list_archers_switched_risers(df):
    archer_riser_history = pd.melt(df[['Archer 1 Name', 'Archer 1 Riser', 'Year', 'Archer 2 Name', 'Archer 2 Riser']],
                                   id_vars=['Year'], value_vars=['Archer 1 Riser', 'Archer 2 Riser'],
                                   var_name='Archer Role', value_name='Riser')
    
    archer_risers = archer_riser_history.pivot_table(index='Archer Role', columns='Year', values='Riser', aggfunc='first')
    switched_risers = archer_risers.apply(lambda x: len(x.unique()) > 1, axis=1)

    print("Lorem Ipsum: List of Archers Who Have Switched Riser Companies")
    print(switched_risers[switched_risers].index.tolist())

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
        print("5. Best Individual Performers (Min. 2 Matches)")
        print("6. Top 10 Most Accurate Performers (Min. 2 Matches)")
        print("7. Top 10 Most Matches")
        print("8. Top 5 Longest Winning Streaks")
        print("9. Percentage of Returning Archers")
        print("10. Top 5 Matches by Total Points")
        print("11. Top 5 Matches by Accuracy (Xs)")
        print("12. 1-Spot vs 3-Spot Performance (2024)")
        print("13. Percentage of Wins with More Xs")
        print("14. Percentage of Losses with More Xs")
        print("15. Only 12 Hit Fact")
        print("16. Zero X Matches and Average Xs per Match")
        print("17. Average Score per Arrow Across All Matches")
        print("18. List Archers by Win Percentage")
        print("19. List Archers Who Switched Riser Companies")
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
        elif choice == '14':
            plot_xs_losses_percentage(df)
        elif choice == '15':
            plot_only_12_hit()
        elif choice == '16':
            plot_zero_x_matches(df)
        elif choice == '17':
            plot_average_score_per_arrow(df)
        elif choice == '18':
            list_archers_by_win_percentage(df)
        elif choice == '19':
            list_archers_switched_risers(df)
        elif choice == '0':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

