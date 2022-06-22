from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from allauth.account.adapter import get_adapter
from allauth.account.utils import user_email, user_field


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE, related_name='%(class)s', verbose_name='пользователь')
    username = models.CharField('логин', max_length=125)
    password = models.CharField('пароль', max_length=128)
    first_name = models.CharField('имя', max_length=30)
    middle_name = models.CharField('отчество', max_length=150)
    last_name = models.CharField('фамилия', max_length=150)
    birth_date = models.DateField('дата рождения', blank=True)
    email = models.EmailField('еmail адрес')
    phone = models.CharField('номер телефона', blank=True, max_length=125)
    avatar = models.ImageField(
        'фотография',
        upload_to='avatars/',
        blank=True,
        help_text='Формат: jpg, gif, png.<br> '
                  'Макс. размер файла: 2Mb.<br> '
                  'Рекомендуется: 512x512px.'
    )
    hobby = models.ManyToManyField('Hobby', related_name='%(class)s', verbose_name='хобби')

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_full_name() if self.get_full_name() else self.user.__str__()

    def get_full_name(self):
        return ' '.join(filter(None, [self.last_name, self.first_name, self.middle_name]))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk:
            adapter = get_adapter()
            try:
                user = self.user
            except ObjectDoesNotExist:
                user = adapter.new_user(None)
            if self.first_name:
                user_field(user, 'first_name', self.first_name)
            if self.last_name:
                user_field(user, 'last_name', self.last_name)
            if self.email:
                user_email(user, self.email)
            if self.username:
                user_field(user, 'username', self.username)
            if self.password:
                user.set_password(self.password)
            user.save()

            self.user = user
        return super().save(force_insert, force_update, using, update_fields)


class Landlord(Profile):
    class Meta(Profile.Meta):
        verbose_name = 'Арендодатель'
        verbose_name_plural = 'Арендодатели'


class Tenant(Profile):
    status = models.CharField('статус', max_length=125, blank=True)

    class Meta(Profile.Meta):
        verbose_name = 'Арендатор'
        verbose_name_plural = 'Арендаторы'


class Hobby(models.Model):
    name = models.CharField('название', max_length=125)

    class Meta:
        verbose_name = 'Хобби'
        verbose_name_plural = 'Хобби'

    def __str__(self):
        return self.name
