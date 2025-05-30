from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group

class Gender(models.TextChoices):
    MALE = 'male', _('Male')
    FEMALE = 'female', _('Female')
    UNSPECIFIED = 'unspecified', _('Unspecified')

class Role(models.Model):
    """
    Custom Role model that extends Group functionality
    """
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    display_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __str__(self):
        return self.display_name or self.group.name

    @property
    def name(self):
        return self.group.name

    @property
    def permissions(self):
        return self.group.permissions

class ExtendedPermission(models.Model):
    """
    Extended Permission model to add extra info.
    """
    permission = models.OneToOneField(Permission, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('extended permission')
        verbose_name_plural = _('extended permissions')

    def __str__(self):
        return self.permission.name

    @property
    def name(self):
        return self.permission.name

    @property
    def codename(self):
        return self.permission.codename

    @property
    def content_type(self):
        return self.permission.content_type

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('full name'), max_length=255)
    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
        default=Gender.UNSPECIFIED
    )
    birth = models.DateField(null=True, blank=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    
    # Use the default groups field from AbstractUser
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['name']),
        ]
        permissions = [
            ("can_view_dashboard", "Can view dashboard"),
            ("can_manage_users", "Can manage users"),
            ("can_manage_roles", "Can manage roles"),
        ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split()[0] if self.name else self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        from django.core.mail import send_mail
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def verify_email(self):
        """Mark user's email as verified."""
        self.email_verified_at = timezone.now()
        self.save(update_fields=['email_verified_at'])

    @property
    def is_email_verified(self):
        return bool(self.email_verified_at)

    def has_admin_role(self):
        """Check if user has admin role."""
        return self.is_superuser or self.groups.filter(role__display_name='Admin').exists()

    def assign_role(self, role_name):
        """Assign a role to the user."""
        group, _ = Group.objects.get_or_create(name=role_name)
        role, _ = Role.objects.get_or_create(group=group)
        self.groups.add(group)

    def remove_role(self, role_name):
        """Remove a role from the user."""
        try:
            group = Group.objects.get(name=role_name)
            self.groups.remove(group)
        except Group.DoesNotExist:
            pass

    def has_role(self, role_name):
        """Check if user has specific role."""
        return self.groups.filter(role__group__name=role_name).exists()

    def has_any_role(self, role_names):
        """Check if user has any of the specified roles."""
        return self.groups.filter(role__group__name__in=role_names).exists()

    def has_all_roles(self, role_names):
        """Check if user has all specified roles."""
        return self.groups.filter(role__group__name__in=role_names).count() == len(role_names)

    def get_all_permissions(self, obj=None):
        """Get all permissions including those from roles."""
        if self.is_superuser:
            return Permission.objects.all()
        return Permission.objects.filter(
            models.Q(user=self) | models.Q(group__in=self.groups.all())
        ).distinct()