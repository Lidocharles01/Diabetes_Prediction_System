from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def home(request):
    return render(request,"index.html")

def user_home(request):
    return render(request,"home.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.is_superuser:
                return redirect('/admin')  # Redirect to the admin page
            else:
                return render(request, 'home.html')
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def register(request):
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username is already exist')
                    return render(request, 'register.html')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email is already exist')
                    return render(request, 'register.html')
                else:

                    # save data in db
                    user = User.objects.create_user(username=username, password=password1, email=email,
                                                    first_name=first_name, last_name=last_name)
                    user.save();
                    print('user created')
                    return redirect('login')

            else:
                messages.info(request, 'Invalid Credentials')
                return render(request, 'register.html')

        else:
            return render(request, 'register.html')


def predict(request):
    return render(request, 'predict.html')
def result(request):
    data = pd.read_csv(r"C:\Users\Lido Charles\PycharmProjects\thirdsem\DiabetesPrediction\diabetes.csv")
    X = data.drop(["Outcome", "Insulin"], axis=1)  # Excluding "Insulin" column
    Y = data["Outcome"]

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

    model = LogisticRegression()
    model.fit(X_train, Y_train)

    try:
        val2 = float(request.GET['n2'])
        val3 = float(request.GET['n3'])
        val4 = float(request.GET['n4'])
        val6 = float(request.GET['n6'])
        val7 = float(request.GET['n7'])
        val8 = float(request.GET['n8'])

        gender = request.GET.get('gender')  # Get the selected gender value
        val1 = 0  # Default value for male gender
        if gender == 'female':
            val1 = float(request.GET.get('n1', 0))  # Use input value if available

        pred = model.predict([[val1, val2, val3, val4, val6, val7, val8]])

        if pred == 1:
            result1 = "Oops! You have DIABETES 😔."
        else:
            result1 = "Great! You DON'T have diabetes 😁."

    except ValueError:
        result1 = "Please fill in all the required fields."

    return render(request, "predict.html", {"result2": result1})

