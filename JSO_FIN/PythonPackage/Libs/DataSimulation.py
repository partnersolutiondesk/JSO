from faker import Faker
# Create a Faker instance
fake = Faker()

# Function to generate fake customer data
def generate_fake_customer():
    return {
        "First_Name": fake.first_name(),
        "Last_Name": fake.last_name(),
        "Address": fake.address(),
        #"Account_ID": fake.uuid4(),
        "Account_ID": str(fake.random_int(min=1000000000, max=9999999999)),
        "Age": fake.random_int(min=18, max=60)
    }

def generate_OTP():
    return str(fake.random_int(min=100000, max=999999))
