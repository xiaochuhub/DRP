# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'PerformedReaction', fields ['reference']
        db.delete_unique(u'DRP_performedreaction', ['reference'])

        # Removing M2M table for field inTestSetFor on 'PerformedReaction'
        db.delete_table('DRP_performedreaction_inTestSetFor')

        # Removing M2M table for field inTrainingSetFor on 'PerformedReaction'
        db.delete_table('DRP_performedreaction_inTrainingSetFor')

        # Adding field 'StatsModel.invalid'
        db.add_column(u'DRP_statsmodel', 'invalid',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'StatsModel.regenerationOf'
        db.add_column(u'DRP_statsmodel', 'regenerationOf',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['DRP.StatsModel'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'StatsModel.snapShot'
        db.add_column(u'DRP_statsmodel', 'snapShot',
                      self.gf('django.db.models.fields.files.FileField')(default=None, max_length=200, null=True),
                      keep_default=False)


        # Changing field 'StatsModel.fileName'
        db.alter_column(u'DRP_statsmodel', 'fileName', self.gf('django.db.models.fields.files.FileField')(max_length=200))

    def backwards(self, orm):
        # Adding M2M table for field inTestSetFor on 'PerformedReaction'
        db.create_table(u'DRP_performedreaction_inTestSetFor', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('performedreaction', models.ForeignKey(orm['DRP.performedreaction'], null=False)),
            ('statsmodel', models.ForeignKey(orm['DRP.statsmodel'], null=False))
        ))
        db.create_unique(u'DRP_performedreaction_inTestSetFor', ['performedreaction_id', 'statsmodel_id'])

        # Adding M2M table for field inTrainingSetFor on 'PerformedReaction'
        db.create_table(u'DRP_performedreaction_inTrainingSetFor', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('performedreaction', models.ForeignKey(orm['DRP.performedreaction'], null=False)),
            ('statsmodel', models.ForeignKey(orm['DRP.statsmodel'], null=False))
        ))
        db.create_unique(u'DRP_performedreaction_inTrainingSetFor', ['performedreaction_id', 'statsmodel_id'])

        # Adding unique constraint on 'PerformedReaction', fields ['reference']
        db.create_unique(u'DRP_performedreaction', ['reference'])

        # Deleting field 'StatsModel.invalid'
        db.delete_column(u'DRP_statsmodel', 'invalid')

        # Deleting field 'StatsModel.regenerationOf'
        db.delete_column(u'DRP_statsmodel', 'regenerationOf_id')

        # Deleting field 'StatsModel.snapShot'
        db.delete_column(u'DRP_statsmodel', 'snapShot')


        # Changing field 'StatsModel.fileName'
        db.alter_column(u'DRP_statsmodel', 'fileName', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        'DRP.booleandescriptor': {
            'Meta': {'object_name': 'BooleanDescriptor', '_ormbases': ['DRP.Descriptor']},
            u'descriptor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['DRP.Descriptor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'DRP.boolmoldescriptor': {
            'Meta': {'object_name': 'BoolMolDescriptor', '_ormbases': ['DRP.BooleanDescriptor']},
            u'booleandescriptor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['DRP.BooleanDescriptor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'DRP.boolmoldescriptorvalue': {
            'Meta': {'unique_together': "(('descriptor', 'compound'),)", 'object_name': 'BoolMolDescriptorValue'},
            'compound': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.Compound']"}),
            'descriptor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.BooleanDescriptor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'DRP.boolrxndescriptor': {
            'Meta': {'object_name': 'BoolRxnDescriptor', '_ormbases': ['DRP.BooleanDescriptor']},
            u'booleandescriptor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['DRP.BooleanDescriptor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'DRP.boolrxndescriptorvalue': {
            'Meta': {'unique_together': "(('reaction', 'descriptor'),)", 'object_name': 'BoolRxnDescriptorValue'},
            'descriptor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.BooleanDescriptor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['DRP.StatsModel']", 'null': 'True'}),
            'reaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.Reaction']"}),
            'value': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'DRP.categoricaldescriptor': {
            'Meta': {'object_name': 'CategoricalDescriptor', '_ormbases': ['DRP.Descriptor']},
            u'descriptor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['DRP.Descriptor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'DRP.categoricaldescriptorpermittedvalue': {
            'Meta': {'unique_together': "(('descriptor', 'value'),)", 'object_name': 'CategoricalDescriptorPermittedValue'},
            'descriptor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'permittedValues'", 'to': "orm['DRP.CategoricalDescriptor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'DRP.catmoldescriptor': {
            'Meta': {'object_name': 'CatMolDescriptor', '_ormbases': ['DRP.CategoricalDescriptor']},
            u'categoricaldescriptor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['DRP.CategoricalDescriptor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'DRP.catmoldescriptorvalue': {
            'Meta': {'unique_together': "(('descriptor', 'compound'),)", 'object_name': 'CatMolDescriptorValue'},
            'compound': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.Compound']"}),
            'descriptor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.CategoricalDescriptor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.CategoricalDescriptorPermittedValue']", 'null': 'True'})
        },
        'DRP.catrxndescriptor': {
            'Meta': {'object_name': 'CatRxnDescriptor', '_ormbases': ['DRP.CategoricalDescriptor']},
            u'categoricaldescriptor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['DRP.CategoricalDescriptor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'DRP.catrxndescriptorvalue': {
            'Meta': {'unique_together': "(('reaction', 'descriptor'),)", 'object_name': 'CatRxnDescriptorValue'},
            'descriptor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.CategoricalDescriptor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['DRP.StatsModel']", 'null': 'True'}),
            'reaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.Reaction']"}),
            'value': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.CategoricalDescriptorPermittedValue']", 'null': 'True'})
        },
        'DRP.chemicalclass': {
            'Meta': {'object_name': 'ChemicalClass'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'DRP.compound': {
            'CSID': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'INCHI': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'Meta': {'unique_together': "(('abbrev', 'labGroup'), ('CSID', 'labGroup'))", 'object_name': 'Compound'},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'chemicalClasses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['DRP.ChemicalClass']", 'symmetrical': 'False'}),
            'custom': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labGroup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.LabGroup']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'smiles': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'DRP.compoundquantity': {
            'Meta': {'object_name': 'CompoundQuantity'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'compound': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.Compound']", 'on_delete': 'models.PROTECT'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.Reaction']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.CompoundRole']"})
        },
        'DRP.compoundrole': {
            'Meta': {'object_name': 'CompoundRole'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'DRP.confirmationcode': {
            'Meta': {'object_name': 'ConfirmationCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        'DRP.descriptor': {
            'Meta': {'unique_together': "(('heading', 'calculatorSoftware', 'calculatorSoftwareVersion'),)", 'object_name': 'Descriptor'},
            'calculatorSoftware': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'calculatorSoftwareVersion': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'DRP.labgroup': {
            'Meta': {'object_name': 'LabGroup'},
            'access_code': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legacy_access_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'DRP.legacystatsmodel': {
            'Meta': {'object_name': 'LegacyStatsModel'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'confusion_table': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'correct_vals': ('django.db.models.fields.CharField', [], {'default': '\'["3","4"]\'', 'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "'/home/padler1/programming/drp/DRP/modelsuntitled.model'", 'max_length': '128'}),
            'headers': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iterations': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'library': ('django.db.models.fields.CharField', [], {'default': "'weka'", 'max_length': '128'}),
            'response': ('django.db.models.fields.CharField', [], {'default': "'outcomoe'", 'max_length': '128'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'untitled'", 'max_length': '100'}),
            'tmp_confusion_table': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'tool': ('django.db.models.fields.CharField', [], {'default': "'svc'", 'max_length': '128'}),
            'train_confusion_table': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'usable': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'DRP.license': {
            'Meta': {'object_name': 'License'},
            'effectiveDate': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'DRP.licenseagreement': {
            'Meta': {'object_name': 'LicenseAgreement'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'signedDateTime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.License']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'DRP.numericdescriptor': {
            'Meta': {'object_name': 'NumericDescriptor', '_ormbases': ['DRP.Descriptor']},
            u'descriptor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['DRP.Descriptor']", 'unique': 'True', 'primary_key': 'True'}),
            'maximum': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'minimum': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'DRP.nummoldescriptor': {
            'Meta': {'object_name': 'NumMolDescriptor', '_ormbases': ['DRP.NumericDescriptor']},
            u'numericdescriptor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['DRP.NumericDescriptor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'DRP.nummoldescriptorvalue': {
            'Meta': {'unique_together': "(('descriptor', 'compound'),)", 'object_name': 'NumMolDescriptorValue'},
            'compound': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.Compound']"}),
            'descriptor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.NumericDescriptor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'DRP.numrxndescriptor': {
            'Meta': {'object_name': 'NumRxnDescriptor', '_ormbases': ['DRP.NumericDescriptor']},
            u'numericdescriptor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['DRP.NumericDescriptor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'DRP.numrxndescriptorvalue': {
            'Meta': {'unique_together': "(('reaction', 'descriptor'),)", 'object_name': 'NumRxnDescriptorValue'},
            'descriptor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.NumericDescriptor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['DRP.StatsModel']", 'null': 'True'}),
            'reaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.Reaction']"}),
            'value': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'DRP.ordinaldescriptor': {
            'Meta': {'object_name': 'OrdinalDescriptor', '_ormbases': ['DRP.Descriptor']},
            u'descriptor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['DRP.Descriptor']", 'unique': 'True', 'primary_key': 'True'}),
            'maximum': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'minimum': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'DRP.ordmoldescriptor': {
            'Meta': {'object_name': 'OrdMolDescriptor', '_ormbases': ['DRP.OrdinalDescriptor']},
            u'ordinaldescriptor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['DRP.OrdinalDescriptor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'DRP.ordmoldescriptorvalue': {
            'Meta': {'unique_together': "(('descriptor', 'compound'),)", 'object_name': 'OrdMolDescriptorValue'},
            'compound': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.Compound']"}),
            'descriptor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.OrdinalDescriptor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'DRP.ordrxndescriptor': {
            'Meta': {'object_name': 'OrdRxnDescriptor', '_ormbases': ['DRP.OrdinalDescriptor']},
            u'ordinaldescriptor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['DRP.OrdinalDescriptor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'DRP.ordrxndescriptorvalue': {
            'Meta': {'unique_together': "(('reaction', 'descriptor'),)", 'object_name': 'OrdRxnDescriptorValue'},
            'descriptor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.OrdinalDescriptor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['DRP.StatsModel']", 'null': 'True'}),
            'reaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.Reaction']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'DRP.performedreaction': {
            'Meta': {'object_name': 'PerformedReaction', '_ormbases': ['DRP.Reaction']},
            'duplicateOf': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'duplicatedBy'", 'null': 'True', 'blank': 'True', 'to': "orm['DRP.PerformedReaction']"}),
            'insertedDateTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'legacyRecommendedFlag': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'performedDateTime': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {}),
            u'reaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['DRP.Reaction']", 'unique': 'True', 'primary_key': 'True'}),
            'recommendation': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'resultantExperiment'", 'null': 'True', 'blank': 'True', 'to': "orm['DRP.RecommendedReaction']"}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'DRP.reaction': {
            'Meta': {'object_name': 'Reaction'},
            'compounds': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['DRP.Compound']", 'through': "orm['DRP.CompoundQuantity']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labGroup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.LabGroup']"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'DRP.recommendedreaction': {
            'Meta': {'object_name': 'RecommendedReaction', '_ormbases': ['DRP.Reaction']},
            'hidden': ('django.db.models.fields.BooleanField', [], {}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DRP.StatsModel']", 'null': 'True'}),
            'nonsense': ('django.db.models.fields.BooleanField', [], {}),
            u'reaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['DRP.Reaction']", 'unique': 'True', 'primary_key': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'saved': ('django.db.models.fields.BooleanField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'seed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seeded'", 'null': 'True', 'to': "orm['DRP.Reaction']"})
        },
        'DRP.statsmodel': {
            'Meta': {'object_name': 'StatsModel'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'descriptors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['DRP.Descriptor']", 'symmetrical': 'False'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'fileName': ('django.db.models.fields.files.FileField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invalid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'iterations': ('django.db.models.fields.IntegerField', [], {}),
            'library': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'regenerationOf': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['DRP.StatsModel']", 'null': 'True', 'blank': 'True'}),
            'snapShot': ('django.db.models.fields.files.FileField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['DRP.StatsModelTag']", 'symmetrical': 'False'}),
            'tool': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'DRP.statsmodeltag': {
            'Meta': {'object_name': 'StatsModelTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['DRP']