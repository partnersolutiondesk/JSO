from faker import Faker
# Create a Faker instance
fake = Faker()
from random import choice
import datetime

# Function to generate fake customer data
def generate_fake_customer():
    answer = choice(['yes', 'no'])
    profession = choice(['Engineer', 'Teacher', 'Doctor', 'Plumber', 'Driver'])
    incomesource=choice(['service', 'business', 'farming', 'trading'])
    Industry_Sector=choice(["IT service", "Banking", "Retail"])
    payslip=choice(['yes','no'])
    itreturn = choice(['yes', 'no'])
    dob=datetime.datetime.combine(fake.date_of_birth(minimum_age=18, maximum_age=105), datetime.time.min)
    return {
        "First_Name": fake.first_name(),
        "Last_Name": fake.last_name(),
        "Address": fake.address(),
        #"Account_ID": fake.uuid4(),
        "Account_ID": str(fake.random_int(min=1000000000, max=9999999999)),
        "Age": fake.random_int(min=18, max=60),
        #'DOB':  fake.date_between(start_date="-60y", end_date="now"),
        'DOB': dob,
        'Pincode': fake.zipcode(),
        'Profession': profession,
        'credit_score': fake.random_int(min=1, max=1000),
        'Income_source': incomesource,
        'Industry_Sector': Industry_Sector,
        'Income_range': fake.random_int(min=1000, max=100000),
        'Payslip': payslip,
        'IT_return':itreturn ,
        'AML': payslip

        }

def generate_OTP():
    return str(fake.random_int(min=100000, max=999999))
