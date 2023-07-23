from django.shortcuts import render,redirect
from django.contrib import messages
from server.models import user_registration, main_data
from django.db.models import Q
from django import forms
import csv,re
import pandas as pd

def login2(request):#for input data in database
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']  
        decoded_file = csv_file.read().decode('utf-8')  
        csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

        for row in csv_data:
            inst = row[0]
            aca=row[1]
            seat=row[2]
            gen=row[3]
            ope=row[4]
            clo=row[5]
            year=row[6]
            rou=row[7]
            my_instance = main_data( Institute=inst,Academic_Program_Name=aca,Seat_Type=seat,Gender=gen,Opening_Rank=ope,Closing_Rank=clo,Year=year,Round=rou)

            my_instance.save()
        
    print('Data has been imported successfully.')

    return render(request, 'login2.html')
class InputYear(forms.Form):
    year_choices = [(year, year) for year in range(2016, 2023)] 
    year = forms.IntegerField(label='Year', widget=forms.Select(choices=year_choices))

class InputForm(forms.Form):
    round_choices = [(round, round) for round in range(1, 8)]  
    round = forms.IntegerField(label='Round', widget=forms.Select(choices=round_choices))
    seat_type = forms.ChoiceField(label='Seat Type', choices=[('OPEN', 'OPEN'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST')])
    gender = forms.ChoiceField(label='Gender', choices=[('Female', 'Female'), ('Gender-Neutral', 'Gender-Neutral')])
    rank=forms.IntegerField(label='Rank', min_value=1, max_value=20000)

class all_functions:
  def filter_courses(self,data):
    df = pd.DataFrame(data)
    df['A'] = df['Academic_Program_Name'].str.replace(' ', '')
    df_no_duplicates = df.drop_duplicates(subset='A')
    df_data=df_no_duplicates['Academic_Program_Name'].tolist()
    return df_data
  
  def find_top_iits(self,data):
    df = pd.DataFrame(list(data.values()))
    df["Average"] = (df["Opening_Rank"] + df['Closing_Rank']) / 2
    grouped_data = df.groupby('Academic_Program_Name').size().reset_index(name='group_size').nlargest(10, 'group_size')
    first_10_groups = grouped_data['Academic_Program_Name'].tolist()
    df_filtered = df[df['Academic_Program_Name'].isin(first_10_groups)]
    grouped_by_institute = df_filtered.groupby('Institute')['Average'].mean().reset_index().sort_values('Average')
    top_iits = grouped_by_institute['Institute'].tolist()
    return top_iits

  def college_probability(self,rank_2022, avg_change, rank):
        closing_2022 = rank_2022 + avg_change
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
            interval_5_end = rank_2022
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
  
  def find_top_courses(self,year):
    queryset = main_data.objects.filter(Year=year, Round=1, Seat_Type='OPEN', Gender='Gender-Neutral')
    df = pd.DataFrame(list(queryset.values()))
    df["Average"] = (df["Opening_Rank"] + df['Closing_Rank']) / 2
    df1 = df[df['Average'] < 1000]
    df2 = df[(df['Average'] > 999) & (df['Average'] < 2000)]
    df3 = df[(df['Average'] > 1999) ]
    df2_filtered = df2[~df2['Academic_Program_Name'].isin(df1['Academic_Program_Name'])]
    df3_filtered = df3[~df3['Academic_Program_Name'].isin(df2['Academic_Program_Name']) & ~df3['Academic_Program_Name'].isin(df1['Academic_Program_Name'])]

    # Sort both DataFrames by 'Average' before merging
    df1_sorted = df1.sort_values(by='Average', ascending=True)
    df2_sorted = df2_filtered.sort_values(by='Average', ascending=True)
    df3_sorted = df3_filtered.sort_values(by='Average', ascending=True)

    # Combine the two DataFrames using concat along rows
    merged_df = pd.concat([df1_sorted, df2_sorted], axis=0)
    merged_df = pd.concat([merged_df, df3_sorted], axis=0)

    grouped_data = merged_df.groupby('Academic_Program_Name')['Average'].mean()
    sorted_data = grouped_data.sort_values(ascending=True)
    unique_names = sorted_data.index.unique().tolist()
    return unique_names
 
  def varify_email(self, email):
        user_data = user_registration.objects.filter(user_email=email)
        if len(user_data) != 0:
            return True
        return False  
  
  def is_valid_email(self, email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, email):
           return False 
        else:
             return True

  def is_valid_password(self, password):
        if len(password) < 8:
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        if not any(char.isdigit() for char in password):
            return False
        special_chars = "!@#$%^&*()_-+=<>?/"
        if not any(char in special_chars for char in password):
            return False
        return True

class authentication(all_functions):
   def signup(self,request):
    try:
        if request.method=='POST':
            email=request.POST.get('email')
            passw=request.POST.get('password')
            repassw=request.POST.get('c-password')

            if  self.varify_email(email):
                return render(request,'sign-up.html',{'error':'Email Already Exists'})
            elif self.is_valid_email(email):
               return render(request,'sign-up.html',{'error':'Invalid Email'})
            elif not self.is_valid_password(passw):
               return render(request,'sign-up.html',{'error':'Invalid Password'})
            elif passw !=repassw:
               return render(request,'sign-up.html',{'error':'Password and Confirm Password are not Same'})
            else:
             my_instance = user_registration(user_email=email, user_password=passw)
             my_instance.save()
             messages.success(request,f'New Account Created')
             return redirect('login')
         
    except:
        pass    
    return render(request,'sign-up.html')

   def login(self,request):
        
    try:
        if request.method=='POST':
            email=request.POST.get('email')
            passw=request.POST.get('password')
            user_data=user_registration.objects.filter(user_email=email)
            if len(user_data)==0:
                 return render(request,'login.html',{'error':'Invalid User Email'})
            elif passw != user_data[0].user_password :
                return render(request,'login.html',{'error':'Invalid-Password'}) 
            else:
                return redirect('home') 

    except:
       pass  
    return render(request,'login.html')

class analysis(all_functions): 
   def home(self,request):
    return render(request,'home.html')
   
   def institute(self,request):
    data = main_data.objects.order_by().values('Institute').distinct()
    return render(request, 'institute.html', {'data': data})
  
   def course_probablity(self,request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            round_num = form.cleaned_data['round']
            rank = form.cleaned_data['rank']
            seat_type = form.cleaned_data['seat_type']
            gender = form.cleaned_data['gender']
            data = main_data.objects.filter(
                Institute='Indian Institute of Technology Guwahati',
                Academic_Program_Name='Mathematics and Computing(B.Tech)',
                Seat_Type=seat_type,
                Gender=gender,
                Round=round_num
            )
            clo_2016 = data.filter(Year=data.earliest('Year').Year).values('Closing_Rank').first()['Closing_Rank']
            clo_2022 = data.filter(Year=2022).values('Closing_Rank').first()['Closing_Rank']
            difference = clo_2022 - clo_2016
            average_change = difference / 7
            probability = int(self.college_probability(clo_2022, average_change, rank)*100)
            return render(request, 'course_probability.html', {'probability': probability})
    else:
        form = InputForm()
    return render(request, 'course_probability.html', {'form': form})

   def branche(self, request):
    queryset = main_data.objects.filter(Year=2022, Round=1, Seat_Type='OPEN', Gender='Gender-Neutral')
    df = pd.DataFrame(list(queryset.values()))
    df=df.sort_values("Academic_Program_Name")
    df['Academic_Program_Name']=df['Academic_Program_Name'].str.replace('(B.Tech)', '')
    df['Academic_Program_Name']=df['Academic_Program_Name'].str.replace('(B.Tech & M.Tech)', '')
    df['Academic_Program_Name']=df['Academic_Program_Name'].str.replace('(BA)', '')
    df['Academic_Program_Name']=df['Academic_Program_Name'].str.replace('(MS)', '')
    df['Academic_Program_Name']=df['Academic_Program_Name'].str.replace('(BS & MS)', '')
    df['Academic_Program_Name']=df['Academic_Program_Name'].str.replace('(BS)', '')
    df['Academic_Program_Name']=df['Academic_Program_Name'].str.replace('and', '&')
    df['A'] = df['Academic_Program_Name'].str.replace(' ', '')
    df_no_duplicates = df.drop_duplicates(subset='A')
    df_data=df_no_duplicates['Academic_Program_Name'].tolist()
    return render(request, 'branche.html', {'data': df_data})

class top(all_functions):

   def top_courses(self,request):
    if request.method == 'POST':
        form = InputYear(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            data=self.find_top_courses(year)
            return render(request, 'top_courses.html', {'data': data})
    else:
        form = InputYear()

    return render(request, 'top_courses.html', {'form': form})
   
   def top_iits(self,request):
    if request.method == 'POST':
        form = InputYear(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            filtered_data = main_data.objects.filter(Year=year, Round=1, Seat_Type='OPEN', Gender='Gender-Neutral')
            data=self.find_top_iits(filtered_data)
            return render(request, 'top_iit.html', {'data': data})
    else:
        form = InputYear()

    return render(request, 'top_iit.html', {'form': form})

class courses(all_functions):
   
   def btech(self,request):
        data = main_data.objects.filter(Q(Academic_Program_Name__contains='B.Tech') & ~Q(Academic_Program_Name__contains='M.Tech')).order_by('Academic_Program_Name').values('Academic_Program_Name')
        data=self.filter_courses(data)
        return render(request, 'btech.html', {'data': data})

   def mtech(self,request):
    data = main_data.objects.filter(Academic_Program_Name__contains='M.tech').order_by('Academic_Program_Name').values('Academic_Program_Name').distinct()
    data=self.filter_courses(data)
    return render(request, 'mtech.html', {'data': data})
   

   def other(self,request):
    data = main_data.objects.filter(~Q(Academic_Program_Name__contains='B.Tech') & ~Q(Academic_Program_Name__contains='M.Tech')).order_by('Academic_Program_Name').values('Academic_Program_Name').distinct()
    data=self.filter_courses(data)
    return render(request, 'other.html', {'data': data})
