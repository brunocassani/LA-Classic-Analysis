import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
def load_data():
    return pd.read_csv('Mens_Barebow.csv')

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


# TODO: FIX
#Bar chart with top 10 performances (x-axis: archer name and the year in parenthesis, y-axis: average score per arrow (archer score / 12.0))
def plot_top_performances(df):
    df['Archer 1 Avg'] = df['Archer 1 Score'] / 12.0
    df['Archer 2 Avg'] = df['Archer 2 Score'] / 12.0

    top_performers = pd.melt(df[['Archer 1 Name', 'Archer 1 Avg', 'Year', 'Archer 2 Name', 'Archer 2 Avg']],
                             id_vars=['Year'], value_vars=['Archer 1 Avg', 'Archer 2 Avg'],
                             var_name='Archer', value_name='Avg Score').nlargest(10, 'Avg Score')

    top_performers.plot(x='Archer', y='Avg Score', kind='bar', figsize=(10, 6))
    plt.title('Men\'s Barebow: Top 10 Performances by Avg Score per Arrow')
    plt.xlabel('Archer (Year)')
    plt.ylabel('Average Score per Arrow')
    plt.show()

# TODO: FIX
#Win percentage visual by riser brand, also mentioning how many total (unique) archers each has sponsored (ex: (percentage/progress chart) company X has won 25/54. so the circle is fillled to 46.2%). ONE CHART PER COMPANY. LIKE A PIE CHART WITH ONLY ONE OPTION
def plot_win_percentage_by_riser(df):
    winners = df.groupby(['Winner', 'Archer 1 Riser', 'Archer 2 Riser']).size().reset_index(name='Wins')
    riser_stats = pd.melt(df[['Archer 1 Riser', 'Archer 2 Riser', 'Winner']],
                          id_vars=['Winner'], value_vars=['Archer 1 Riser', 'Archer 2 Riser'])

    for riser, group in riser_stats.groupby('value'):
        total_matches = len(group)
        wins = len(group[group['Winner'] == group['Winner']])
        win_percentage = (wins / total_matches) * 100

        plt.figure(figsize=(6, 6))
        plt.pie([win_percentage, 100 - win_percentage], labels=[f'{riser} Wins', 'Losses'], autopct='%1.1f%%')
        plt.title(f'Lorem Ipsum: Win Percentage for {riser}')
        plt.show()

# Bar chart with top 10 best individual performers  (x-axis: archer name and with all years in parenthesis, y-axis: average score per arrow (archer score / 12.0))
def plot_best_individual_performers(df):
    archer_scores = pd.melt(df[['Archer 1 Name', 'Archer 1 Score', 'Archer 2 Name', 'Archer 2 Score']],
                            value_vars=['Archer 1 Score', 'Archer 2 Score'], var_name='Archer', value_name='Score')

    match_counts = archer_scores.groupby('Archer').size()
    average_scores = archer_scores.groupby('Archer').mean()

    performers = average_scores[match_counts >= 2].nlargest(10, 'Score')

    performers.plot(kind='bar', figsize=(10, 6))
    plt.title('Lorem Ipsum: Best Individual Performers')
    plt.xlabel('Archer Name')
    plt.ylabel('Average Score per Arrow')
    plt.show()

# Function to create bar chart for top 10 most accurate performers (minimum 2 matches)
def plot_top_accurate_performers(df):
    archer_xs_counts = df[['Archer 1 Name', 'Archer 1 Xs', 'Archer 2 Name', 'Archer 2 Xs']]
    archer_xs_melt = pd.melt(archer_xs_counts, var_name='Archer', value_name='Xs')

    archer_xs = archer_xs_melt.groupby('Archer').mean().nlargest(10, 'Xs')

    archer_xs.plot(kind='bar', figsize=(10, 6))
    plt.title('Lorem Ipsum: Top 10 Most Accurate Performers')
    plt.xlabel('Archer Name')
    plt.ylabel('Average Xs per Match')
    plt.show()

# Function to create a bar chart for top 10 most matches
def plot_top_match_counts(df):
    matches = pd.melt(df, id_vars=['Match ID'], value_vars=['Archer 1 Name', 'Archer 2 Name'],
                      var_name='Archer Role', value_name='Archer')

    match_counts = matches['Archer'].value_counts().nlargest(10)

    match_counts.plot(kind='bar', figsize=(10, 6))
    plt.title('Lorem Ipsum: Top 10 Most Matches')
    plt.xlabel('Archer Name')
    plt.ylabel('Total Matches')
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

