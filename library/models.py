from __future__ import unicode_literals

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
    ISBN = models.CharField(max_length=13, default="1111111111111", validators=[RegexValidator(regex='^.{13}$', message='Length has to be 13', code='nomatch')])
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    image = models.ImageField(upload_to='book_covers/', blank=True)
    library = models.ForeignKey(Library)

    def __unicode__(self):
        return "{}_{}".format(self.id_book, self.title)

    def save(self):
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
            book = Book.get(borrowBook.id())
            if book.ISBN == self.ISBN:
                nrBorrowed += 1

        for reservedBook in Reserve.objects.all():
            book = Book.get(reservedBook.id())
            if book.ISBN == self.ISBN:
                nrReserved += 1

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


class Review(models.Model):
    id_review = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    opinion = models.CharField(max_length=140)
    choices = [('1', 'Very poor'), ('2', 'Poor'), ('3', 'Not bad'),
               ('4', 'Good'), ('5', 'Very Good')]
    rating = models.CharField(max_length=1, choices=choices)
