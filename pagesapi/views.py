from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from django.http import Http404



# class ContactView(viewsets.ModelViewSet):
#     queryset = Contact.objects.all()
#     serializer_class = ContactSerializer   


class ContactView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
           
            limit = self.request.query_params.get('limit', None)
           


            queryset = Contact.objects.all()

            if limit:
                # If only "limit" parameter is provided, order by id and limit the queryset
                queryset = queryset.order_by('-id')[:int(limit)]
       
            return queryset
            # serializer = self.get_serializer(queryset, many=True)
            # return Response(serializer.data)
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class ContactViewDetail(APIView):
    def get_object(self, pk):
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        leave = self.get_object(pk)
        serializer = ContactSerializer(leave)
        return Response(serializer.data)

    def put(self, request, pk):
        leave = self.get_object(pk)
        serializer = ContactSerializer(leave, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        leave = self.get_object(pk)
        leave.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
from django.http import Http404
from django.db.models import Avg

class SellerReviewListCreateAPIView(APIView):
    def get(self, request, format=None):
        seller_id = request.query_params.get('seller_id')
        if seller_id:
            reviews = SellerReview.objects.filter(seller_id=seller_id)
            if not reviews:
                raise Http404("No reviews found for the specified seller_id.")
            avg_rating = reviews.aggregate(Avg('rating_value'))['rating_value__avg']
            serializer = SellerReviewSerializer(reviews, many=True)
            data = serializer.data
            data.append({'average_rating_value': avg_rating})
            return Response(data)
        else:
            reviews = SellerReview.objects.all()
            serializer = SellerReviewSerializer(reviews, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SellerReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# class TopSellerReviewsAPIView(APIView):
#     def get(self, request, format=None):
#         seller_id = request.query_params.get('seller_id')
#         if not seller_id:
#             return Response({"error": "seller_id parameter is required"}, status=400)

#         try:
#             reviews = SellerReview.objects.filter(seller_id=seller_id).order_by('-rating_value')[:10]
#             if not reviews:
#                 raise Http404("No reviews found for the specified seller_id.")
#             serializer = SellerReviewSerializer(reviews, many=True)
#             return Response(serializer.data)
#         except SellerReview.DoesNotExist:
#             raise Http404("Seller does not exist.")
from adsapi.serializers import *
class TopSellerReviewsAPIView(APIView):
   
    def post(self, request, *args, **kwargs):
        seller_id = request.data.get('seller_id')
        if seller_id:
            seller_reviews = SellerReview.objects.filter(seller_id=seller_id)
            rating_product_dict = {review.rating_value: review.product for review in seller_reviews}
            sorted_rating_values = sorted(rating_product_dict.keys(), reverse=True)  # Sort rating values
            sorted_product_ids = [rating_product_dict[rating_value] for rating_value in sorted_rating_values]
            
            # Limit to 10 responses
            limited_sorted_product_ids = sorted_product_ids[:10]
            
            # Serialize product_ids
            product_serializer = ProductSerializer(instance=limited_sorted_product_ids, many=True)
            serialized_product_ids = product_serializer.data
            
            return Response(serialized_product_ids, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Please provide seller_id in the request data"}, status=status.HTTP_400_BAD_REQUEST)
 # def post(self, request, format=None):
    #     # Get the seller_id from the request data
    #     seller_id = request.data.get('seller_id')

    #     # Fetch top 10 reviews with the highest rating_value for the given seller
    #     top_rated_reviews = SellerReview.objects.filter(seller_id=seller_id).order_by('-rating_value')[:10]

    #     # Extract product_ids from top rated reviews
    #     product_ids = [review.product_id.id for review in top_rated_reviews]

    #     # Fetch the products corresponding to the top rated reviews
    #     top_rated_products = Product.objects.filter(id__in=product_ids)

    #     # Serialize the queryset
    #     serializer = ProductSerializer(top_rated_products, many=True)

    #     return Response(serializer.data, status=status.HTTP_200_OK)
        
class UserAPIView(APIView):
    def get(self, request):
        limit = request.query_params.get('limit')  # Get the 'limit' parameter from the query string
        if limit:
            try:
                limit = int(limit)
            except ValueError:
                return Response({"error": "Invalid limit value. Must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
            users = User.objects.order_by('-id')[:limit]  # Slice the queryset to limit the number of records
        else:
            users = User.objects.all()

        serializer = UserSerializerNew(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UserDetailView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializerNew(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializerNew(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class TrafficList(APIView):
    def get(self, request):
        city = request.query_params.get('city')
        date = request.query_params.get('date')

        queryset = Traffic.objects.all()

        if city:
            queryset = queryset.filter(location__icontains=city)
        
        if date:
            queryset = queryset.filter(date=date)

        serializer = TrafficSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TrafficSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from paymentapi.models import *  
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

class NewUserPlanView(APIView):
    def post(self, request):
        user_id = request.data.get("user")
        user = get_object_or_404(User, id=user_id)

        # Check if the user has purchased a plan based on the Transaction model
        plan_purchased = TransactionDetails.objects.filter(userID=user, plan__isnull=False).exists()

        # if plan_purchased:
        #     # Execute the logic for a user who has purchased a plan
        #     transaction_success = self.process_transaction_after_plan(request)
			
        #     return Response({"message": "You have already purchased a plan. Enjoy using the ads!"})
			
        if plan_purchased:
            # Execute the logic for a user who has purchased a plan
            return self.process_transaction_after_plan(request) 
        # Check if the user is new and hasn't viewed any ads yet
        new_user_plan, created = NewCustomer.objects.get_or_create(userid=user)

        if created:
    # Set the initial value for free ads for new users
          new_user_plan.total_count = 10  # Set the initial total count for free ads
          new_user_plan.remaining_ads = new_user_plan.total_count  # Set remaining_ads initially
          new_user_plan.price = 0
          new_user_plan.plan_type = "Lead details"
          new_user_plan.validity = 30
          new_user_plan.save()
          return Response({"message": "Welcome! You are a new user. You have 10 free ads. Remaining Ads: {}".format(new_user_plan.remaining_ads)})

        # Check if the user has reached the free ads limit
        if new_user_plan.ads_count >= new_user_plan.total_count:
            return Response({"message": "You have viewed all free ads. Please purchase a plan to continue using ads."})

        # Your logic to process the transaction (replace the hardcoded True)
        transaction_success = self.process_transaction(request)

        if transaction_success:            
            new_user_plan.price=0
            # new_user_plan.plan_type="Lead details"
            new_user_plan.validity=30
            new_user_plan.ads_count += 1
            new_user_plan.remaining_ads = max(0, int(new_user_plan.total_count) - int(new_user_plan.ads_count))  # Convert to int before subtraction
            new_user_plan.save()
            # Check if the user has viewed all free ads
            if new_user_plan.ads_count == new_user_plan.total_count:
                return Response({"message": "You have viewed all free ads. Please purchase a plan to continue using ads."})

            return Response({"message": "Transaction successful! Ad details updated successfully. Total Ads Viewed: {}. Remaining Ads: {}".format(new_user_plan.ads_count, new_user_plan.remaining_ads)})
        else:
            return Response({"message": "Transaction failed! Please try again."}, status=status.HTTP_400_BAD_REQUEST)

    def process_transaction(self, request):
        # Your logic to process the transaction and determine its success or failure
        # Replace this with your actual logic to validate the transaction
        transaction_success = True  # Replace this line with your actual logic
        return transaction_success
    
    def process_transaction_after_plan(self, request):
     user_id = request.data.get("user")
     user = get_object_or_404(User, id=user_id)
     new_user_plan, created = NewCustomer.objects.get_or_create(userid=user)

     if not created:
        transaction_details = TransactionDetails.objects.filter(userID=user, plan__isnull=False).last()

        if transaction_details:
            ads_value = transaction_details.adsValue
            price = transaction_details.order_payment_amount
            validity = transaction_details.monthsVale
            order_id = transaction_details.payment_token_id
            print("Before update - Total Count:", new_user_plan.total_count)            
                # For the first purchase, set the initial total count
            new_user_plan.total_count = 10 + int(ads_value)
            # if ads_value==new_user_plan.total_count:
            #    new_user_plan.total_count + int(ads_value)            
            print("After update - Total Count:", new_user_plan.total_count)
		
            # Check if the plan has expired before incrementing ads_count
            if new_user_plan.ads_count == new_user_plan.total_count:
                return Response({"message": "Your plan has expired. Please purchase a new plan."})
            else:
                # Increment ads_count by 1
                new_user_plan.ads_count += 1
                new_user_plan.price = price
                new_user_plan.validity = validity
                new_user_plan.OrderID = order_id
                new_user_plan.save()

                total_ads_viewed = new_user_plan.ads_count
                remaining_ads = max(0, int(new_user_plan.total_count) - int(new_user_plan.ads_count))
                response_message = f"Ad viewed successfully. Total Ads Viewed: {total_ads_viewed}. Remaining Ads: {remaining_ads}"
                print(response_message)
                # print("Ad viewed successfully.")
                # print("Total Ads Viewed:", total_ads_viewed)
                # print("Remaining Ads:", remaining_ads)

                return  Response({
							"message": response_message,
							"IdValue": user.id,  # Replace with the actual attribute you want to include
							"PriceValue": new_user_plan.price,  # Replace with the actual attribute you want to include
							"AdsValue": new_user_plan.total_count  # Include the ads count or any other attribute you want
						})

        else:
            return JsonResponse({"message": "Transaction details not found."})
     else:
        return JsonResponse({"message": "NewUserPlan not created."})






# ********************************************************************************************************





from rest_framework.permissions import IsAuthenticated
class SendMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MessageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReceiveMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        received_messages = Message.objects.filter(receiver=user)
        serializer = MessageSerializer(received_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ConversationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = request.user
        other_user = get_object_or_404(User, id=user_id)

        sent_messages = Message.objects.filter(sender=user, receiver=other_user)
        received_messages = Message.objects.filter(sender=other_user, receiver=user)

        messages = (sent_messages | received_messages).order_by('timestamp')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
from django.contrib.messages import constants as message_constants
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.messages import get_messages


@receiver(post_save, sender=Message)
def message_notification(sender, instance, created, **kwargs):
    if created and not instance.is_system_message:
        # Create a notification message for the receiver
        NotificationMessage.objects.create(
            receiver=instance.receiver,
            content="You have a new message from {}".format(instance.sender.name)
        )

class NotificationListAPIView(APIView):
    def get(self, request):
        user = request.user
        notifications = NotificationMessage.objects.filter(receiver=user)
        serializer = NotificationMessageSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
        
class EditMessageAPIView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    
    
class AdsCommentListView(APIView):
    def post(self, request):
        ads_id = request.data.get('ads_id', None)  # Assuming the ads_id is provided in the request data
        if ads_id is None:
            return Response({"error": "Ads ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ads_comments = AdsComment.objects.filter(ads_id=ads_id)
            total_ratings = ads_comments.aggregate(total_ratings=models.Sum('rating'))['total_ratings']
            total_comments = ads_comments.count()

            if total_comments > 0:
                average_rating = total_ratings / total_comments
                return Response({"average_rating": average_rating}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No comments found for the specified ad ID"}, status=status.HTTP_404_NOT_FOUND)
        except AdsComment.DoesNotExist:
            return Response({"error": "Ads not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
