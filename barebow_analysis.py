import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('Mens_Barebow.csv')

# Remove duplicate sponsor entries for each archer
unique_sponsors = data[['Archer 1 Riser', 'Archer 1 Name']].drop_duplicates()

# 1. Most archers sponsored per riser brand
sponsored_archers = unique_sponsors.groupby('Archer 1 Riser')['Archer 1 Name'].count().reset_index().sort_values(by='Archer 1 Name', ascending=False)
print("Most Archers Sponsored Per Riser Brand:\n", sponsored_archers)

# 2. Most represented riser brand
most_represented = data.groupby('Archer 1 Riser').size().reset_index(name='Matches').sort_values(by='Matches', ascending=False)
print("Most Represented Riser Brand:\n", most_represented)

# 3. Average points per match (for each year)
def plot_avg_points_per_year():
    avg_points_per_match = data.groupby(['Year', 'Match ID'])[['Archer 1 Score', 'Archer 2 Score']].mean().reset_index()
    for year in avg_points_per_match['Year'].unique():
        year_data = avg_points_per_match[avg_points_per_match['Year'] == year]
        plt.plot(year_data['Match ID'], year_data[['Archer 1 Score', 'Archer 2 Score']].mean(axis=1), label=f'Year {year}')
    
    plt.xlabel('Match ID')
    plt.ylabel('Average Points')
    plt.legend()
    plt.title('Average Points per Match by Year')
    plt.show()

plot_avg_points_per_year()

# 4. Average Xs per match (for each year)
def plot_avg_xs_per_year():
    avg_xs_per_match = data.groupby(['Year', 'Match ID'])[['Archer 1 Xs', 'Archer 2 Xs']].mean().reset_index()
    for year in avg_xs_per_match['Year'].unique():
        year_data = avg_xs_per_match[avg_xs_per_match['Year'] == year]
        plt.plot(year_data['Match ID'], year_data[['Archer 1 Xs', 'Archer 2 Xs']].mean(axis=1), label=f'Year {year}')
    
    plt.xlabel('Match ID')
    plt.ylabel('Average Xs')
    plt.legend()
    plt.title('Average Xs per Match by Year')
    plt.show()

plot_avg_xs_per_year()

# 5. Highest/lowest quality match
data['Total Score'] = data['Archer 1 Score'] + data['Archer 2 Score']
highest_quality_match = data.loc[data['Total Score'].idxmax()]
lowest_quality_match = data.loc[data['Total Score'].idxmin()]

print("Highest Quality Match:\n", highest_quality_match)
print("Lowest Quality Match:\n", lowest_quality_match)

# 6. Average performance per riser brand (avg points, avg Xs)
performance_by_riser = data.groupby('Archer 1 Riser')[['Archer 1 Score', 'Archer 1 Xs']].mean().reset_index()
print("Average Performance Per Riser Brand:\n", performance_by_riser)

# 7. Is the 3-spot target effective? 
three_spot_data = data[(data['Archer 1 Target'] == '3-spot') | (data['Archer 2 Target'] == '3-spot')]
avg_3_spot_performance = three_spot_data[['Archer 1 Score', 'Archer 2 Score']].mean().mean()
print("Average Score for 3-Spot Target Matches:", avg_3_spot_performance)

