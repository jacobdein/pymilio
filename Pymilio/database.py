"""
Jacob Dein 2016
Pymilio
Author: Jacob Dein
License: MIT
"""


import MySQLdb
import pandas

class Pymilio_db_connection:
	"""Create connection to pumilio database and perform operations."""
	
	
	def __init__(self, **kwargs):
		"""
		
		user
			string, user to connect as
			
		password
			string, password to use
			
		database
			string, database to use
		
		host = 'localhost'
			string, host to connect
			default = None
			
		read_default_file = None
			string, file from which default client values are read
			default = None
			
		"""
		
		self.user = kwargs['user']
		self.password = kwargs['password']
		self.database = kwargs['database']
		if 'host' in kwargs:
			self.host = kwargs['host']
		else:
			self.host = 'localhost'
		if 'read_default_file' in kwargs:
			self.read_default_file = kwargs['read_default_file']


	def _connect(self):
		"""Create MySQLdb connection to pumilio database."""
		
		'''
		if self.read_default_file:
			db=MySQLdb.connect(host=self.host,
						 user=self.user,
						 db=self.database,
						 read_default_file=self.read_default_file)
		else: '''
		db=MySQLdb.connect(host=self.host,
					 user=self.user,
					 passwd=self.password,
					 db=self.database)
		return db


	def fetch_as_pandas_df(self, table='Analyses', fields=['*'], where='', limit=1000):
		"""Fetch information from a pumilio database as a pandas dataframe."""
		
		result = self.query(table=table, fields=fields, where=where, limit=limit)
		if fields == ['*']:
			column_query = ("""SELECT COLUMN_NAME """
							"""FROM INFORMATION_SCHEMA.COLUMNS """
							"""WHERE TABLE_NAME = '{0}'""").format(table)
			db = self._connect()
			c = db.cursor()
			c.execute(column_query)
			rows = c.fetchall()
			c.close()
			db.close()
			column_names = [ i[0] for i in rows ]
		else:
			column_names = fields
		
		data = pandas.DataFrame( [[ij for ij in i] for i in result], columns=column_names )
		return data


	def query(self, table='Analyses', fields=['*'], where='', limit=1000):
		"""Query database."""
		
		db = self._connect()
		c = db.cursor()
		fields_string = ''
		for s in fields:
			 fields_string = fields_string + s + ', '
		fields_string = fields_string[:-2]
		if where != '':
			where = 'WHERE ' + where + ' '
		query = ("""SELECT {0} FROM {1} {2}LIMIT {3}""").format(fields_string, table, where, limit)
		c.execute(query)
		rows = c.fetchall()
		c.close()
		db.close()
		return rows
	
	
	def insert(self, table, values):
		"""Insert into database.
			
			table
				string, table name
				
			values
				tuple of two tuples, (({column_name}), ({value}))
				only supports one column insertion
		"""
		
		db = self._connect()
		c = db.cursor()
		statement = ("""INSERT INTO {0} ({1}) VALUES ('{2}')""").format(table, values[0], values[1])
		c.execute(statement)
		c.close()
		db.close()
		
		
	def update(self, table, values, where):
		"""Update database.
			
			table
				string, table name
				
			values
				tuple as follows: ({column_name}, {value})
				only supports one column insertion
			
			where
				string, where statement as follows: "{Column_name} = {value}"
		"""

		db = self._connect()
		c = db.cursor()
		# set the format for the input values (no change for strings, 4 decimals for floats)
		if type(values[1]) is str:
			value_format = '{0}'
		elif type(values[1]) is int:
			value_format = '{0}'
		else:
			value_format = '{0:.4f}'
		statement = ("""UPDATE {0} SET {1} = "{2}" WHERE {3}""").format(table, values[0], value_format, where)
		statement = statement.format(values[1])
		c.execute(statement)
		c.close()
		db.close()
	
	
	def get_sound_paths(self, prepath='', where=''):
		"""Get sound pathnames as a python dictionary."""
		
		results = self.query(table='Sounds', fields=['SoundID', 'ColID', 'DirID', 'OriginalFilename'], where=where)
		sound_paths = {}
		for r in results:
			sound_paths[str(r[0])] = "{3}/{0}/{1}/{2}".format(r[1], r[2], r[3], prepath)
		return sound_paths