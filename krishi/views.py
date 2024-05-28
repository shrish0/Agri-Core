from django.shortcuts import render,redirect
from .models import *
import time
from django.contrib import messages
from django.http import HttpResponse
from account.models import *
from .forms import *
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
# from django.http import JsonResponse
# Create your views here.
from django.conf import settings
from django.http import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import joblib
import pandas as pd
import numpy as np

# Load the trained model


@csrf_exempt
def predict_crop(request):
    if request.method == 'POST':
        model = joblib.load('plant_suggestion_random_forest_model.pkl')
        # Extract input values from the POST request
        
        season = request.POST.get('season')
        state = request.POST.get('state')
        area = float(request.POST.get('area'))
        production = float(request.POST.get('production'))
        annual_rainfall = float(request.POST.get('annual_rainfall'))
        fertilizer = float(request.POST.get('fertilizer'))
        pesticide = float(request.POST.get('pesticide'))
        
        # Create a DataFrame with the input values
        input_data = pd.DataFrame({
            'Season': [season],
            'State': [state],
            'Area': [area],
            'Production': [production],
            'Annual_Rainfall': [annual_rainfall],
            'Fertilizer': [fertilizer],
            'Pesticide': [pesticide]
        })
        
        # Perform one-hot encoding for categorical variables
        input_encoded = pd.get_dummies(input_data)
        
        # Use the trained model to make predictions
        predicted_probabilities = model.predict_proba(input_encoded)
        crop_labels = model.classes_
        top_three_indices = np.argsort(predicted_probabilities, axis=1)[:, -3:][:, ::-1]
        top_three_crops = crop_labels[top_three_indices][0]
        
        # Return the predicted crops as JSON response
        return JsonResponse({'top_three_crops': top_three_crops.tolist()})
    
    else:
        return JsonResponse({'error': 'POST method required'})

def home(request):
    print(settings.DJANGO_SERVER_IP)
    return render(request,"index.html",{'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def index(request):
    return redirect("/")

def update_or_delete_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            product = selling.objects.get(pk=product_id)
            
            # Check if the user making the request is the owner of the product
            if request.user != product.username:
                messages.error(request, 'You are not authorized to update or delete this product.')
                return redirect('/profile.html')
            
            if 'delete_product' in request.POST:
                # If the delete checkbox is checked, delete the product
                product.delete()
                messages.success(request, 'Product deleted successfully.')
            else:
                # If the delete checkbox is not checked, update the product
                new_product_name = request.POST.get('new_product_name')
                new_product_price = request.POST.get('new_product_price')

                if new_product_name:
                    product.name = new_product_name
                if new_product_price:
                    product.price = new_product_price

                product.save()
                messages.success(request, 'Product updated successfully.')
        except selling.DoesNotExist:
            messages.error(request, 'Product does not exist.')
        
        return redirect('/profile.html')
    else:
        # Handle GET request or return an error
        return redirect('/')

def show(request,id):
    query = request.POST.get('query')
    print(query)
    # Perform your search logic here
    if(query):
       results = (selling.objects.filter(productdet__icontains=query)).order_by('price')
    else:
       results = selling.objects.all().order_by('price')
    return render(request,"show.html",{"sell1":results,"id":id,'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def sell(request):
    if request.method=="POST":
        img=request.FILES['filename']
        product=request.POST['product']
        productdet=request.POST['productdet']
        quantity=request.POST['quantity']
        price=request.POST['price']
        phone=request.POST['Phone']
        email=request.POST['email']
        username=request.POST['username']
        seller1=selling(username=username,img=img,product=product,productdet=productdet,quantity=quantity,price=price,email=email,phone=phone)
        seller1.save()
        return render(request,"sell.html",{'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

    return render(request,"sell.html",{'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def plant(request):
     if request.method=="POST":
         return 
     return render(request,"plant-disease-detection.html",{'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def plant1(request):
     if request.method=="POST":
         return 
     return redirect("/plant-disease-detection.html")

def about(request):
    return render(request,"about.html",{'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def about1(request):
    return redirect("/about.html")

def daily_news(request):
    return render(request,"daily_news.html",{'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def daily_news1(request):
    return redirect("/daily_news.html")

def weather(request):
    return render(request,"weather.html",{'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})
def weather1(request):
    return redirect("/weather.html")

def weather_finder(request):
    return render(request,"weatherapp.html",{'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def tourism(request):
    agricultural_sites = AgriculturalSite.objects.all()
    sites_with_images = []
    for site in agricultural_sites:
        images = SiteImage.objects.filter(site=site)
        sites_with_images.append({'site': site, 'images': images})
        print(site.location)

    return render(request,"tourism.html",{'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP, 'sites_with_images': sites_with_images})

def product(request):
    items=item.objects.all()
    return render(request,"products.html",{"items":items,'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})
def product1(request):
   return redirect("/products.html")
def blog(request):
    return render(request,"blog.html",{'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})
def login(request):
    return render(request,"login.html",{'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def counsell(request):
     if request.method == 'POST':
        form = CounselForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")  # Redirect to a success page
     else:
        form = CounselForm(user=request.user)
     return render(request, 'counselling.html', {'form': form,'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def counsell1(request):
    return redirect("/counselling.html")

def feedback1(request):
    if request.method=="POST":
        form=FeedbackForm(request.POST)
        if form.is_valid():
                form.save()
                return redirect("/")
    form = FeedbackForm(user=request.user)
    return render(request, 'counselling.html', {'form': form,'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})    

def preprocess_image(input_image):
    # Implement the necessary pre-processing steps based on your model requirements
    image = Image.open(input_image)
    # Resize, normalize, etc.
    resized_image = image.resize((224, 224))
    # Convert the image to a NumPy array
    processed_image = np.array(resized_image) / 255.0  # Normalize to [0, 1]

    return processed_image

def interpret_prediction(prediction):
    # Implement the interpretation logic based on your model's output format
    class_index = np.argmax(prediction)
    classes=['Apple Apple scab',
             'Apple Black rot',
             'Apple Cedar apple_rust',
             'Apple healthy', 
             'Blueberry healthy', 
             'Cherry(including sour) Powdery mildew', 
             'Cherry(including sour) healthy', 
             'Corn (maize) Cercospora leaf spot Gray leaf spot', 
             'Corn (maize) Common rust', 
             'Corn (maize) Northern Leaf Blight', 
             'Corn (maize) healthy', 
             'Grape Black_rot', 
             'Grape Esca (Black Measles)',  
             'Grape Leaf blight (Isariopsis Leaf Spot)', 
             'Grape healthy',
             'Orange Haunglongbing (Citrus greening)', 
             'Peach Bacterial_spot', 
             'Peach healthy', 
             'Pepper, bell Bacterial_spot', 
             'Pepper, bell healthy', 
             'Potato Early blight',  
             'Potato Late blight',
             'Potato healthy', 
             'Raspberry healthy', 
             'Soybean healthy', 
             'Squash Powdery mildew', 
             'Strawberry Leaf scorch',
             'Strawberry healthy',  
             'Tomato Bacterial spot', 
             'Tomato Early blight', 
             'Tomato Late blight',
             'Tomato Leaf Mold' , 
             'Tomato Septoria leaf spot', 
             'Tomato Spider mites Two-spotted spider mite',
             'Tomato Target Spot', 
             'Tomato Tomato Yellow Leaf Curl Virus', 
             'Tomato Tomato mosaic virus', 
             'Tomato healthy']
    result = classes[class_index]
    return result

def disease_prediction_view(request):
    if request.method == 'POST':
        try:
            input_image = request.FILES['image']
            
            # Perform some pre-processing on the image (resize, normalize, etc.)
            processed_image = preprocess_image(input_image)

            # Make predictions using the loaded model
            model = load_model('plant_disease_model.h5')
            prediction = model.predict(np.expand_dims(processed_image, axis=0))[0]

            # Convert the prediction to a human-readable result (adjust as needed)
            result1 = interpret_prediction(prediction)
            result=PlantResult.objects.filter(name=result1).all()
            print(result)
            print(result1)
            if "healthy" in result1:
                result = {"name2": result1.split(" ")}
                
            return render(request, 'result.html', {'result1':result1,'result': result,'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})
        except Exception as e:
            # Redirect to the plant-disease-detection.html page with an alert message
            messages.error(request, f"An error occurred while processing the image: try with another pic ")
            return redirect('disease_prediction')

    return render(request, 'plant-disease-detection.html',{'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def feedback1(request):
      if request.method == 'POST':
            Full_Name=request.POST["Full Name"]
            Email=request.POST["Email"]
            Phone_Number=request.POST["Phone Number"]
            message=request.POST["message"]
            page=request.POST["page"]
            contact=feedback(first_name=Full_Name,email=Email,phone=Phone_Number,message=message)
            contact.save()
            return JsonResponse({'message': 'Success'})
      else:
        # Handle other HTTP methods
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    

def news(request):
    Email=request.POST["Email"]
    page=request.POST["page"]
    email1=newsletter(email=Email)
    email1.save()
    return render(request,page+".html",{'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def counselling(request):
    firstname=request.POST["firstname"]
    lastname=request.POST["lastname"]
    Email=request.POST["mail"]
    Phone_Number=request.POST["Phone"]
    address=request.POST["local address"]
    state=request.POST["state"]
    postal=request.POST["postal code"]
    contact=feedback(first_name=firstname,email=Email,phone=Phone_Number,local_address=address,state=state,postal_code=postal,last_name=lastname)
    contact.save()
    return render(request,"contact.html",{'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def policy_list(request):
    # Fetch all policies from the database
    policies = Policy.objects.all()
    
    # Initialize an empty list to store policy-point pairs
    policy_point_pairs = []
    
    # Iterate through each policy and split its content into points
    for policy in policies:
        points = policy.policy_content.split(' $ ')
        # Append a tuple containing the policy and its points to the list
        policy_point_pairs.append((policy, points))
    
    # Pass the list of policy-point pairs to the template context
    return render(request, 'policy_list.html', {'policy_point_pairs': policy_point_pairs,'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def back(request):
    redirect("/")

def delete_slot(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            slot = counsel.objects.get(pk=product_id)
            
            # Check if the user making the request is the owner of the slot
            if request.user.email == slot.email:
                slot.delete()
                messages.success(request, 'Slot deleted successfully.')
            else:
                messages.error(request, 'You are not authorized to delete this slot.')
        except counsel.DoesNotExist:
            messages.error(request, 'Slot does not exist.')
        
    return redirect('/profile.html')


def create_agricultural_site(request):
    if request.method == 'POST':
        form = AgriculturalSiteForm(request.POST, user=request.user)
        image_formset = SiteImageFormSet(request.POST, request.FILES)
        if form.is_valid() and image_formset.is_valid():
            # Save the AgriculturalSite instance
            agricultural_site = form.save(commit=False)
            agricultural_site.save()

            # Save the images associated with the site
            for form in image_formset:
                if form.cleaned_data.get('image'):
                    image = form.save(commit=False)
                    image.site = agricultural_site
                    image.save()

            return redirect('/profile.html')  # Redirect to success page
    else:
        form = AgriculturalSiteForm(user=request.user,id=request.user.id)
        image_formset = SiteImageFormSet()

    # Fetch all registered agricultural sites and their associated images
    agricultural_sites = AgriculturalSite.objects.filter(owner_id=request.user.id).all()
    sites_with_images = []
    
    for site in agricultural_sites:
        images = SiteImage.objects.filter(site=site)
        sites_with_images.append({'site': site, 'images': images})
        print(site.location)

    return render(request, 'create_agricultural_site.html', {'form': form, 'image_formset': image_formset,'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def profile(request):
   # Filter the Selling objects based on the user's email
    sell_objects =selling.objects.filter(email=request.user.email).all()

    counsel_objects =counsel.objects.filter(email=request.user.email).all()

    form = AgriculturalSiteForm(user=request.user,id=request.user.id)
    image_formset = SiteImageFormSet()

    # Fetch all registered agricultural sites and their associated images
    agricultural_sites = AgriculturalSite.objects.filter(owner_id=request.user.id).all()
    sites_with_images = []
    
    for site in agricultural_sites:
        images = SiteImage.objects.filter(site=site)
        sites_with_images.append({'site': site, 'images': images})
        print(site.location)

    return render(request, "profile.html", {'sell1': sell_objects,'counsel':counsel_objects,'form': form, 'image_formset': image_formset, 'sites_with_images': sites_with_images,'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def delete_farm(request):
    if request.method == 'POST':
        farm_id = request.POST.get('farm_id')
        print(request.user.id)
        try:
            farm = AgriculturalSite.objects.get(pk=farm_id)
            print(farm.owner_id)
            # print(farm.owner_id)
            # img= SiteImage.objects.get(site_id=farm.owner)
            # Check if the user making the request is the owner of the farm
            if request.user.id != farm.owner_id:
                messages.error(request, 'You are not authorized to delete this farm.')
            else:
                farm.delete()
                messages.success(request, 'Farm deleted successfully.')
        except AgriculturalSite.DoesNotExist:
            messages.error(request, 'Farm does not exist.')
        
    return redirect('/profile.html')


def search_results(request,id):
    query = request.GET.get('query')
    # Perform your search logic here
    results = selling.objects.filter(productdet__icontains=query)
    return render(request, 'show.html', {'sell1': results,'id':id,'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})

def FaQs(request):
    qna_data = FaQ.objects.all()
    return render(request, 'FaQ.html', {'qna_data': qna_data,'DJANGO_SERVER_IP': settings.DJANGO_SERVER_IP})
