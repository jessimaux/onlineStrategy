from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from core.models import Settings


class AccountsManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, last_name, date_of_birth, municipality, password, **extra_fields):
        """Layout for create_user"""
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not date_of_birth:
            raise ValueError("User must have a date of birth")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            municipality_id=municipality,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, date_of_birth, municipality, password=None, **extra_fields):
        extra_fields.setdefault('staff', False)
        extra_fields.setdefault('superuser', False)
        return self._create_user(email, first_name, last_name, date_of_birth, municipality, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, date_of_birth, municipality, password, **extra_fields):
        extra_fields.setdefault('staff', True)
        extra_fields.setdefault('superuser', True)
        if extra_fields.get('staff') is not True:
            raise ValueError('Superuser must have staff=True.')
        if extra_fields.get('superuser') is not True:
            raise ValueError('Superuser must have superuser=True.')

        return self._create_user(email, first_name, last_name, date_of_birth, municipality, password, **extra_fields)


class Account(AbstractBaseUser):

    # Main information block
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=64, default=None)
    last_name = models.CharField(max_length=64, default=None)
    middle_name = models.CharField(max_length=64, blank=True)
    GENDER_CHOICES = (
        ('М', 'Мужской'),
        ('Ж', 'Женский'),
    )
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, default=None, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    NATIONAL_CHOICES = (
        ('ПР', 'Прочее'),
        ('РФ', 'Российская федерация'),
    )
    national = models.CharField(max_length=64, choices=NATIONAL_CHOICES, default=None, null=True)
    municipality = models.ForeignKey('core.Municipality', on_delete=models.CASCADE, default=None)

    # TODO: make validation on client-side
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=32, blank=True)  # validators should be a list

    # Education information block
    EDUCATION_CHOICES = (
        ('ПР', 'Прочее'),
        ('СПО', 'СПО'),
        ('БКВТ', 'Бакалавриат'),
        ('СПЦ', 'Специалитет'),
        ('МАГ', 'Магистратура'),
    )
    education_level = models.CharField(max_length=8, choices=EDUCATION_CHOICES, default=None, null=True)
    education_document_serial = models.CharField(max_length=6, blank=True)
    education_document_number = models.CharField(max_length=7, blank=True)
    education_document_reg_number = models.CharField(max_length=4, blank=True)
    education_document_date = models.DateField(blank=True, null=True)
    education_document_second_name = models.CharField(max_length=64, blank=True)
    education_document_first_name = models.CharField(max_length=64, blank=True)
    education_document_middle_name = models.CharField(max_length=64, blank=True)
    education_qualify = models.CharField(max_length=128, blank=True)
    EDUCATION_POW_CHOICES = (
        ('Н', 'Нет степени'),
        ('КН', 'Кандидат наук'),
        ('ДОК', 'Доктор наук'),
    )
    education_pow = models.CharField(max_length=8, choices=EDUCATION_POW_CHOICES, default=None, null=True)
    EDUCATION_RANK_CHOICES = (
        ('Н', 'Нет звания'),
        ('КН', 'Доцент'),
        ('ДОК', 'Профессор'),
    )
    education_rank = models.CharField(max_length=8, choices=EDUCATION_RANK_CHOICES, default=None, null=True)

    # Work information block
    work = models.CharField(max_length=255, blank=True)
    work_pos = models.CharField(max_length=255, blank=True)
    work_exp = models.PositiveIntegerField(blank=True, null=True)
    work_edu_exp = models.PositiveIntegerField(blank=True, null=True)

    # Document
    document_serial = models.CharField(max_length=4, blank=True)
    document_number = models.CharField(max_length=6, blank=True)
    document_department = models.CharField(max_length=255, blank=True)
    document_date = models.DateField(blank=True, null=True)
    document_code_department = models.CharField(max_length=7, blank=True)
    document_place_birth = models.CharField(max_length=255, blank=True)

    # Avatar
    # TODO: change folder name to profiles_pic or smth
    image = models.ImageField(upload_to='images', default='images/default.png')

    # Technical field
    is_active = models.BooleanField(default=True)
    methodist = models.BooleanField(default=False)
    moderator = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'municipality']

    objects = AccountsManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def is_moderator(self):
        return self.moderator

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_absolute_url(self):
        return f'/account/{self.id}'