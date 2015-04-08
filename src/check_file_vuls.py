import os
import parse_file as p

def scan_files_for_vul(root, file_dirs, vuls):
	results = []
	for file_dir in file_dirs:
		try:
			with open(os.path.join(root, file_dir), 'r') as f:
				#print 'Checking ' + file_dir + ' for vuls'
				f = f.read()
				result = p.search_for_function_uses(p.removeCommentsAndStrings(f), vuls)				
				#if len(result) > 0:
				results.append({file_dir: result})
		except IOError, e:
			print e
	return results
		
