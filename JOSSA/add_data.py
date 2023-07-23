import pandas as pd
from server.models import popular_course

csv_file = pd.read_csv('2022department_popularity_frequency.csv')
print(csv_file)
# for index, row in csv_file.iterrows():
#     dept = row['Department']
#     score = row['popu']
#     course = popular_course(department_name=dept, department_score=score)
#     course.save()
