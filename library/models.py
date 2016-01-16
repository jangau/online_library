from __future__ import unicode_literals

from datetime import datetime

from PIL import Image

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Library(models.Model):
    id_library = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' ' + self.city


class Book(models.Model):
    id_book = models.AutoField(primary_key=True)
    ISBN = models.CharField(max_length=13, default="1111111111111",
                            validators=[RegexValidator(regex='^[0-9]{13}$',
                                                       message='Digits only, length has to be 13',
                                                       code='nomatch')])
    title = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100,  blank=True)
    genre = models.CharField(max_length=100,  blank=True)
    image = models.ImageField(upload_to='book_covers/', blank=True)
    library = models.ForeignKey(Library)

    def __unicode__(self):
        return "{}_{}".format(self.id_book, self.title)

    def save(self):
        book = Book.objects.filter(ISBN=self.ISBN).first()
        if book is not None:
            self.title = book.title
            self.author = book.author
            self.genre = book.genre
            self.image = book.image

        if not self.image:
            return

        super(Book, self).save()
        image = Image.open(self.image)
        (width, height) = image.size
        max_dimension = width
        if height > width:
            max_dimension = height

        ratio = max_dimension / 200.00

        size = (int(round(width/ratio)), int(round(height/ratio)))
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path)

    def getStock(self):
        nr = len(Book.objects.filter(ISBN=self.ISBN))
        nrBorrowed = 0
        nrReserved = 0
        for borrowBook in Borrow.objects.all():
            if borrowBook.book.ISBN == self.ISBN and borrowBook.date_return <= datetime.now().date():
                nrBorrowed += 1

        # for reservedBook in Reserve.objects.all():
        #     book = Book.get(reservedBook.id())
        #     if book.ISBN == self.ISBN:
        #         nrReserved += 1

        nr = nr - nrBorrowed - nrReserved
        return nr


class Borrow(models.Model):
    id_borrow = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    date_borrowed = models.DateField()
    date_return = models.DateField()


class Reserve(models.Model):
    id_reserve = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    period = models.IntegerField()


class Suggest(models.Model):
    id_suggestion = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100, blank=False)
    author = models.CharField(max_length=100, blank=False)


class Review(models.Model):
    id_review = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    opinion = models.CharField(max_length=140)
    choices = [('1', 'Very poor'), ('2', 'Poor'), ('3', 'Not bad'),
               ('4', 'Good'), ('5', 'Very Good')]
    rating = models.CharField(max_length=1, choices=choices)


class Profile(models.Model):
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    id_user = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=256)
    birthday = models.DateField()
    gender = models.CharField(max_length=1, choices=gender_choices)
    phone = models.CharField(max_length=20)
    card_number = models.CharField(max_length=16, default="1111111111111111",
                                   validators=[RegexValidator(regex='^[0-9]{16}$',
                                                              message='Digits only, length has to be 16',
                                                              code='nomatch')])
    card_cvv = models.CharField(max_length=3, default="111",
                                validators=[RegexValidator(regex='^[0-9]{3}$',
                                                           message='Digits only, length has to be 3',
                                                           code='nomatch')])
