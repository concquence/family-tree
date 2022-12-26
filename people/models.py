from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    gender = models.CharField(max_length=1,
                              choices=(('M', 'Male'), ('F', 'Female')),
                              blank=False, default='M', verbose_name='Пол')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True,
                                 verbose_name='Фамилия')
    maiden_name = models.CharField(max_length=50, blank=True,
                                   verbose_name='Девичья фамилия')
    birth = models.DateField(blank=True, null=True,
                             verbose_name='Дата рождения')
    death = models.DateField(blank=True, null=True,
                             verbose_name='Дата смерти')
    lived_ca = models.CharField(max_length=100, blank=True,
                                verbose_name='Годы жизни (приблизительно)')
    bio = models.TextField(blank=True, verbose_name='Биография')
    photo = models.ImageField(blank=True, upload_to='people',
                              verbose_name='Фото члена семьи')
    spouse = models.ManyToManyField('self', blank=True, symmetrical=True,
                                    verbose_name='Супруг/Супруга')
    father = models.ForeignKey('self', models.SET_NULL, blank=True, null=True,
                               limit_choices_to={'gender': 'M'},
                               related_name='who_father', verbose_name='Отец')
    mother = models.ForeignKey('self', models.SET_NULL, blank=True, null=True,
                               limit_choices_to={'gender': 'F'},
                               related_name='who_mother', verbose_name='Мать')
    tree_owner = models.BooleanField(default=False,
                                     verbose_name='Исходный член семьи')

    class Meta:
        verbose_name = 'Член семьи'
        verbose_name_plural = 'Семья'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        current_owner = Person.objects.filter(tree_owner=True,
                                              user=self.user.pk)
        if not self.tree_owner and len(current_owner):
            super(Person, self).save(*args, **kwargs)
        elif self.tree_owner and len(current_owner):
            current_owner[0].tree_owner = False
            current_owner[0].save()
            super(Person, self).save(*args, **kwargs)
        else:
            self.tree_owner = True
            super(Person, self).save(*args, **kwargs)
        return self

    def __str__(self):
        if self.last_name:
            return '{} {} ({})'.format(self.first_name, self.last_name,
                                       self.pk)
        else:
            return '{} ({})'.format(self.first_name, self.pk)

    @property
    def parents(self):
        return self.father, self.mother

    @property
    def partners(self):
        queryset =  Person.objects.get(id=self.pk).spouse.all()
        partner_list = []
        for partner in queryset:
            partner_list.append(partner)
        return partner_list


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    persons = models.ManyToManyField(Person, blank=True, related_name='imgs',
                                     verbose_name='Фотография')
    description = models.TextField(blank=True,
                                   verbose_name='Описание фотографии')
    img = models.ImageField(blank=True, upload_to='images',
                            verbose_name='Image file')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        filename = self.img.name.rsplit('/')[-1]
        return filename

    @property
    def get_filename(self):
        return self

    @property
    def get_persons(self):
        queryset = Image.objects.get(id=self.pk).persons.filter()
        person_list = []
        for person in queryset:
            person_list.append(person)
        return person_list


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    person = models.ForeignKey(Person, blank=True, null=True, default=None,
                               on_delete=models.CASCADE,
                               verbose_name='Владелец документа')
    description = models.TextField(blank=True, default='',
                                   verbose_name='Описание документа')
    doc = models.ImageField(blank=True, upload_to='documents',
                            verbose_name='Document file')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        filename = self.doc.name.rsplit('/')[-1]
        return filename

    @property
    def get_filename(self):
        return self

    @property
    def get_document_owner(self):
        return Document.objects.get(id=self.pk).person
