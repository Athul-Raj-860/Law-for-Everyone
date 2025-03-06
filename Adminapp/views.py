
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from Adminapp.models import Register, User_Details, Case_Details, Lawyer_Register, Basic_Laws, Book_Lawyer, Payment_Details, \
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

                User_Details.objects.create(User=user,Name=Name,Number=Number,Email=Email,Address=Address,City=City,
                                            State=State)
                Case_Details.objects.create(Complaint_Type=Complaint_Type,Complaint_Subject=Complaint_Subject,Complaint_Area=Complaint_Area,Complaint_Date=Complaint_Date,
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
        return render(request,"EmergencyNumbers.html",{'Num':Num ,'r':r})

def book_lawyer1(request):
    LawyersNames = Lawyer_Register.objects.values('Name','Category')
    if "User_Id" in request.session and request.method == "POST":
        user = request.session["User_Id"]
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
            User=user,
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
            User=user,
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

def payment(request,Book_Id):

        Lawyer = Book_Lawyer.objects.get(Book_Id=Book_Id)
        Lawyer_details = Lawyer_Register.objects.get(Name=Lawyer.Lawyer_Name)
        if "User_Id" in request.session and request.method == "POST":
            user = request.session["User_Id"]
            CardName = request.POST.get('CardName')
            CardNumber = request.POST.get('CardNumber')
            CardExpiryMonth = request.POST.get('CardExpiryMonth')
            CardExpiryYear = request.POST.get('CardExpiryYear')
            Cvv = request.POST.get('CVV')


            Payment_Details.objects.create(Book_Id=Book_Id,User=user,CardName=CardName,CardNumber=CardNumber,CardExpiryMonth=CardExpiryMonth,
                                           CardExpiryYear=CardExpiryYear,Cvv=Cvv,Price=Lawyer_details.Price)
            context = {
                'Lawyer': Lawyer,
                'Lawyer_details': Lawyer_details,
                'Payment_Status': "Payment Successful, Appointment Booked!"
            }
            return render(request,"AppointmentPayment.html",context)
        return render(request,"AppointmentPayment.html",{'Lawyer':Lawyer,'Lawyer_details':Lawyer_details})

def booking_history(request):
    if "User_Id" in request.session:
        User_Id = request.session["User_Id"]
        r = Register.objects.get(User_Id=User_Id)
        Lawyer = Book_Lawyer.objects.all()
        Lawyer_details = []
        for lawyer in Lawyer:
            try:
                lawyer_detail = Lawyer_Register.objects.get(Name=lawyer.Lawyer_Name)
                Lawyer_details.append(lawyer_detail)
            except Lawyer_Register.DoesNotExist:
                continue

        return render(request, "BookingHistory.html", {'Lawyer': Lawyer, 'r': r, 'Lawyer_details': Lawyer_details})

def case_history(request):
    if "User_Id" in request.session:
        User_Id = request.session["User_Id"]
        r = Register.objects.get(User_Id=User_Id)
        print(r)
        user = User_Details.objects.get(User=r.User_Id)
        print(user)
        cases = Case_Details.objects.filter(Case_Id=user.Case_Id)

        return render(request, "BookingHistory.html", {'cases':cases , 'r': r})
# Create your views here.

