#http://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files
import re

def removeComments(string):
	string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", string)
	string = re.sub(re.compile("//.*?\n" ) , "", string)
	return string

def removeCommentsAndStrings(string):
	#print string
	string = re.sub(re.compile("(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)", re.MULTILINE|re.DOTALL), "", string)
	return string

def search_for_function_uses(string, func_list): 
	f_list = []
	for func in func_list:
		result = search_for_function_use(string, func)
		#print result
		if result:
			match_list = {func: []}
			for tuple in result:
				match_list[func].append(tuple)
			
			f_list.append(match_list)
			#f_list.append({func: result.group(0)})
			#print result.group(0)
	return f_list		

def search_for_function_use(string, func):
	return re.findall(re.compile(".*\s" + func + "\s*\(.*\).*"), string)
		
