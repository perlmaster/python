######################################################################
#
# File      : mysql-describe-2.py
#
# Author    : Barry Kimelman
#
# Created   : January 7, 2020
#
# Purpose   : python script to describe the structure of a mysql table
#
# Notes     :
#
######################################################################

import mysql.connector
from mysql.connector import Error
import sys

######################################################################
#
# Function  : show_table_details
#
# Purpose   : Run the query with the specified id value
#
# Inputs    : table_name - name of table to be described
#
# Output    : query results
#
# Returns   : nothing
#
# Example   : show_table_details("customers")
#
# Notes     : (none)
#
######################################################################

def show_table_details(table_name):
	try:
		mySQLConnection = mysql.connector.connect(host='localhost',database='mydatabase',user='myusername',password='mypassword')

		cursor = mySQLConnection.cursor(buffered=True)
		sql_select_query = "select ordinal_position ordinal, column_name colname,is_nullable isnull,"
		sql_select_query += "ifnull(character_maximum_length,'--') maxlen,column_type,extra,column_key,"
		sql_select_query += "ifnull(column_comment,'--') comment"
		sql_select_query += " from information_schema.columns where table_schema = 'mydatabase' and "
		sql_select_query += "table_name = %s"
		cursor.execute(sql_select_query, (table_name,))
		record = cursor.fetchall()
		ordinals = []
		colnames = []
		data_types = []
		maxlens = []
		isnulls = []
		keys = []
		extras = []
		comments = []
		num_columns = 0
		headers = ["Ordinal" , "Column Name", "Data Type", "Maxlen" , "Nullable ?" , "Key" , "Extra" , "Comment"]
		longest = []
		for index in range(0,8):
			longest.append(len(headers[index]))
		num = len(longest)

		for row in record:
			num_columns += 1
			ordinals.append(row[0])
			colnames.append(row[1])
			num_bytes = len(row[1])
			if num_bytes > longest[1]:
				longest[1] = num_bytes

			data_types.append(row[4])
			num_bytes = len(row[4])
			if num_bytes > longest[2]:
				longest[2] = num_bytes

			maxlens.append(row[3])
			num_bytes = len(row[3])
			if num_bytes > longest[3]:
				longest[3] = num_bytes

			isnulls.append(row[2])
			num_bytes = len(row[2])
			if num_bytes > longest[4]:
				longest[4] = num_bytes

			keys.append(row[6])
			num_bytes = len(row[6])
			if num_bytes > longest[5]:
				longest[5] = num_bytes

			extras.append(row[5])
			num_bytes = len(row[5])
			if num_bytes > longest[6]:
				longest[6] = num_bytes

			comments.append(row[7])
			num_bytes = len(row[7])
			if num_bytes > longest[7]:
				longest[7] = num_bytes
		print("\n%d columns found for table %s\n" % (num_columns,table_name))
		# print(repr(x).rjust(2), repr(x*x).rjust(3), end=' ')
		for index in range(0, 8):
			print(str(headers[index]).ljust(longest[index]), end=' ')
		print("")
		for index in range(0, num_columns):
			# print("column [ %d ]" % index)
			print(str(ordinals[index]).ljust(longest[0]), end=' ')
			print(str(colnames[index]).ljust(longest[1]), end=' ')
			print(str(data_types[index]).ljust(longest[2]), end=' ')
			print(str(maxlens[index]).ljust(longest[3]), end=' ')
			print(str(isnulls[index]).ljust(longest[4]), end=' ')
			print(str(keys[index]).ljust(longest[5]), end=' ')
			print(str(extras[index]).ljust(longest[6]), end=' ')
			print(str(comments[index]).ljust(longest[7]))

	except mysql.connector.Error as error:
		print("Failed to get record from MySQL table: {}".format(error))

	finally:
		if (mySQLConnection.is_connected()):
			cursor.close()
			mySQLConnection.close()
			print("\nMySQL connection is closed")

# Main program

num_args = len(sys.argv) - 1
if num_args > 0:
	show_table_details(sys.argv[1])
else:
	print("No table name was specified")
