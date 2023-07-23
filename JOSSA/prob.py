import pandas as pd
from server.models import  main_data
# Query data from the database
data_queryset = main_data.objects.filter(
    Institute='Indian Institute of Technology Guwahati',
    Academic_Program_Name='Mathematics and Computing(B.Tech)',
    Seat_Type='OPEN',
    Gender='Gender-Neutral',
    Round=1
)

# Convert the queryset to a pandas DataFrame
df = pd.DataFrame(list(data_queryset.values()))

# Filter data for the required year and calculate the difference between closing ranks
clo_2016 = df.loc[df['Year'] == 2016, "Closing_Rank"]
clo_2021 = df.loc[df['Year'] == 2021, "Closing_Rank"]
rank = df.loc[df['Year'] == 2022, "Closing_Rank"]

difference = clo_2021.iloc[0] - clo_2016.iloc[0]
average_change = difference / 6

print("Closing Rank for 2016:")
print(clo_2016.to_string(index=False))

print("Closing Rank for 2021:")
print(clo_2021.to_string(index=False))
print("Closing Rank for 2022:")
print(rank.to_string(index=False))


def college_probability(rank_2021, avg_change, rank):
        closing_2022 = rank_2021 + avg_change
        interval_1_start = 1
        interval_1_end = closing_2022 / 4
        interval_2_start = interval_1_end + 1
        interval_2_end = closing_2022/3
        interval_3_start = interval_2_end + 1
        interval_3_end = closing_2022/2
        interval_4_start = interval_3_end + 1
        interval_4_end = closing_2022
        interval_5_start = interval_4_end + 1
        interval_5_end=0
        if avg_change > 0:
            interval_5_end = interval_5_start + avg_change
        else:
            interval_5_end = rank_2021
        interval_6_start = interval_5_end
        interval_6_end = 5 * closing_2022/4
        interval_7_start = interval_6_end+1
        interval_7_end = 3* closing_2022/2
        interval_8_start = interval_7_end+1
        interval_8_end = 7* closing_2022/4
        interval_7_start = interval_8_end+1
        interval_7_end = 2* closing_2022

     
        # Calculate the probability for each range
        if rank <= interval_1_end:
            probability = 1 - 0.05 * ((rank) / (interval_1_end - interval_1_start))
        elif rank <= interval_2_end:
            probability = 0.95 - 0.05 * ((rank - interval_2_start) / (interval_2_end - interval_2_start))
        elif rank <= interval_3_end:
            probability = 0.90 - 0.1 * ((rank - interval_3_start) / (interval_3_end - interval_3_start))
        elif rank <= interval_4_end:
            probability = 0.8 - 0.3 * ((rank - interval_4_start) / (interval_4_end - interval_4_start))
        elif rank<=interval_5_end:
            probability= 0.5-0.05*((rank-interval_5_start)/(interval_5_end-interval_5_start))
        elif rank<=interval_6_end:
            probability= 0.45-0.075*((rank-interval_6_start)/(interval_6_end-interval_6_start))
        elif rank<=interval_7_end:
            probability= 0.325-0.1*((rank-interval_7_start)/(interval_7_end-interval_7_start))
        elif rank<=interval_8_end:
            probability= 0.225-0.2*((rank-interval_8_start)/(interval_8_end-interval_8_start))
        else:
            probability = 0.025
        
        return probability
x=int(input("Enter your rank"))
probability = college_probability(clo_2021.iloc[0],average_change,x)
print(f"Probability of getting a college with rank {x} in 2022 is: {probability:.2f}")
