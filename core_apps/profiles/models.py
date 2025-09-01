from autoslug import AutoSlugField
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core_apps.common.models import TimeStampModel

User = get_user_model()

def get_user_username(instance: "Profile") -> str:
    if instance.user.username:
        return instance.user.username
    return instance.user.first_name + '-' + instance.user.last_name

class Profile(TimeStampModel):
    class Gender(models.TextChoices):
        MALE = ('male', _("Male"))
        FEMALE = ('female', _("Female"))
        OTHER = ('other', _("Other"))

    class Occupation(models.TextChoices):
        Mason = ('mason', _("Mason"))
        Carpenter = ('carpenter', _("Carpenter"))
        Plumber = ('plumber', _("Plumber"))
        Roofer = ('roofer', _("Roofer"))
        Painter = ('painter', _("Painter"))
        Electrician = ('electrician', _("Electrician"))
        HVAC = ('hvac', _("HVAC"))
        Tenant = ('tenant', _("Tenant"))
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = CloudinaryField(verbose_name=_("Avatar"), blank=True, null=True)
    gender = models.CharField(verbose_name=_("Gender"), max_length=10, choices=Gender.choices, default=Gender.MALE)
    bio = models.TextField(verbose_name=_("Biography"), blank=True, null=True)
    occupation = models.CharField(verbose_name=_("Occupation"), max_length=20, choices=Occupation.choices, default=Occupation.Tenant)
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"), max_length=15, default="+84987654321")
    country_of_origin = CountryField(verbose_name=_("Country"), default="VN")
    city_of_origin = models.CharField(verbose_name=_("City"), max_length=100, default="Quang Tri")
    report_count = models.IntegerField(verbose_name=_("Report Count"), default=0)
    reputation = models.IntegerField(verbose_name=_("Reputation"), default=100)
    slug = AutoSlugField(populate_from=get_user_username, unique=True)

    @property
    def is_banned(self) -> bool:
        return self.report_count >= 5
    
    def update_reputation(self):
        self.reputation = max(0, 100 - self.report_count * 20)
        
    def save(self, *args, **kwargs):
        self.update_reputation()
        super().save(*args, **kwargs)
