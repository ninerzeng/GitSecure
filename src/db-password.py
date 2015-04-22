import re
import os
import subprocess


#<quotes> <not quotes> <quotes>
STRING_PASSWORD = r"""[\'\"][^\'\"]*[\'\"]"""

#<not comma length 2-35 (includes whitespace)> <comma>
ARGUMENT = r"""[^,]{2,35},\s*"""

LONG_ARGUMENT = r"""[^,]{2,150},\s*"""

END_FUNCTION = r"""\s*\)"""

END_WITH_OPTIONALS = r"""[^\)]*\)"""


#	MYSQL AND FRIENDS
#	mysql or mysqli ( <any argument> , <any argument> <any string argument> )
#	regex = r"""\bmysql(i)?(_connect)?\([^,]{2,25}?,[^,]{2,25}?,\s*[\'\"][^\'\"]+[\'\"]\s*\)"""
#	changed to accept empty string "" passwords
#	mysqlx = r"""\bmysql(i)?(_connect)?\([^,]{2,25}?,[^,]{2,25}?,\s*[\'\"][^\'\"]*[\'\"]\s*\)"""
#	changed to greedy, think it's more efficient for going up to ) character
mysqlx = r"""\bmysql(i)?(_connect)?\(""" + ARGUMENT + ARGUMENT + STRING_PASSWORD + END_WITH_OPTIONALS


#	MSSQL
#	optional crap at end
mssqlx = r"""\bmssql_connect\(""" + ARGUMENT + ARGUMENT + STRING_PASSWORD+ END_WITH_OPTIONALS


#	PDO
#	password is always third argument. first argument is a wacky string
PDOx = r"""\bPDO\(""" + LONG_ARGUMENT + ARGUMENT + STRING_PASSWORD + END_FUNCTION


#	ODBC			optional arguments after password
ODBCx = r"""\bodbc_connect\(""" + LONG_ARGUMENT + ARGUMENT + STRING_PASSWORD + END_WITH_OPTIONALS


#	POSTGRES
#	long connection string including password=PASSWORD
POSTGRESx = r"""\bpg_connect\(\s*[\"\'][^\"\'\)]*password=[^\"\'\)]*[\"\']\s*\)"""


#	ORACLE OCI
OCIx = r"""\boci_connect\(""" + ARGUMENT + STRING_PASSWORD + END_WITH_OPTIONALS




'''
def testregex(regex):
	cmd = "grep -i -E \"" + regex + "\" db-test.txt"
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	temp = process.communicate()
	
	print temp
	print "\n"


testregex(mysqlx)
testregex(mssqlx)
testregex(PDOx)
testregex(ODBCx)
testregex(POSTGRESx)
testregex(OCIx)
'''


