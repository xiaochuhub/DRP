from scipy.stats import gmean
from utils import setup
import DRP
from DRP import chemical_data

elements = chemical_data.elements

#Inorganic descriptors
inorgAtomicProperties = (
    'ionization_energy',
    'electron_affinity',
    'pauling_electronegativity',
    'pearson_electronegativity',
    'hardness',
    'atomic_radius'
)

weightings= (
    ('unw', 'unweighted'),
    ('stoich', 'stoichiometry')
)

inorgElements = {}
for element, info in elements.items():
    if (element == 'Se') or (info['group'] in range(3, 13)) or ((info['group'] > 12) and ((not info['nonmetal']) or info['metalloid'])):
        inorgElements[element] = info 

_descriptorDict = {}

for prop in inorgAtomicProperties:
    stem = 'drpInorgAtom' + prop.title().replace('_', '') 
    for weighting in weightings:
        _descriptorDict['{}_geom_{}'.format(stem, weighting[0])] = {
            'type':'num',
            'name': 'Geometric mean of {} weighted by {}.'.format(prop.replace('_', ' '), weighting[1]),
            'calculatorSoftware':'DRP',
            'calculatorSoftwareVersion':'0.02',
            'maximum':None,
            'minimum':None
            }
    _descriptorDict['{}_max'.format(stem)] = {
        'type': 'num',
        'name': 'Maximal value of {}'.format(prop.replace('_', '')),
        'calculatorSoftware':'DRP',
        'calculatorSoftwareVersion':'0.02',
        'maximum':None,
        'minimum':None
        }
    _descriptorDict['{}_range'.format(stem)] = {
        'type': 'num',
        'name': 'Range of {}'.format(prop.replace('_', '')),
        'calculatorSoftware':'DRP',
        'calculatorSoftwareVersion':'0.02',
        'maximum':None,
        'minimum':None
        }

descriptorDict = setup(_descriptorDict)

def delete_descriptors(compound_set):
    num = DRP.models.NumMolDescriptorValue
    descriptors_to_delete = []
    for prop in inorgAtomicProperties:
        descriptors_to_delete.append(descriptorDict['drpInorgAtom{}_geom_unw'.format(prop.title().replace('_', ''))])
        descriptors_to_delete.append(descriptorDict['drpInorgAtom{}_geom_stoich'.format(prop.title().replace('_', ''))])
        descriptors_to_delete.append(descriptorDict['drpInorgAtom{}_max'.format(prop.title().replace('_', ''))])
        descriptors_to_delete.append(descriptorDict['drpInorgAtom{}_range'.format(prop.title().replace('_', ''))])
    num.objects.filter(descriptor__in=descriptors_to_delete, compound__in=compound_set).delete(recalculate_reactions=False)

def calculate_many(compound_set, verbose=False):
    delete_descriptors(compound_set)
    for i, compound in enumerate(compound_set):
        _calculate(compound)
        if verbose:
            print "Done with {} ({}/{})".format(compound, i+1, len(compound_set))

def calculate(compound):
    delete_descriptors([compound])
    _calculate(compound)
    
def _calculate(compound):

    num = DRP.models.NumMolDescriptorValue

    if any(element in inorgElements for element in compound.elements):
        delete_descriptors([compound])
        vals_to_create = []
        inorgElementNormalisationFactor = sum(info['stoichiometry'] for element, info in compound.elements.items() if element in inorgElements)
        for prop in inorgAtomicProperties:
            vals_to_create.append(num( 
                                        compound=compound,
                                        descriptor=descriptorDict['drpInorgAtom{}_geom_unw'.format(prop.title().replace('_', ''))],
                                        value=gmean([inorgElements[element][prop] for element in compound.elements if element in inorgElements])
                                        ))

            vals_to_create.append(num(
                                        compound=compound,
                                        descriptor=descriptorDict['drpInorgAtom{}_geom_stoich'.format(prop.title().replace('_', ''))],
                                        value = gmean([inorgElements[element][prop]*(info['stoichiometry']/inorgElementNormalisationFactor) for element, info in compound.elements.items() if element in inorgElements])))
               
            vals_to_create.append(num(
                                        compound=compound,
                                        descriptor=descriptorDict['drpInorgAtom{}_max'.format(prop.title().replace('_', ''))],
                                        value = max(inorgElements[element][prop] for element in compound.elements if element in inorgElements)))
    
            vals_to_create.append(num(
                                        compound=compound,
                                        descriptor=descriptorDict['drpInorgAtom{}_range'.format(prop.title().replace('_', ''))],
                                        value = max(inorgElements[element][prop] for element in compound.elements if element in inorgElements) - min(inorgElements[element][prop] for element in compound.elements if element in inorgElements)))
        num.objects.bulk_create(vals_to_create)
    
