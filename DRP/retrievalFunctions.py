from django.db.models import Q
from DRP.models import Data, get_lab_Data, get_model_field_names
from DRP.cacheFunctions import get_cache, set_cache
from DRP.models import get_lab_Data
import datetime, dateutil.relativedelta
import operator
from DRP.data_config import CONFIG
from DRP.validation import bool_fields
  
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
=======
from DRP.models import CompoundEntry

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
   # # # # # # # # # # # # # # # # # DATA  # # # # # # # # # # # # # # # # # #
   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_public_data():
  '''Returns a data that is both valid and public'''
  return Data.objects.filter(public=True, is_valid=True).order_by("creation_time_dt")


def get_lab_Data_size(lab_group):
  size = get_cache(lab_group, "TOTALSIZE")
  if not size:
    size = get_lab_Data(lab_group).count()
    set_cache(lab_group, "TOTALSIZE", size)
  return size


def atom_filter(atoms, data=None, op="and", negative=False):
  """
  Applies a containment search on the `data` for each atom in `atoms`;
  thus, it can be used to find any reaction that contains any/all atoms
  in a list.

  op = The operator to use for the query.
  negative = Enable to *remove* anything from `data` that matches the query.
  """


  op_map = {
    "and":operator.and_,
    "or":operator.or_,
  }

  # Variable Setup
  if data is None: data = get_valid_data()
  if type(atoms)!=list: atoms = list(atoms)
  op = op_map[op]

  # Construct the query.
  Qs = [Q(atoms__contains=atom) for atom in atoms]
  filters = reduce(op, Qs)

  # Apply the filter.
  if negative:
    data = data.filter(~filters)
  else:
    data = data.filter(filters)

  return data

def filter_by_date(lab_data, raw_date, direction="after"):

  # Convert the date input into a usable string. (Date must be given as MM-DD-YY.)
  date = datetime.datetime.strptime(raw_date, "%m-%d-%Y")

  # Get the reactions before/after a specific date.
  if direction.lower() == "after":
    filtered_data = lab_data.filter(creation_time_dt__gte=date)
  else:
    # Add a day to cover any times 00:00-23:59 on a given date.
    date += dateutil.relativedelta.relativedelta(days=1)
    filtered_data = lab_data.filter(creation_time_dt__lte=date)

  return filtered_data


def filter_existing_calcs(data):
  """
  Returns only the data which have calculations.
  """
  data = data.filter(~Q(calculations=None))
  data = data.filter(~Q(calculations__contents=""))
  data = data.filter(~Q(calculations__contents="[]"))

  return data

def filter_data(data, queries):

  multifields = {"reactant", "quantity", "unit"}
  mapper = {
    "reactant": "reactant_fk",
   }
  default_suffix = {
    "reactant":"abbrev",
    "user":"username",
  }
  op_map = {
    "reactant":operator.and_,
  }

  Qs = []

  for field, val_list in queries.items():
    # Read the "field.subfield.match" syntax correctly.
    if field.count(".")==2:
      field, suffix, suffix2 = field.split(".")
    elif field.count(".")==1:
      field, suffix = field.split(".")
      suffix2 = ""
    else:
      suffix = ""
      suffix2 = ""

    # Flip the suffix2 and suffix if no true subfield was specified.
    if not suffix2 and ("contains" in suffix or "exact" in suffix):
      suffix2 = suffix
      suffix = ""


    if not suffix and field in default_suffix:
      suffix = default_suffix[field]

    cleaned_suffix = "__{}".format(suffix) if suffix else ""
    cleaned_suffix += "__{}".format(suffix2) if suffix2 else "__icontains"

    cleaned = mapper[field] if field in mapper else field

    query = []

    for val in val_list:
      if field in multifields:
        multifield_query = []

        for i in CONFIG.reactant_range():
          actual_field = "{}_{}{}".format(cleaned, i, cleaned_suffix)
          multifield_query.append( Q(**{actual_field:val}) )

        query.append( reduce(operator.or_, multifield_query) )

      else:
        actual_field = "{}{}".format(cleaned, cleaned_suffix)
        query.append( Q(**{actual_field:val}) )

    if query:
      op = op_map[field] if field in op_map else operator.or_
      query = reduce(op, query)
      Qs.append(query)

  if queries:
    ands = reduce(operator.and_, Qs)
    data = data.filter(ands)

  return data


def form_filter_data(lab_group, query_list):

 #Variable Setup
 data = get_lab_Data(lab_group)
 filters = {}
 Q_list = []

  #Collect all the valid search options
 non_reactant_fields = get_model_field_names(unique_only=True)
 foreign_fields = ["user"] #Fields that cannot search by containment.
 reactant_fields = ["reactant","quantity","unit"]
 legal_fields = set(non_reactant_fields+reactant_fields+foreign_fields+["atoms", "public","is_valid"])

 legal_sub_fields = set(get_model_field_names(model="CompoundEntry"))


 #Check the query_list input before performing any database requests.
 for query in query_list:
  try:
   #Make sure values are provided.
   assert query.get(u"field") in legal_fields
   assert query.get(u"match") in {"contain","exact"}
   assert query.get(u"value")

   if query.get(u"sub-field"):
     assert query.get(u"sub-field") in legal_sub_fields

  except:
   raise Exception("One or more inputs is illegal")

 for query in query_list:
  field = query[u"field"]
  sub_field = query[u"sub-field"] if u"sub-field" in query else ""
  match = "__icontains" if query[u"match"] == "contain" else ""
  value = query[u"value"]
  if field in foreign_fields:
   field += "__username" #TODO: Generalize to all fields (make foreign_fields a dict where values are the foreign-field to search).

  #Translate Boolean inputs into Boolean values.
  if field in bool_fields:
   value = True if value.lower()[0] in "1tyc" else False

  #Apply the filter or a Q object with a range of filters.
  if field in reactant_fields:
   or_Qs = []
   for i in CONFIG.reactant_range():
    temp = {field+"_fk_{}".format(i)+"__"+sub_field+match: value}
    or_Qs.append(Q(**temp))

   Q_list.append(reduce(operator.or_, or_Qs))

  elif field=="atoms":
   atom_list = value.split(" ")
   if len(atom_list)>1:
    search_bool = atom_list.pop(-2) #Take the "and" or "or" from the list.
    op = operator.and_ if search_bool == "and" else operator.or_
    atom_Qs = [Q(atoms__contains=atom) for atom in atom_list] #TODO: Test this
    Q_list.append(reduce(op, atom_Qs))
   else:
    Q_list.append(Q(atoms__contains=atom_list[0]))

  else:
   filters[field+match] = value

 #Apply the Q objects and the filters.
 if Q_list:
  data = data.filter(reduce(operator.and_, Q_list))
 if filters:
  data = data.filter(**filters)
 return data


#Either get the valid Data entries for a lab group or get all valid data.
#  Note: Accepts an actual LabGroup object.
def get_valid_data(lab_group=None, clean=True):
  from models import Data
  data = Data.objects.filter(is_valid=True)

  if lab_group:
    data= data.filter(lab_group=lab_group)

  # If new data exists, check if it is valid or not.
  if clean:
    new = data.filter(calculations=None)

    for entry in new:
      try:
        entry.get_calculations_dict()
      except:
        entry.is_valid = False
        entry.save()

  data = data.filter(is_valid=True)

  return data



   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
   # # # # # # # # # # # # # # # DATACALCS   # # # # # # # # # # # # # # # # #
   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#Given some 'data', returns a list of any DataCalc objects that can be gathered.
def expand_data(data, include_lab_info=False, make_new=False, debug=False):
  from DRP.model_building.load_cg import get_cg
  calcList = []

  compound_guide = get_cg()

  for i, datum in enumerate(data):
    if debug and (i%100)==0: print "{}...".format(i)
    try:
      if datum.calculations or make_new:
        calcs = datum.get_calculations_list(include_lab_info=include_lab_info,
                                            preloaded_cg=compound_guide)
        calcList.append(calcs)
    except Exception as e:
      print "(expand_data) {}".format(e)
      pass
  return calcList

#Grabs the "expanded_headers" for the DataCalc objects created in 'parse_rxn.'
def get_expanded_headers():
  from DRP.model_building.rxn_calculator import headers
  return headers


   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
   # # # # # # # # # # # # RECOMMENDATIONS # # # # # # # # # # # # # # # # # #
   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_active_recommendations():
  from models import Recommendation
  model = get_latest_ModelStats()
  return Recommendation.objects.filter(model_version=model)

def get_seed_recs(lab_group, seed_ref=None, show_hidden=False, latest_first=True):
 from DRP.models import Recommendation, Data
 seed_recs = Recommendation.objects.filter(seeded=True, lab_group=lab_group)

 #If given a seed ref, only yield those recommendations that are seeded from it.
 if seed_ref:
   datum = Data.objects.filter(ref=seed_ref)
   seed_recs = seed_recs.filter(seed=datum)

 if not show_hidden:
   seed_recs = seed_recs.filter(hidden=False)

 if latest_first:
   seed_recs = seed_recs.order_by("-date_dt")

 return seed_recs



   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
   # # # # # # # # # # # # # # # #  MODEL   # # # # # # # # # # # # # # # # # #
   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_usable_models():
  from models import ModelStats
  model_stats = ModelStats.objects.filter(usable=True).order_by("end_time")
  return model_stats


def get_latest_ModelStats():
  from models import ModelStats
  models = ModelStats.objects.filter(usable=True, active=True)
  return models.last()


   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
   # # # # # # # # # # # # #  LABS AND USERS  # # # # # # # # # # # # # # # # #
   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_lab_users(lab_group):
  from DRP.models import Lab_Member
  lab_members = Lab_Member.filter(lab_group=lab_group)
  users = lab_members.values_list("user", flat=True)
  return users


   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
   # # # # # # # # # # # # #  COMPOUNDS  # # # # # # # # # # # # # # # # # # #
   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_compound_by_string(compound_str):
    return list(CompoundEntry.objects.filter(compound=compound_str))[0]

def get_compound_by_abbrev(abbrev_str):
    return list(CompoundEntry.objects.filter(abbrev=abbrev_str))[0]

def get_compound_by_name(compound_str):
    by_string = list(CompoundEntry.objects.filter(abbrev=compound_str))
    by_abbrev = list(CompoundEntry.objects.filter(compound=compound_str))
    by_both = by_string + by_abbrev
    # This bit with the by_both_filtered is a bit of a hack, intended to avoid errors
    #   from missing SMILES which should really be fixed in the database.
    by_both_filtered = [x for x in by_both if x.smiles]
    return (by_both_filtered+by_both)[0]

