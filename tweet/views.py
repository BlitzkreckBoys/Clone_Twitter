# from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
# from django.urls import reverse_lazy
# from django.views.generic import View, UpdateView, ListView
# from django.http import JsonResponse
# from django.core.paginator import Paginator
# from .models import Tweet
# from .forms import TweetForm
# # Create your views here.
# class HomeView(View):
#     """ Home view for the profile"""
#     def get(self, request, *args, **kwargs):
#         """ for the profile view """
#         if request.user.is_authenticated:
#             tweet_form = TweetForm()
#             tweets = Tweet.objects.filter(
#                 user__in=request.user.profile.follows.values_list('id', flat=True)
#             ).order_by('-created_at')
#             user_tweets = Tweet.objects.filter(user=request.user)
#             tweets = tweets | user_tweets
#             tweets = tweets.order_by('-created_at')

#             # Pagination
#             paginator = Paginator(tweets, 10)  # Show 10 tweets per page
#             page_number = request.GET.get('page')
#             page_obj = paginator.get_page(page_number)

#             return render(request, 'home.html', {
#                 'tweet_form': tweet_form,
#                 'page_obj': page_obj,
#             })
#         return redirect('login')

#     def post(self, request, *args, **kwargs):
#         """ Handle tweet submission """
#         if request.user.is_authenticated:
#             tweet_form = TweetForm(request.POST, request.FILES)
#             if tweet_form.is_valid():
#                 tweet = tweet_form.save(commit=False)
#                 tweet.user = request.user
#                 tweet.save()
#                 return redirect('home')
#         return redirect('login')
# class FollowingTweetsView(ListView):
#     """List of tweets from users I follow"""
#     model = Tweet
#     template_name = 'tweets_list.html'
#     context_object_name = 'tweets'

#     def get_queryset(self):
#         user = self.request.user
#         followed_profiles = user.profile.follows.all()  # This returns a QuerySet of Profile objects
#         followed_users = User.objects.filter(profile__in=followed_profiles)  # This converts it to a QuerySet of User objects
#         return Tweet.objects.filter(user__in=followed_users).order_by('-created_at')
# class LikeTweetView(View):
#     def post(self, request, tweet_id):
#         try:
#             tweet = Tweet.objects.get(id=tweet_id)
#         except Tweet.DoesNotExist:
#             return JsonResponse({'error': 'Tweet not found'}, status=404)
#         user = request.user
#         if user.is_authenticated:
#             if user in tweet.likes.all():
#                 tweet.likes.remove(user)
#                 liked = False
#             else:
#                 tweet.likes.add(user)
#                 liked = True
#             return JsonResponse({'liked': liked, 'likes_count': tweet.likes.count()})
#         return JsonResponse({'error': 'User not authenticated'}, status=401)
# class TweetUpdateView(UpdateView):
#     model = Tweet
#     form_class = TweetForm
#     template_name = 'edit_tweet.html'
#     success_url = reverse_lazy('home')  # Redirect to home after successful update

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(user=self.request.user)  # Ensure users can only edit their own tweets

#     def form_valid(self, form):
#         # You can add additional logic here if needed
#         return super().form_valid(form)