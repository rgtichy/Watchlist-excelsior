from django.db import models
import bcrypt, re
# Create your models here.

def ValidateLogin(email,id):
    return User.objects.filter(email=email)[0].id == id
    return False

class UserManager(models.Manager):


    def register(self,data):

        email = data['email'].strip().lower()
        first_name = data['first_name'].strip()
        last_name = data['last_name'].strip()
        password = data['password'].strip()

        error = False
        errors = []
        if len(first_name) < 1:
            errors.append('Please enter a first name')
        if len(last_name) < 1:
            errors.append('Please enter a last name')
        if len(password) < 8:
            errors.append('Password must be at least 8 in length')
        if not re.search(r'[0-9]',password):
            errors.append('Password should contain at least one number.')
        if not re.search(r'[A-Z]',password):
            errors.append('Password should contain at least one uppercase.')
        if not re.search(r'[a-z]',password):
            errors.append('Password should contain at least one lowercase.')
        if not re.search(r'[~!@#$%^&*_+]',password):
            errors.append('Password should have at least one of these: ~!@#$%^&*_+')
        if not re.search(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$',email):
            errors.append('Enter a valid email address.')
        if data['password'] != data['password2']:
            errors.append('Password and validation password do not match.')

        if len(User.objects.filter(email=email)) > 0:
            errors.append('This email is already registered.')

        if len(errors) > 0:
            error = True
        # print email, first_name, last_name
        if error == False:
            # encrypt password
            # put stuff in  front of .Create
            temp = password.encode('utf-8')
            hashed = bcrypt.hashpw(temp,bcrypt.gensalt()).decode('utf-8')
            user = User.objects.create(email=email, first_name=first_name, last_name=last_name, password=hashed)
            # clear the password but pass the whole user object back so a landign page can user
            # user first name last name and email without .get, if desired
            user.password = '*cleared'
            user_dict={'user_id':user.id, 'first_name':user.first_name,'last_name':user.last_name,'email':user.email}
            return (True, user_dict)
        else:
            return (False, errors)

    def login(self, data):

        # print(data)
        email = data['user'].strip().lower()
        attempt = data['password'].strip()

        row = User.objects.filter(email=email)
        # print(row)

        if len(row) == 1:
            attempt = attempt.encode('utf-8')
            login = bcrypt.checkpw(attempt, row[0].password.encode('utf-8'))

            if login == True:
                # print("Login Successful:", email)
                row[0].password='*cleared'
                rdata = row[0]
            else:
                # print("Login Failed:", email)
                rdata = ['user/password combination not correct.']
        else:
            login = False
            rdata = ['User ID is invalid for login.']

        return (login, rdata)

class User(models.Model):
    email = models.EmailField(max_length = 100, null = False)
    password = models.CharField(max_length = 255 )
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    admin_flag = models.CharField(max_length = 1, default="N")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
