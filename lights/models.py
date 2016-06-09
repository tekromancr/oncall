from __future__ import unicode_literals

from colorful.fields import RGBColorField
import matrix_settings
import pypurdypixels

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

Strand = pypurdypixels.Strand


# Create your models here.
class LightManager(models.Manager):
    def get_pixels(self):
        lights = self.get_queryset()
        pos_sorted_pixels = map(lambda x: (Strand.rgb2px(*x.color_as_pixel), x.position), lights)
        matrix_sorted_pixels = [0] * matrix_settings.strand_length
        for idx,pix_val in enumerate(pos_sorted_pixels):
            matrix_index = matrix_settings.mapping[pix_val[1]]
            matrix_sorted_pixels[matrix_index] = pix_val[0]
        return matrix_sorted_pixels



    def get_strand(self):
        num_pixels = matrix_settings.strand_length
        debug_mode = matrix_settings.debug
        pixels = self.get_pixels()
        strand = Strand(strand_length=num_pixels, pixels=pixels,
                        debug_mode=debug_mode)
        return strand

    def get_matrix(self):
        cols = matrix_settings.cols
        rows = matrix_settings.rows
        mapping = matrix_settings.mapping
        return pypurdypixels.Matrix(strand=self.get_strand())


class Light(models.Model):
    class Meta:
        ordering = ('position',)

    position = models.IntegerField(unique=True)
    assigned_user = models.ForeignKey(User, null=True, blank=True)
    color = RGBColorField(colors=['#FFFFFF', '#FF0000', '#00FF00', '#0000FF', "#000000"])
    objects = LightManager()

    @property
    def color_as_pixel(self):
        r = self.color[1:3]
        g = self.color[3:5]
        b = self.color[5:7]
        return map(lambda x: int(x,16), (r,g,b))

    def __unicode__(self):
        return "light %d : %s"%(self.position, self.assigned_user)


@receiver(post_save, sender=Light)
def update_stock(sender, instance, **kwargs):
    Light.objects.get_strand()
