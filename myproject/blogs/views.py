from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm
from django.urls import reverse_lazy


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_header(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        posts = self.list(request, *args, **kwargs)  # Retrieve list of posts
        context = {'posts': posts.data}  # Create context for the template
        return render(request, 'posts/post_list.html', context)  # Render the template

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        slug = self.kwargs['slug']
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


    def get(self, request, slug, *args, **kwargs):
        post = self.retrieve(request, slug, *args, **kwargs)
        context = {'post': post.data}  # Create context for the template
        return render(request, 'posts/post_detail.html', context)  # Render the template
    
    def destroy(self, request, slug=None, *args, **kwargs):
        instance = self.get_object()  # Retrieve post object
        self.perform_destroy(instance)  # Delete the post
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated] 
    serializer_class = PostSerializer

    def delete(self, request, slug, *args, **kwargs):
        try:
            post = Post.objects.get(slug=slug)
            # Check if the user owns the post or is admin (optional)
            if not (post.author == self.request.user or self.request.user.is_staff):
                return Response({'error': 'You are not authorized to delete this post'}, status=status.HTTP_403_FORBIDDEN)
            post.delete()
            return Response({'message': 'Post Delete successful!'}, status=status.HTTP_204_NO_CONTENT)
        
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, slug, *args, **kwargs):
        self.delete(self, request, slug, *args, **kwargs)
        return Response({'message': 'Post!'})
    def get(self, request, slug, *args, **kwargs):
        self.delete(self, request, slug, *args, **kwargs)
        return Response({'message': 'Get!'})
    
class PostCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Set the current user as the author

from rest_framework.views import APIView

class PostEditView(APIView):
    permission_classes = [IsAuthenticated]


    def get_object(self, slug):
        try:
            post = Post.objects.get(slug=slug)
            # Check if the user owns the post or is admin (optional)
            if not (post.author == self.request.user or self.request.user.is_staff):
                return Response({'error': 'You are not authorized to edit this post'}, status=status.HTTP_403_FORBIDDEN)
            return post
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    

    def get(self, request, slug, *args, **kwargs):
        post = self.get_object(slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, slug, *args, **kwargs):
        post = self.get_object(slug)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# login and logout view

# signup page


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, './registration/signup.html', {'form': form})



# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect("post-list")
    else:
        form = LoginForm()
    return render(request, './registration/login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)
    


class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        try:
            post = Post.objects.get(slug=slug)
            serializer = CommentSerializer(data=request.data)  # Assuming CommentSerializer is defined elsewhere
            if serializer.is_valid():
                serializer.save(post=post, author=request.user)  # Set post and current user as author
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
