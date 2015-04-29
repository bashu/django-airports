# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Airport'
        db.create_table(u'airports_airport', (
            ('airport_id', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('iata', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('icao', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('altitude', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities.Country'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities.City'])),
        ))
        db.send_create_signal(u'airports', ['Airport'])


    def backwards(self, orm):
        # Deleting model 'Airport'
        db.delete_table(u'airports_airport')


    models = {
        u'airports.airport': {
            'Meta': {'ordering': "['airport_id']", 'object_name': 'Airport'},
            'airport_id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'altitude': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.City']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.Country']"}),
            'iata': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'icao': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'cities.alternativename': {
            'Meta': {'object_name': 'AlternativeName'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_colloquial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_preferred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_short': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'cities.city': {
            'Meta': {'object_name': 'City'},
            'alt_names': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['cities.AlternativeName']", 'symmetrical': 'False'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.Country']"}),
            'elevation': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_std': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.Region']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'subregion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.Subregion']", 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'cities.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'alt_names': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['cities.AlternativeName']", 'symmetrical': 'False'}),
            'area': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'capital': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'code3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'currency_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'neighbours': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'neighbours_rel_+'", 'to': u"orm['cities.Country']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'population': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tld': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'cities.region': {
            'Meta': {'object_name': 'Region'},
            'alt_names': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['cities.AlternativeName']", 'symmetrical': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_std': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'cities.subregion': {
            'Meta': {'object_name': 'Subregion'},
            'alt_names': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['cities.AlternativeName']", 'symmetrical': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_std': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.Region']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['airports']