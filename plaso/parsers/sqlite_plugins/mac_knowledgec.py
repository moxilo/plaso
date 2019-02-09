# -*- coding: utf-8 -*-
"""Parser for the MacOS Duet / KnowledgeC database."""

from __future__ import unicode_literals

from dfdatetime import cocoa_time as dfdatetime_cocoa_time

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import definitions
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface


class MacKnowledgeCApplicationEventData(events.EventData):
  """MacOS KnowledgeC database event data related to application activity.

  Attributes:
    action: source of the action
    usage_in_seconds: seconds where the action happens
    bundle_id: bundle id responsable of the action (application)
  """

  DATA_TYPE = 'mac:knowledgec:application'

  def __init__(self):
    """Initializes event data."""
    super(MacKnowledgeCApplicationEventData, self).__init__(
        data_type=self.DATA_TYPE)
    self.action = None
    self.usage_in_seconds = None
    self.bundle_id = None

class MacKnowledgeCSafariEventData(events.EventData):
  """MacOS Duet / KnowledgeC database event data for Safari.

  Attributes:
    action: source of the action
    usage_in_seconds: seconds where the action happens
    bundle_id: bundle id responsable of the action (application)
    uri: URI where Safari connected
    fulluri: full URI where Safari connected
    uri_title: title of the URI
  """

  DATA_TYPE = 'mac:knowledgec:safari'

  def __init__(self):
    """Initializes event data."""
    super(MacKnowledgeCSafariEventData, self).__init__(data_type=self.DATA_TYPE)
    self.action = None
    self.usage_in_seconds = None
    self.uri = None
    self.fulluri = None
    self.uri_title = None


class MacKnowledgeCPlugin(interface.SQLitePlugin):
  """Parse the MacOS Duet / KnowledgeC database."""

  NAME = 'mac_knowledgec'
  DESCRIPTION = 'Parser for Duet / KnowledgeC database file.'

  # Define the needed queries.
  # entry_creation: when the entry was created in the Sqlitedb
  # start: when the activity started
  # end: when the activity finished
  # usage_in_seconds: seconds where the application was used
  # action: actions that created the entry (inFocus, activity, intents)
  # bundle_id: bundle ID (application)
  # app_act_content_description: description of the activity
  # app_act_user_activity_request: user activity request
  # uri: Safari URI
  # uri_title: Safari uri title
  QUERIES = [
      (("""
        SELECT
          ZOBJECT.ZCREATIONDATE AS "entry_creation", 
          ZOBJECT.ZSTARTDATE AS "start", 
          ZOBJECT.ZENDDATE AS "end",
          (ZOBJECT.ZENDDATE-ZOBJECT.ZSTARTDATE) AS "usage_in_seconds",
          ZOBJECT.ZSTREAMNAME AS "action",
          ZOBJECT.ZVALUESTRING AS "bundle_id",
          ZSTRUCTUREDMETADATA.Z_DKAPPLICATIONACTIVITYMETADATAKEY__CONTENTDESCRIPTION AS "app_act_content_description", 
          ZSTRUCTUREDMETADATA.Z_DKAPPLICATIONACTIVITYMETADATAKEY__USERACTIVITYREQUIREDSTRING AS "app_act_user_activity_request",
          ZOBJECT.ZVALUESTRING AS "uri", 
          ZSTRUCTUREDMETADATA.Z_DKSAFARIHISTORYMETADATAKEY__TITLE AS "uri_title"
        FROM ZOBJECT
        LEFT JOIN ZSTRUCTUREDMETADATA ON ZOBJECT.ZSTRUCTUREDMETADATA = ZSTRUCTUREDMETADATA.Z_PK
        """),
       'KnowledgeCRow')]

  # The required tables for the query.
  REQUIRED_TABLES = frozenset(['ZOBJECT', 'ZSTRUCTUREDMETADATA'])

  # pylint: disable=C0301
  # Field names in lines 163, 166, 169 and 196 are too long
  SCHEMAS = [{
      'ZOBJECT': (
          """
          CREATE TABLE ZOBJECT ( Z_PK INTEGER PRIMARY KEY, Z_ENT INTEGER,
          Z_OPT INTEGER, ZUUIDHASH INTEGER, ZEVENT INTEGER, ZSOURCE INTEGER,
          ZCATEGORYTYPE INTEGER, ZINTEGERVALUE INTEGER, ZENDDAYOFWEEK INTEGER,
          ZENDSECONDOFDAY INTEGER, ZHASCUSTOMMETADATA INTEGER,
          ZHASSTRUCTUREDMETADATA INTEGER, ZSECONDSFROMGMT INTEGER,
          ZSHOULDSYNC INTEGER, ZSTARTDAYOFWEEK INTEGER,
          ZSTARTSECONDOFDAY INTEGER, ZVALUECLASS INTEGER,
          ZVALUEINTEGER INTEGER, ZVALUETYPECODE INTEGER,
          ZSTRUCTUREDMETADATA INTEGER, ZVALUE INTEGER, Z9_VALUE INTEGER,
          ZIDENTIFIERTYPE INTEGER, ZQUANTITYTYPE INTEGER, ZOBJECT INTEGER,
          Z9_OBJECT INTEGER, ZSUBJECT INTEGER, Z9_SUBJECT INTEGER,
          ZCREATIONDATE TIMESTAMP, ZLOCALCREATIONDATE TIMESTAMP,
          ZCONFIDENCE FLOAT, ZENDDATE TIMESTAMP, ZSTARTDATE TIMESTAMP,
          ZVALUEDOUBLE FLOAT, ZDOUBLEVALUE FLOAT, ZUUID VARCHAR,
          ZSTREAMNAME VARCHAR, ZVALUESTRING VARCHAR,
          ZSTRING VARCHAR, ZVERBPHRASE VARCHAR, ZMETADATA BLOB)
          """),
      'ZSTRUCTUREDMETADATA': (
          """
          CREATE TABLE ZSTRUCTUREDMETADATA (
          Z_PK INTEGER PRIMARY KEY, Z_ENT INTEGER, Z_OPT INTEGER,
          Z_CDPORTRAITMETADATAKEY__ALGORITHM INTEGER,
          Z_CDPORTRAITMETADATAKEY__ASSETVERSION INTEGER,
          Z_DKAPPINSTALLMETADATAKEY__ISINSTALL INTEGER,
          Z_DKAPPLICATIONACTIVITYMETADATAKEY__ISELIGIBLEFORPREDICTION INTEGER,
          Z_DKAPPLICATIONACTIVITYMETADATAKEY__ISPUBLICLYINDEXABLE INTEGER,
          Z_DKAPPLICATIONMETADATAKEY__PROCESSIDENTIFIER INTEGER,
          Z_DKAUDIOMETADATAKEY__ROUTECHANGEREASON INTEGER,
          Z_DKBLUETOOTHMETADATAKEY__DEVICETYPE INTEGER,
          Z_DKBULLETINBOARDMETADATAKEY__HASDATE INTEGER,
          Z_DKDIGITALHEALTHMETADATAKEY__USAGETYPE INTEGER,
          Z_DKGLANCELAUNCHMETADATA__DEVICEIDENTIFIER INTEGER,
          Z_DKINTENTMETADATAKEY__DONATEDBYSIRI INTEGER,
          Z_DKINTENTMETADATAKEY__INTENTHANDLINGSTATUS INTEGER,
          Z_DKINTENTMETADATAKEY__INTENTTYPE INTEGER,
          Z_DKNOWPLAYINGMETADATAKEY__IDENTIFIER INTEGER,
          Z_DKNOWPLAYINGMETADATAKEY__PLAYING INTEGER,
          Z_DKSEARCHFEEDBACKMETADATAKEY__INTERACTIONTYPE INTEGER,
          Z_DKSEARCHFEEDBACKMETADATAKEY__SUGGESTIONTYPE INTEGER,
          Z_QPMETRICSMETADATAKEY__QUERYENGAGED INTEGER,
          Z_QPMETRICSMETADATAKEY__RESULTENGAGED INTEGER,
          ZCOM_APPLE_CALENDARUIKIT_USERACTIVITY_DATE INTEGER,
          ZCOM_APPLE_CALENDARUIKIT_USERACTIVITY_ENDDATE INTEGER,
          Z_CDPORTRAITMETADATAKEY__DECAYRATE FLOAT,
          Z_CDPORTRAITMETADATAKEY__SCORE FLOAT,
          Z_DKAPPLICATIONACTIVITYMETADATAKEY__EXPIRATIONDATE TIMESTAMP,
          Z_DKLOCATIONAPPLICATIONACTIVITYMETADATAKEY__LATITUDE FLOAT,
          Z_DKLOCATIONAPPLICATIONACTIVITYMETADATAKEY__LONGITUDE FLOAT,
          Z_DKLOCATIONMETADATAKEY__LATITUDE FLOAT,
          Z_DKLOCATIONMETADATAKEY__LONGITUDE FLOAT,
          Z_DKNOWPLAYINGMETADATAKEY__DURATION FLOAT,
          Z_DKNOWPLAYINGMETADATAKEY__ELAPSED FLOAT,
          Z_DKPERIODMETADATAKEY__PERIODEND TIMESTAMP,
          Z_DKPERIODMETADATAKEY__PERIODSTART TIMESTAMP,
          Z_QPMETRICSMETADATAKEY__TIMESTAMP FLOAT,
          Z_CDENTITYMETADATAKEY__BESTLANGUAGE VARCHAR,
          Z_CDENTITYMETADATAKEY__NAME VARCHAR,
          Z_CDPORTRAITMETADATAKEY__OSBUILD VARCHAR,
          Z_DKAPPINSTALLMETADATAKEY__PRIMARYCATEGORY VARCHAR,
          Z_DKAPPINSTALLMETADATAKEY__TITLE VARCHAR,
          Z_DKAPPLICATIONACTIVITYMETADATAKEY__ACTIVITYTYPE VARCHAR,
          Z_DKAPPLICATIONACTIVITYMETADATAKEY__CONTENTDESCRIPTION VARCHAR,
          Z_DKAPPLICATIONACTIVITYMETADATAKEY__ITEMIDENTIFIER VARCHAR,
          Z_DKAPPLICATIONACTIVITYMETADATAKEY__ITEMRELATEDUNIQUEIDENTIFIER VARCHAR,
          Z_DKAPPLICATIONACTIVITYMETADATAKEY__SUGGESTEDINVOCATIONPHRASE VARCHAR,
          Z_DKAPPLICATIONACTIVITYMETADATAKEY__TITLE VARCHAR,
          Z_DKAPPLICATIONACTIVITYMETADATAKEY__USERACTIVITYREQUIREDSTRING VARCHAR,
          Z_DKAPPLICATIONACTIVITYMETADATAKEY__USERACTIVITYUUID VARCHAR,
          Z_DKAPPLICATIONMETADATAKEY__BACKBOARDSTATE VARCHAR,
          Z_DKAPPLICATIONMETADATAKEY__EXTENSIONCONTAININGBUNDLEIDENTIFIER VARCHAR,
          Z_DKAPPLICATIONMETADATAKEY__EXTENSIONHOSTIDENTIFIER VARCHAR,
          Z_DKAPPLICATIONMETADATAKEY__LAUNCHREASON VARCHAR,
          Z_DKAUDIOMETADATAKEY__CHANNELS VARCHAR,
          Z_DKAUDIOMETADATAKEY__DATASOURCES VARCHAR,
          Z_DKAUDIOMETADATAKEY__IDENTIFIER VARCHAR,
          Z_DKAUDIOMETADATAKEY__PORTNAME VARCHAR,
          Z_DKAUDIOMETADATAKEY__PORTTYPE VARCHAR,
          Z_DKAUDIOMETADATAKEY__PREFERREDDATASOURCE VARCHAR,
          Z_DKAUDIOMETADATAKEY__SELECTEDDATASOURCE VARCHAR,
          Z_DKBATTERYSAVERMETADATAKEY__SOURCE VARCHAR,
          Z_DKBLUETOOTHMETADATAKEY__ADDRESS VARCHAR,
          Z_DKBLUETOOTHMETADATAKEY__NAME VARCHAR,
          Z_DKBULLETINBOARDMETADATAKEY__FEED VARCHAR,
          Z_DKBULLETINBOARDMETADATAKEY__MESSAGE VARCHAR,
          Z_DKBULLETINBOARDMETADATAKEY__SUBTITLE VARCHAR,
          Z_DKBULLETINBOARDMETADATAKEY__TITLE VARCHAR,
          Z_DKCALENDARMETADATAKEY__INTERACTION VARCHAR,
          Z_DKCALLMETADATAKEY__INTERACTION VARCHAR,
          Z_DKDEVICEIDMETADATAKEY__DEVICEIDENTIFIER VARCHAR,
          Z_DKDIGITALHEALTHMETADATAKEY__WEBDOMAIN VARCHAR,
          Z_DKINTENTMETADATAKEY__INTENTCLASS VARCHAR,
          Z_DKINTENTMETADATAKEY__INTENTVERB VARCHAR,
          Z_DKLOCATIONAPPLICATIONACTIVITYMETADATAKEY__URL VARCHAR,
          Z_DKLOCATIONAPPLICATIONACTIVITYMETADATAKEY__CITY VARCHAR,
          Z_DKLOCATIONAPPLICATIONACTIVITYMETADATAKEY__COUNTRY VARCHAR,
          Z_DKLOCATIONAPPLICATIONACTIVITYMETADATAKEY__DISPLAYNAME VARCHAR,
          Z_DKLOCATIONAPPLICATIONACTIVITYMETADATAKEY__FULLYFORMATTEDADDRESS VARCHAR,
          Z_DKLOCATIONAPPLICATIONACTIVITYMETADATAKEY__LOCATIONNAME VARCHAR,
          Z_DKLOCATIONAPPLICATIONACTIVITYMETADATAKEY__POSTALCODE_V2 VARCHAR,
          Z_DKLOCATIONAPPLICATIONACTIVITYMETADATAKEY__STATEORPROVINCE VARCHAR,
          Z_DKLOCATIONAPPLICATIONACTIVITYMETADATAKEY__SUBTHOROUGHFARE VARCHAR,
          Z_DKLOCATIONAPPLICATIONACTIVITYMETADATAKEY__THOROUGHFARE VARCHAR,
          Z_DKLOCATIONMETADATAKEY__IDENTIFIER VARCHAR,
          Z_DKMETADATAHOMEAPPVIEW__HOMEUUID VARCHAR,
          Z_DKMETADATAHOMEAPPVIEW__VIEWINFORMATION VARCHAR,
          Z_DKMETADATAHOMEAPPVIEW__VIEWNAME VARCHAR,
          Z_DKMETADATAHOMEAPPVIEW__VIEWUUID VARCHAR,
          Z_DKMETADATAHOMEKITACCESSORYCONTROL__ACCESSORYNAME VARCHAR,
          Z_DKMETADATAHOMEKITACCESSORYCONTROL__ACCESSORYUUID VARCHAR,
          Z_DKMETADATAHOMEKITACCESSORYCONTROL__CHARACTERISTICTYPE VARCHAR,
          Z_DKMETADATAHOMEKITACCESSORYCONTROL__CLIENTNAME VARCHAR,
          Z_DKMETADATAHOMEKITACCESSORYCONTROL__HOMEUUID VARCHAR,
          Z_DKMETADATAHOMEKITACCESSORYCONTROL__SERVICENAME VARCHAR,
          Z_DKMETADATAHOMEKITACCESSORYCONTROL__SERVICETYPE VARCHAR,
          Z_DKMETADATAHOMEKITSCENE__ACTIONSETNAME VARCHAR,
          Z_DKMETADATAHOMEKITSCENE__ACTIONSETTYPE VARCHAR,
          Z_DKMETADATAHOMEKITSCENE__ACTIONSETUUID VARCHAR,
          Z_DKMETADATAHOMEKITSCENE__CLIENTNAME VARCHAR,
          Z_DKMETADATAHOMEKITSCENE__HOMEUUID VARCHAR,
          Z_DKMETADATAHOMEKITSCENE__SCENENAME VARCHAR,
          Z_DKMICROLOCATIONMETADATAKEY__LOCATIONDISTRIBUTION VARCHAR,
          Z_DKMICROLOCATIONMETADATAKEY__MICROLOCATIONDISTRIBUTION VARCHAR,
          Z_DKNOTIFICATIONUSAGEMETADATAKEY__BUNDLEID VARCHAR,
          Z_DKNOTIFICATIONUSAGEMETADATAKEY__IDENTIFIER VARCHAR,
          Z_DKNOWPLAYINGMETADATAKEY__ALBUM VARCHAR,
          Z_DKNOWPLAYINGMETADATAKEY__ARTIST VARCHAR,
          Z_DKNOWPLAYINGMETADATAKEY__GENRE VARCHAR,
          Z_DKNOWPLAYINGMETADATAKEY__TITLE VARCHAR,
          Z_DKRELEVANTSHORTCUTMETADATAKEY__KEYIMAGEPROXYIDENTIFIER VARCHAR,
          Z_DKSAFARIHISTORYMETADATAKEY__TITLE VARCHAR,
          Z_DKSEARCHFEEDBACKMETADATAKEY__CLIENT VARCHAR,
          Z_DKSEARCHFEEDBACKMETADATAKEY__CONTACTID VARCHAR,
          Z_DKTOMBSTONEMETADATAKEY__EVENTSOURCEDEVICEID VARCHAR,
          Z_DKTOMBSTONEMETADATAKEY__EVENTSTREAMNAME VARCHAR,
          Z_QPMETRICSMETADATAKEY__QUERY VARCHAR,
          ZCOM_APPLE_CALENDARUIKIT_USERACTIVITY_EXTERNALID VARCHAR,
          ZKCDCSNOTIFICATIONOPTIONCLIENTIDENTIFIERKEY VARCHAR,
          ZKCDCSNOTIFICATIONOPTIONCLIENTLAUNCHKEY VARCHAR,
          ZKCDCSNOTIFICATIONOPTIONPERSISTENTPREDICATESTRINGKEY VARCHAR,
          ZMETADATAHASH VARCHAR,
          Z_DKAPPLICATIONACTIVITYMETADATAKEY__ITEMRELATEDCONTENTURL VARCHAR,
          Z_DKDIGITALHEALTHMETADATAKEY__WEBPAGEURL VARCHAR,
          Z_DKAPPINSTALLMETADATAKEY__SUBCATEGORIES BLOB,
          Z_DKINTENTMETADATAKEY__SERIALIZEDINTERACTION BLOB,
          Z_DKLOCATIONAPPLICATIONACTIVITYMETADATAKEY__PHONENUMBERS BLOB,
          Z_DKRELEVANTSHORTCUTMETADATAKEY__SERIALIZEDRELEVANTSHORTCUT BLOB,
          Z_QPMETRICSMETADATAKEY__CANDIDATELIST BLOB,
          Z_QPMETRICSMETADATAKEY__QUERYLIST BLOB )
      """)}]
  # pylint: enable=C0301

  def KnowledgeCRow(
      self, parser_mediator, query, row, **unused_kwargs):
    """Parses KnowledgeC application activity

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfvfs.
      query (str): query that created the row.
      row (sqlite3.Row): row.
    """
    query_hash = hash(query)
    entry_creation = self._GetRowValue(query_hash, row, 'entry_creation')
    activity_starts = self._GetRowValue(query_hash, row, 'start')
    activity_ends = self._GetRowValue(query_hash, row, 'end')
    usage_in_seconds = self._GetRowValue(query_hash, row, 'usage_in_seconds')
    action = self._GetRowValue(query_hash, row, 'action')
    bundle_id = self._GetRowValue(query_hash, row, 'bundle_id')

    entry_creation_time = dfdatetime_cocoa_time.CocoaTime(
        timestamp=entry_creation)
    entry_creation_event = time_events.DateTimeValuesEvent(
        entry_creation_time, definitions.TIME_DESCRIPTION_CREATION)
    activity_starts_time = dfdatetime_cocoa_time.CocoaTime(
        timestamp=activity_starts)
    activity_starts_event = time_events.DateTimeValuesEvent(
        activity_starts_time, definitions.TIME_DESCRIPTION_START)
    activity_ends_time = dfdatetime_cocoa_time.CocoaTime(
        timestamp=activity_ends)
    activity_ends_event = time_events.DateTimeValuesEvent(
        activity_ends_time, definitions.TIME_DESCRIPTION_END)

    if action.startswith('/safari/'):
      fulluri = self._GetRowValue(query_hash, row, 'uri')
      uri_title = self._GetRowValue(query_hash, row, 'uri_title')
      event_data = MacKnowledgeCSafariEventData()
      event_data.usage_in_seconds = usage_in_seconds
      event_data.uri = bundle_id
      event_data.fulluri = fulluri
      event_data.uri_title = uri_title
      parser_mediator.ProduceEventWithEventData(
          entry_creation_event, event_data)
      parser_mediator.ProduceEventWithEventData(
          activity_starts_event, event_data)
      parser_mediator.ProduceEventWithEventData(
          activity_ends_event, event_data)
    elif action.startswith('/app/'):
      event_data = MacKnowledgeCApplicationEventData()
      event_data.action = action
      event_data.usage_in_seconds = usage_in_seconds
      event_data.bundle_id = bundle_id
      parser_mediator.ProduceEventWithEventData(
          entry_creation_event, event_data)
      parser_mediator.ProduceEventWithEventData(
          activity_starts_event, event_data)
      parser_mediator.ProduceEventWithEventData(
          activity_ends_event, event_data)


sqlite.SQLiteParser.RegisterPlugin(MacKnowledgeCPlugin)
