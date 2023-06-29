from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics,status
from .serializers import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class UserRegistrationView(generics.GenericAPIView):
    serializer_class = NewUserSerializer
    def post(self, request, format=None):
       
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)
    

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        userdata = request.data
        # user1 = MyUser.objects.get(name=user['name'])
        # print(user1)
        serializer = self.serializer_class(data=userdata)
        valid = serializer.is_valid(raise_exception=True)
       

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LikeView(generics.GenericAPIView):
    serializer_class = LikeListSerializer
    # test=Like.objects.filter(post=14).count()
    # print('.............',test)
    
    def get(self,request):
            data = request.data
            like = Like.objects.all()
            count=0
            for i in like:
                 count +=1
                 
            serializer = LikeListSerializer(like, many=True)
            response = {
                'total likes ':count,
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched likes',
                'likes': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)
class LikeUpdateView(generics.GenericAPIView):
    serializer_class = LikeListSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, pk, format=None):
        user = request.user
        try:
            if user.role == 'admin':
                item =  Like.objects.get(pk=pk)
                item.delete()
                return Response({
                    'message': 'Like Deleted Successfully'
                })
            else:
                response = {
                    # 'success': False,
                    # 'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status.HTTP_403_FORBIDDEN)
        except:
            return Response("Department cannot be deleted")

class AllPostView(generics.GenericAPIView):
    serializer_class = PostSerializer

    def get(self,request):
            user = request.user
            item = Post.objects.filter(status='public')
            
           
            test=Post.objects.filter(liked_by=1).count()
            
            print('.......................',test)
            count=0
            for i in item:
                 count +=1
                 
            serializer = PostListSerializer(item, many=True)
            response = {
                'total published Posts':count,
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched posts',
                'posts': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)

class PostView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        data = request.data
        if data is not None:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(author=user)
            user_data = serializer.data

            return Response(user_data, status=status.HTTP_201_CREATED)
        else:
                response = {
                    # 'success': False,
                    # 'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status.HTTP_403_FORBIDDEN)
        
    def get(self,request):
            user = request.user
        # try:
            if user is not None:
                item = Post.objects.filter(author=user)
                count=0
                for i in item:
                    count +=1
                serializer = PostListSerializer(item, many=True)
                response = {
                    'total users post':count,
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': 'Successfully fetched posts',
                    'posts': serializer.data

                }
                return Response(response, status=status.HTTP_200_OK)
                
            else:
                response = {
                    # 'success': False,
                    # 'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'there is some error'
                }
                return Response(response, status.HTTP_403_FORBIDDEN)
            
    def put(self, request, pk=None, format=None):
            user = request.user
            if user is not None:
                update = Post.objects.get(pk=pk)
                if update.author == user:
                    serializer = self.serializer_class(instance=update,data=request.data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save(updated_on=True)
                    response = Response()
                    response.data = {
                        'message': 'Post Updated Successfully',
                        'data': serializer.data
                    }

                    return response
                else:
                     response = {"message": "you cannot update the post as your are not the author"}
                     return Response(response)
            else:
                response = {
                    
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status.HTTP_403_FORBIDDEN)
            
class PostUpdateView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk=None, format=None):
            user = request.user
            if user.role == 'admin':
                update = Post.objects.get(pk=pk)
                
                serializer = self.serializer_class(instance=update,data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save(updated_on=True)
                response = Response()
                response.data = {
                    'message': 'Post Updated Successfully',
                    'data': serializer.data
                }

                return response
            
            else:
                response = {
                    
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status.HTTP_403_FORBIDDEN)
            
    def delete(self, request, pk, format=None):
        user = request.user
        if user.role == 'admin':
            item =  Post.objects.get(pk=pk)
            print("user.......",user.role)
            item.delete()
            return Response({
                'message': 'Post Deleted Successfully'
            })
        else:
            response = {
                # 'success': False,
                # 'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)

class UserView(generics.GenericAPIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
       
        users = User.objects.get(email=user)
        serializer = self.serializer_class(users)
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Successfully fetched user Profile',
            'users': serializer.data

        }
        return Response(response, status=status.HTTP_200_OK)
    
    def put(self, request, format=None):
            user = request.user
            if user is not None:
                update = User.objects.get(email=user)
                serializer = self.serializer_class(instance=update,data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save(updated_on=True)
                response = Response()
                response.data = {
                    'message': 'User Profile Updated Successfully',
                    'data': serializer.data
                }

                return response
                
            else:
                response = {
                    
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status.HTTP_403_FORBIDDEN)
    
class UserListView(generics.GenericAPIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role != 'admin':
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = User.objects.filter(role='user')
            serializer = self.serializer_class(users, many=True)
            count=0
            for i in users:
                 count +=1
            response = {
                'total user': count,
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)
        
class UserUpdateView(generics.GenericAPIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    
    def put(self, request, pk=None, format=None):
            user = request.user
            if user.role == 'admin':
                update = User.objects.get(pk=pk)
                serializer = self.serializer_class(instance=update,data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save(last_update_at=True)
                response = Response()
                response.data = {
                    'message': 'User Updated Successfully',
                    'data': serializer.data
                }

                return response
            else:
                response = {
                    
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        user = request.user
        try:
            if user.role == 'admin':
                item =  User.objects.get(pk=pk)
                item.delete()
                return Response({
                    'message': 'Users Deleted Successfully'
                })
            else:
                response = {
                
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status.HTTP_403_FORBIDDEN)
        except:
            return Response("User cannot be deleted")



    def get(self,request,pk):
            user = request.user
            if user.role == 'admin':
                    item = User.objects.get(pk=pk)
                
                    serializer = self.serializer_class(item)
                    response = {
                        'success': True,
                        'status_code': status.HTTP_200_OK,
                        'message': 'Successfully fetched User',
                        'Users': serializer.data

                    }
                    return Response(response, status=status.HTTP_200_OK)
                
            else:
                response = {
                    
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status.HTTP_403_FORBIDDEN)
        
