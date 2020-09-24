from django.db import models

class User(models.Model):
    """Model representing an user."""
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    card_number = models.IntegerField(null=True, blank=True)
    
    USER_STATUS = (
        (1, 'Teacher'),
        (2, 'Student/Parents'),
    )

    status = models.IntegerField(
        max_length=1,
        choices=USER_STATUS,
    )

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.user_id}, {self.name}'

class Class(models.Model):
    """Model representing an user."""
    class_id = models.AutoField(primary_key=True)
    tutor = models.IntegerField(max_length=100)
    student = models.IntegerField(max_length=100)
    topic = models.CharField(max_length=100)
    pay_per_hour = models.IntegerField(null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.class_id}, {self.topic}'