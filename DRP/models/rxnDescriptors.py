'''A module containing the reactions descriptors'''
from descriptors import CategoricalDescriptor, OrdinalDescriptor, BooleanDescriptor
from descriptors import CategoricalDescriptorPermittedValue, NumericDescriptor, Predictable, DescriptorManager
import rxnDescriptorValues
import DRP.models

class CatRxnDescriptor(CategoricalDescriptor, Predictable):
    '''A class which describes a descriptor- a value which describes a system such as a compound or a reaction'''

    class Meta:
        app_label='DRP'
        verbose_name = 'Categorical Reaction Descriptor'

    objects = DescriptorManager()

    def __init__(self, *args, **kwargs):
        super(CatRxnDescriptor, self).__init__(*args, **kwargs)
        self.predictedDescriptorType = DRP.models.predRxnDescriptors.PredCatRxnDescriptor #because of python's flawed dependency resolution, this is what I've been reduced to.

    def createValue(self, reaction, value):
        """Create a new reaction value object"""
        if not isinstance(value, str) and value is not None:
            raise TypeError("You cannot create a categorical value with non-string type {}".format(type(value)))
        try:
            v = rxnDescriptorValues.CatRxnDescriptorValue.objects.get(descriptor=self, reaction=reaction)
        except rxnDescriptorValues.CatRxnDescriptorValue.doesnotExist:
            v = rxnDescriptorValues.CatRxnDescriptorValue(descriptor=self, reaction=reaction)
        v.value=CategoricalDescriptorPermittedValue.objects.get(value=value)
        return v

class OrdRxnDescriptor(OrdinalDescriptor, Predictable):
    '''A class which represents an ordinal descriptor'''

    class Meta:
        verbose_name= 'Ordinal Reaction Descriptor'
        app_label='DRP'

    objects = DescriptorManager()

    def __init__(self, *args, **kwargs):
        super(OrdRxnDescriptor, self).__init__(*args, **kwargs)
        self.predictedDescriptorType = DRP.models.predRxnDescriptors.PredOrdRxnDescriptor #because of python's flawed dependency resolution, this is what I've been reduced to.

    def createValue(self, reaction, value):
        if not isinstance(value, int) and value is not None:
            raise TypeError("You cannot create a ordinal value with non-integer type {}".format(type(value)))
        try:
            v = rxnDescriptorValues.OrdRxnDescriptorValue.objects.get(descriptor=self, reaction=reaction)
        except rxnDescriptorValues.OrdRxnDescriptorValue.DoesNotExist:
            v = rxnDescriptorValues.OrdRxnDescriptorValue(descriptor=self, reaction=reaction)
        v.value = value
        return v

    def createPredictionDescriptor(self, *args, **kwargs):
        pred = super(OrdRxnDescriptor, self).createPredictionDescriptor(*args, **kwargs)
        pred.maximum = self.maximum
        pred.minimum = self.minimum
        return pred

class NumRxnDescriptor(NumericDescriptor, Predictable):
    '''A class which represents a numerical descriptor'''

    class Meta:
        app_label='DRP'
        verbose_name= 'Numerical Reaction Descriptor'

    objects = DescriptorManager()

    def __init__(self, *args, **kwargs):
        super(NumRxnDescriptor, self).__init__(*args, **kwargs)
        self.predictedDescriptorType = DRP.models.predRxnDescriptors.PredNumRxnDescriptor #because of python's flawed dependency resolution, this is what I've been reduced to.

    def createValue(self, reaction, value):
        if not isinstance(value, float) and value is not None:
            raise TypeError("You cannot create a numerical value with non-float type {}".format(type(value)))
        try:
            v = rxnDescriptorValues.NumRxnDescriptorValue.objects.get(descriptor=self, reaction=reaction)
        except rxnDescriptorValues.NumRxnDescriptorValue.DoesNotExist:
            v = rxnDescriptorValues.NumRxnDescriptorValue(descriptor=self, reaction=reaction)
        v.value = value
        return v

    def createPredictionDescriptor(self, *args, **kwargs):
        pred = super(NumRxnDescriptor, self).createPredictionDescriptor(*args, **kwargs)
        pred.maximum = self.maximum
        pred.minimum = self.minimum
        return pred

class BoolRxnDescriptor(BooleanDescriptor, Predictable):
    '''A class which represents a boolean descriptors'''

    class Meta:
        app_label='DRP'
        verbose_name= 'Boolean Reaction Descriptor'

    objects = DescriptorManager()

    def __init__(self, *args, **kwargs):
        super(BoolRxnDescriptor, self).__init__(*args, **kwargs)
        self.predictedDescriptorType = DRP.models.predRxnDescriptors.PredBoolRxnDescriptor #because of python's flawed dependency resolution, this is what I've been reduced to.

    def createValue(self, reaction, value):
        if not isinstance(value, bool) and value is not None:
            raise TypeError("You cannot create a boolean value with non-boolean type {}".format(type(value)))
        try:
            v = rxnDescriptorValues.BoolRxnDescriptorValue.objects.get(descriptor=self, reaction=reaction)
        except rxnDescriptorValues.BoolRxnDescriptorValue.DoesNotExist:
            v = rxnDescriptorValues.BoolRxnDescriptorValue(descriptor=self, reaction=reaction)
        v.value = value
        return v
