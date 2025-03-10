
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from users.models import Register, User_Details, Case_Details, Lawyer_Register, Basic_Laws, Book_Lawyer, Payment_Details, \
    Emergency_Numbers


def signup(request):

    if request.method == "POST":
        Name = request.POST.get('Name')
        Email = request.POST.get('Email')
        Number = request.POST.get('Number')
        Username = request.POST.get('Username')
        Password = request.POST.get('Password')
        Confirm_Password = request.POST.get('Password1')
        if Password != Confirm_Password:
            return render(request,"Signup.html",{'Error':'Passwords Doesnot Match'})
        else:
          hashed_password = make_password(Password)
          Register.objects.create(Name=Name,Email=Email,Number=Number,Username=Username,Password=hashed_password)
          return render(request, "Login.html")
    return render(request,"Signup.html")

def login(request):

    if request.method == "POST":
        Username = request.POST.get('Username')
        Password = request.POST.get('Password')

        try:
            user = Register.objects.get(Username=Username)
            if check_password(Password, user.Password):
                request.session['User_Id'] = user.User_Id
                return redirect('home')
            else:
                return render(request, "Login.html", {'Error': ' Password is Invalid'})
        except Register.DoesNotExist:
            return render(request, "Login.html", {'Error': 'Username or Password is Invalid'})

    return render(request, "Login.html")


def forgot_password(request):

    if request.method == "POST":
        Email = request.POST.get('Email')
        Password = request.POST.get('Password')
        ConfirmPassword = request.POST.get('Password1')
        try:
            user = Register.objects.get(Email=Email)
            if Password == ConfirmPassword:
                hashed_password = make_password(Password)
                user.Password = hashed_password
                user.save()
                return redirect("login")
            else:
                return render(request,"ForgotPassword.html",{"Error":"Password Doesnot Match"})

        except Register.DoesNotExist:
            return render(request,"ForgotPassword.html",{"Error":"Email Doesnot Exist"})
    return render(request,"ForgotPassword.html")

def home(request):
    if "User_Id" in request.session:
        User_Id = request.session["User_Id"]
        r = Register.objects.get(User_Id=User_Id)
        return render(request,"Home.html",{'r':r})

def register_case(request):
    if "User_Id" in request.session:
        user = request.session["User_Id"]
        try:
            register_instance = Register.objects.get(User_Id=user)
        except Register.DoesNotExist:
            return redirect("register_case")

        if request.method =="POST" :
                Name = request.POST.get('Name')
                Number = request.POST.get('Number')
                Email = request.POST.get('Email')
                Address = request.POST.get('Address')
                City = request.POST.get('City')
                State = request.POST.get('State')

                Complaint_Type = request.POST.get('Complaint_Type')
                Complaint_Subject = request.POST.get('Complaint_Subject')
                Complaint_Area = request.POST.get('Complaint_Area')
                Complaint_Date = request.POST.get('Complaint_Date')
                Complaint_Description = request.POST.get('Complaint_Description')
                Complaint_Image = request.FILES.get('Image')

                case_instance=User_Details.objects.create(User=register_instance, Name=Name, Number=Number, Email=Email,
                                            Address=Address, City=City,State=State)

                Case_Details.objects.create(Case=case_instance,Complaint_Type=Complaint_Type, Complaint_Subject=Complaint_Subject,
                                            Complaint_Area=Complaint_Area, Complaint_Date=Complaint_Date,
                                            Complaint_Details=Complaint_Description,Complaint_Image=Complaint_Image)
                return redirect("home")

        return render(request,"RegisterCase.html")

def lawyer_list(request):
    if "User_Id" in request.session and  request.method=="POST":

        sort = request.POST.get('Sort',"All")
        filter = request.POST.get('Filter',"All")
        search = request.POST.get('Search',"")
        query_params = {
            "Sort": sort,
            "Filter" : filter,

        }
        if search:
            query_params["Search"] = search

        query_string = '&'.join([f'{k}={v}' for k, v in query_params.items()])
        return redirect(f"{request.path}?{query_string}")



    lawyer = Lawyer_Register.objects.all()

    sort = request.GET.get('Sort', "All")
    filter = request.GET.get('Filter', "All")
    search = request.GET.get('Search', "")
    page_number = request.GET.get("page",1)
    # Sort
    if sort == "Name_asc":
            lawyer = lawyer.order_by('Name')
    elif sort == "Name_desc":
            lawyer = lawyer.order_by('-Name')


    # filter
    if filter != "All":
        lawyer = lawyer.filter(Category=filter)

    # Search
    if search:
        lawyer = lawyer.filter(Law_Title__icontains=search)


    # Pagination
    paginator = Paginator(lawyer, 8)
    page_obj = paginator.get_page(page_number)

    User_Id = request.session["User_Id"]
    r = Register.objects.get(User_Id=User_Id)
    return render(request, "Lawyers.html", {
            "page_obj": page_obj,
            "Filter": filter,
            "Sort": sort,
            "Search": search,
            "r":r,
        })


def update_user(request,id):
    user = Register.objects.get(User_Id=id)

    if request.method == "POST":
        user.Name = request.POST.get('Name')
        user.Email = request.POST.get('Email')
        user.Number = request.POST.get('Number')
        try:

            New_Password = request.POST.get('NewPassword')
            ConfirmPassword = request.POST.get('Password1')
            if New_Password == ConfirmPassword:
                    hashed_password = make_password(New_Password)
                    user.Password = hashed_password
                    user.save()
                    return redirect("home")
            else:
                    return render(request, "Update_User.html.html", {"Error": "Password Doesnot Match"})
        except:
          user.save()
          return redirect("home")


    return render(request,"Update_User.html",{'user':user})



def logout(request):
    if "User_Id" in request.session:
        del request.session["User_Id"]
    return render(request, "Login.html")

def emergency_numbers(request):
    if "User_Id" in request.session:
        User_Id = request.session["User_Id"]
        r = Register.objects.get(User_Id=User_Id)
        Num = Emergency_Numbers.objects.all()
        search = request.POST.get('Search')
        if search:
            Num = Num.filter(Title__icontains=search)
        return render(request,"EmergencyNumbers.html",{'Num':Num ,'r':r})

def book_lawyer1(request):
    LawyersNames = Lawyer_Register.objects.values('Name','Category')
    if "User_Id" in request.session and request.method == "POST":
        user = request.session["User_Id"]
        try:
            register_instance = Register.objects.get(User_Id=user)
        except Register.DoesNotExist:
            return redirect("book_lawyer")

        Name = request.POST.get('Name')
        Number = request.POST.get('Number')
        Email = request.POST.get('Email')
        City = request.POST.get('City')
        State = request.POST.get('State')

        Lawyer_Name = request.POST.get('LawyerName')
        Category = request.POST.get('Category')
        Appointment_Date = request.POST.get('Appointment_Date')
        Appointment_Time = request.POST.get('Appointment_Time')
        Contact_Time = request.POST.get('Contact_Time')


        booking = Book_Lawyer.objects.create(
            User=register_instance,
            Name=Name,
            Number=Number,
            Email=Email,
            City=City,
            State=State,
            Lawyer_Name=Lawyer_Name,
            Category=Category,
            Appointment_Date=Appointment_Date,
            Appointment_Time=Appointment_Time,
            Contact_Time=Contact_Time
        )

        return redirect("payment",Book_Id=booking.Book_Id)

    return render(request, 'BookLawyer1.html', {'LawyersNames': LawyersNames})

def book_lawyer2(request,id):
    Lawyer = Lawyer_Register.objects.get(User_Id=id)
    if "User_Id" in request.session and request.method == "POST":

        user = request.session["User_Id"]

        try:
            register_instance = Register.objects.get(User_Id=user)
        except Register.DoesNotExist:
            return redirect("book_lawyer")

        Name = request.POST.get('Name')
        Number = request.POST.get('Number')
        Email = request.POST.get('Email')
        City = request.POST.get('City')
        State = request.POST.get('State')

        Lawyer.Lawyer_Name = request.POST.get('Lawyer_Name')
        Lawyer.Category = request.POST.get('Category')
        Appointment_Date = request.POST.get('Appointment_Date')
        Appointment_Time = request.POST.get('Appointment_Time')
        Contact_Time = request.POST.get('Contact_Time')

        booking = Book_Lawyer.objects.create(
            User=register_instance,
            Name=Name,
            Number=Number,
            Email=Email,
            City=City,
            State=State,
            Lawyer_Name=Lawyer.Lawyer_Name,
            Category=Lawyer.Category,
            Appointment_Date=Appointment_Date,
            Appointment_Time=Appointment_Time,
            Contact_Time=Contact_Time
        )

        return redirect("payment",Book_Id=booking.Book_Id)

    return render(request, 'BookLawyer2.html',{'Lawyer':Lawyer})

def book_lawyer3(request,Book_Id):
    Lawyer = Book_Lawyer.objects.get(Book_Id=Book_Id)
    if "User_Id" in request.session and request.method == "POST":
        user = request.session["User_Id"]

        try:
            register_instance = Register.objects.get(User_Id=user)
        except Register.DoesNotExist:
            return redirect("book_lawyer")

        Lawyer.Name = request.POST.get('Name')
        Lawyer.Number = request.POST.get('Number')
        Lawyer.Email = request.POST.get('Email')
        Lawyer.City = request.POST.get('City')
        Lawyer.State = request.POST.get('State')

        Lawyer.Lawyer_Name = request.POST.get('Lawyer_Name')
        Lawyer.Category = request.POST.get('Category')
        Appointment_Date = request.POST.get('Appointment_Date')
        Appointment_Time = request.POST.get('Appointment_Time')
        Contact_Time = request.POST.get('Contact_Time')

        booking = Book_Lawyer.objects.create(
            User=register_instance,
            Name=Lawyer.Name,
            Number=Lawyer.Number,
            Email=Lawyer.Email,
            City=Lawyer.City,
            State=Lawyer.State,
            Lawyer_Name=Lawyer.Lawyer_Name,
            Category=Lawyer.Category,
            Appointment_Date=Appointment_Date,
            Appointment_Time=Appointment_Time,
            Contact_Time=Contact_Time
        )

        return redirect("payment",Book_Id=booking.Book_Id)

    return render(request, 'BookLawyer3.html',{'i':Lawyer})

def basiclaws(request):

    # Handle POST requests (from search, filter, or sort forms)
    if "User_Id"  in request.session and request.method == "POST":

        # Get filter, sort, and search parameters from POST data
        filter_data = request.POST.get("Filter", "All")
        sort = request.POST.get("Sort", "All")
        search = request.POST.get("Search", "")

        # Construct query parameters for redirection
        query_params = {
            "Filter": filter_data,
            "Sort": sort,
        }
        if search:
            query_params["Search"] = search

        # Redirect to GET request with query parameters
        query_string = '&'.join([f'{k}={v}' for k, v in query_params.items()])
        return redirect(f"{request.path}?{query_string}")

    # Handle GET requests
    # Retrieve all Basic_Laws objects
    laws = Basic_Laws.objects.all()

    # Get filter, sort, search, and page parameters from GET data
    filter_data = request.GET.get("Filter", "All")
    sort = request.GET.get("Sort", "All")
    search = request.GET.get("Search", "")
    page_number = request.GET.get("page", 1)

    # Apply search filter if provided
    if search:
        laws = laws.filter(Law_Title__icontains=search)

    # Apply category filter if not 'All'
    if filter_data != "All":
        laws = laws.filter(Law_Category=filter_data)

    # Apply sorting
    if sort == "Name_asc":
        laws = laws.order_by("Law_Title")
    elif sort == "Name_desc":
        laws = laws.order_by("-Law_Title")

    # Paginate the results (6 items per page)
    paginator = Paginator(laws, 6)
    page_obj = paginator.get_page(page_number)

    User = request.session["User_Id"]
    r = Register.objects.get(User_Id=User)
    # Render the template with context
    return render(request, "BasicLaws.html", {
        "page_obj": page_obj,
        "Filter": filter_data,
        "Sort": sort,
        "Search": search,
        "r":r,
    })


from django.shortcuts import render, redirect
from .models import Register, Book_Lawyer, Lawyer_Register, Payment_Details


def payment(request, Book_Id):
    if "User_Id" in request.session:
        user = request.session["User_Id"]
        try:
            register_instance = Register.objects.get(User_Id=user)
            Lawyer = Book_Lawyer.objects.get(Book_Id=Book_Id)
            Lawyer_details = Lawyer_Register.objects.get(Name=Lawyer.Lawyer_Name)
        except (Register.DoesNotExist, Book_Lawyer.DoesNotExist, Lawyer_Register.DoesNotExist):
            return redirect("payment")

        if request.method == "POST":
            CardName = request.POST.get('CardName')
            CardNumber = request.POST.get('CardNumber')
            CardExpiryMonth = request.POST.get('CardExpiryMonth')
            CardExpiryYear = request.POST.get('CardExpiryYear')
            CardCvv = request.POST.get('CardCVV')

            Payment_Details.objects.create(
                Book=Lawyer,
                User=register_instance,
                CardName=CardName,
                CardNumber=CardNumber,
                CardExpiryMonth=CardExpiryMonth,
                CardExpiryYear=CardExpiryYear,
                Cvv=CardCvv,
                Price=Lawyer_details.Price
            )

            # After processing payment, render the same template with success context
            context = {
                'Lawyer': Lawyer,
                'Lawyer_details': Lawyer_details,
                'Payment_Status': "Payment Successful, Appointment Booked!",
                'payment_success': True
            }
            return render(request, "AppointmentPayment.html", context)

        # For GET request, render the form without payment success
        context = {
            'Lawyer': Lawyer,
            'Lawyer_details': Lawyer_details,
        }
        return render(request, "AppointmentPayment.html", context)
    else:
        return redirect("login")  # Redirect to login if user is not authenticated

def booking_history(request):
    # Handle POST requests (from search, filter, or sort forms)
    if "User_Id" in request.session and request.method == "POST":

        # Get filter, sort, and search parameters from POST data
        filter_data = request.POST.get("Filter", "All")
        sort = request.POST.get("Sort", "All")
        search = request.POST.get("Search", "")

        # Construct query parameters for redirection
        query_params = {
            "Filter": filter_data,
            "Sort": sort,
        }
        if search:
            query_params["Search"] = search

        # Redirect to GET request with query parameters
        query_string = '&'.join([f'{k}={v}' for k, v in query_params.items()])
        return redirect(f"{request.path}?{query_string}")

    # Handle GET requests
    # Retrieve all Basic_Laws objects
    User = request.session["User_Id"]
    r = Register.objects.get(User_Id=User)
    lawyer = Book_Lawyer.objects.filter(User=r.User_Id)

    # Get filter, sort, search, and page parameters from GET data
    filter_data = request.GET.get("Filter", "All")
    sort = request.GET.get("Sort", "All")
    search = request.GET.get("Search", "")
    page_number = request.GET.get("page", 1)

    # Apply search filter if provided
    if search:
        lawyer = lawyer.filter(Law_Title__icontains=search)

    # Apply category filter if not 'All'
    if filter_data != "All":
        lawyer = lawyer.filter(Law_Category=filter_data)

    # Apply sorting
    if sort == "Name_asc":
        lawyer = lawyer.order_by("Law_Title")
    elif sort == "Name_desc":
        lawyer = lawyer.order_by("-Law_Title")

    # Paginate the results (6 items per page)
    paginator = Paginator(lawyer, 6)
    page_obj = paginator.get_page(page_number)

    # Render the template with context
    return render(request, "BookingHistory.html", {
        "page_obj": page_obj,
        "Filter": filter_data,
        "Sort": sort,
        "Search": search,
        "r": r,
    })

def case_history(request):

    # Handle POST requests (from search, filter, or sort forms)
    if "User_Id"  in request.session and request.method == "POST":

        # Get filter, sort, and search parameters from POST data
        filter_data = request.POST.get("Filter", "All")
        sort = request.POST.get("Sort", "All")
        search = request.POST.get("Search", "")

        # Construct query parameters for redirection
        query_params = {
            "Filter": filter_data,
            "Sort": sort,
        }
        if search:
            query_params["Search"] = search

        # Redirect to GET request with query parameters
        query_string = '&'.join([f'{k}={v}' for k, v in query_params.items()])
        return redirect(f"{request.path}?{query_string}")

    # Handle GET requests
    # Retrieve all Basic_Laws objects
    User = request.session["User_Id"]
    r = Register.objects.get(User_Id=User)
    user = User_Details.objects.get(User=r.User_Id)
    Cases = Case_Details.objects.filter(Case=user.Case_Id)

    # Get filter, sort, search, and page parameters from GET data
    filter_data = request.GET.get("Filter", "All")
    sort = request.GET.get("Sort", "All")
    search = request.GET.get("Search", "")
    page_number = request.GET.get("page", 1)

    # Apply search filter if provided
    if search:
        Cases = Cases.filter(Law_Title__icontains=search)

    # Apply category filter if not 'All'
    if filter_data != "All":
        Cases = Cases.filter(Law_Category=filter_data)

    # Apply sorting
    if sort == "Name_asc":
        Cases = Cases.order_by("Law_Title")
    elif sort == "Name_desc":
        Cases = Cases.order_by("-Law_Title")

    # Paginate the results (6 items per page)
    paginator = Paginator(Cases, 6)
    page_obj = paginator.get_page(page_number)


    # Render the template with context
    return render(request, "RegisteredCases.html", {
        "page_obj": page_obj,
        "Filter": filter_data,
        "Sort": sort,
        "Search": search,
        "r":r,
    })


# Create your views here.



# Create your views here.
