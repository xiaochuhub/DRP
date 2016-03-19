'''A module containing only the PerformedReaction class'''
from django.db import models
from Reaction import Reaction, ReactionManager, ReactionQuerySet
from RecommendedReaction import RecommendedReaction
from django.contrib.auth.models import User
from itertools import chain
import DRP

class PerformedReactionQuerySet(ReactionQuerySet):
        # I assume this was wrong and it should be the one below
        #def __init__(self, model=None, **kwargs):
                #"""Initialises the queryset"""
                #model = Reaction if model is None else model
                #super(ReactionQuerySet, self).__init__(model=model, **kwargs)
        def __init__(self, model=None, **kwargs):
                """Initialises the queryset"""
                model = PerformedReaction if model is None else model
                super(PerformedReactionQuerySet, self).__init__(model=model, **kwargs)

class PerformedReactionManager(ReactionManager):
        def get_queryset(self):
            return PerformedReactionQuerySet(model=PerformedReaction)


class PerformedReaction(Reaction):
    '''A class representing concrete instances of reactions that have actually been performed'''

    class Meta:
        app_label="DRP"

    objects = PerformedReactionManager()
    user = models.ForeignKey(User)
    performedBy = models.ForeignKey(User, related_name='performedReactions', null=True, default=None)
    reference = models.CharField(max_length=40, unique=True)
    performedDateTime = models.DateTimeField('Date Reaction Performed', null=True, default=None, help_text='Date in format YYYY-MM-DD')
    insertedDateTime = models.DateTimeField('Date Reaction Saved', auto_now_add=True)
    recommendation = models.ForeignKey(RecommendedReaction, blank=True, unique=False, null=True, default=None, related_name='resultantExperiment')
    legacyRecommendedFlag = models.NullBooleanField(default=None)
    '''If this reaction was based from a recommendation, reference that recommendation'''
    valid = models.BooleanField(default=True)
    '''A flag to denote reactions which have been found to be invalid, for instance,
    if the wrong reactant was used or some bad lab record has been found'''
    public = models.BooleanField(default=False)
    duplicateOf = models.ForeignKey('self', related_name='duplicatedBy', blank=True, unique=False, null=True, default=None)

    def __unicode__(self):
        return self.reference

    def save(self, *args, **kwargs):
        self.reference = self.reference.lower()
        if self.pk is not None:
            test = DRP.models.StatsModel.objects.filter(testSets__reactions__in=[self])
            train = DRP.models.StatsModel.objects.filter(trainingSet__reactions=self)
            for model in chain(test, train):
                model.invalidate()
        super(PerformedReaction, self).save(*args, **kwargs)
