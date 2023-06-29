from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


 # custom user models
class UserManager(BaseUserManager):
    def create_user(self, email,password=None , password2=None):
        """
        Creates and saves a User with the given email,name,tc,and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, name,tc and password.
        """
        user = self.create_user(
            email,
            password=password,
            
        )
        user.is_admin = True
        user.is_active =True
        user.name = 'admin'
        user.role = 'admin'
        user.save(using=self._db)
        return user
    

    # Custom User Manager
class User(AbstractBaseUser):
    DESIG = [
        ('admin', 'admin'),
        ('user', 'user'),
        ]
    
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=20,blank=False,null=False)
    mobile_number = models.CharField(max_length=17,blank=False)
    liked = models.ManyToManyField('Post', through='Like')

    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(choices=DESIG, max_length=200, default='user')
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    last_update_at = models.DateTimeField(auto_now=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    

STATUS = (
    ('private',"Draft"),
    ('public',"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    description = models.CharField(max_length=100)
    content = models.TextField()
    post_image = models.ImageField(upload_to='upload/')
    liked_by = models.ManyToManyField(User, through='Like')
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200,choices=STATUS, default='private')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    

class Like(models.Model):
    # likes = models.IntegerField()
    post = models.ForeignKey(Post, on_delete= models.CASCADE,related_name='posts')
    liked_by = models.ForeignKey(User, on_delete= models.CASCADE,related_name='like_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    last_update_at = models.DateTimeField(auto_now=True)

    def number_of_likes(self):
        return self.likes.count()
