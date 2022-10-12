# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from reference_books.models import Branches

GENDER_CHOICES = (
    ('man', u'Мужской'),
    ('woman', u'Женский')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.ManyToManyField(Branches, related_name='branches_available', verbose_name=u'Филиалы доступные',
                                    help_text='Выбрать филиалы доступные пользователю')
    branch_default = models.ForeignKey(Branches, models.SET_NULL, related_name='branch_default',
                                       verbose_name=u'Филиал по умолчанию', null=True, blank=True)
    branch_current = models.ForeignKey(Branches, models.SET_NULL, related_name='branch_current',
                                       verbose_name=u'Филиал активный', null=True, blank=True)
    birthday = models.DateField(u'Дата рождения', null=True, blank=True)
    phone = models.CharField(u'Номер телефона', blank=True, max_length=10,
                             help_text=u'Вводить номер в федеральном формате, без кода страны 8 или +7')
    gender = models.CharField(u'Пол', choices=GENDER_CHOICES, max_length=50, blank=True)
    personal_data = models.BooleanField(u'Согласие на обработку персональных данных', default=False)
    mobile_version = models.BooleanField(u'Мобильная версия', default=False)
    avatar = models.ImageField(u'Аватар', upload_to='accounts/avatars/', blank=True, default='user.png')

    class Meta:
        ordering = ["user__last_name"]

    def __str__(self):
        return self.user.last_name + ' ' + self.user.first_name


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
