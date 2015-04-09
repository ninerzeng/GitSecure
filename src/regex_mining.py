import re;
 
#tested with https://regex101.com 

#base64 key
#64 repetitions is arbitrary, just enough to get past redacted ones
key_pattern = r"""BEGIN( RSA)? PRIVATE KEY(-*)(\s*)(([A-Za-z0-9+/]{4})\n?){64}"""

#3 arguments, last one being string password
sql_pattern = r"""mysql(i)?(_connect)?\((.){2,25},(.){2,25},['"]\S+['"]\)"""



test_sql = """$conn = new mysql_connect("servername", $usesssssrname,"sdf")"""

test_key = """-----BEGIN RSA PRIVATE KEY----- 
MIICXgIBAAKBgQDHikastc8+I81zCg/qWW8dMr8mqvXQ3qbPAmu0RjxoZVI47tvs
kYlFAXOf0sPrhO2nUuooJngnHV0639iTTEYG1vckNaW2R6U5QTdQ5Rq5u+uV3pMk
7w7Vs4n3urQ6jnqt2rTXbC1DNa/PFeAZatbf7ffBBy0IGO0zc128IshYcwIDAQAB
AoGBALTNl2JxTvq4SDW/3VH0fZkQXWH1MM10oeMbB2qO5beWb11FGaOO77nGKfWc
bYgfp5Ogrql4yhBvLAXnxH8bcqqwORtFhlyV68U1y4R+8WxDNh0aevxH8hRS/1X5
031DJm1JlU0E+vStiktN0tC3ebH5hE+1OxbIHSZ+WOWLYX7JAkEA5uigRgKp8ScG
auUijvdOLZIhHWq7y5Wz+nOHUuDw8P7wOTKU34QJAoWEe771p9Pf/GTA/kr0BQnP """

print re.search(key_pattern, test_key)

print re.search(sql_pattern, test_sql)


#printf: number of % signs must match number of commas
#needs to count % then , 
def printf_pattern(document) :
	printf_call = r"""printf\(.*\)"""
	printfs = findall(printf_call, document)
	#compare % and ,
	#
	return false
