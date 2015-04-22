import os
import subprocess

def grep_for_regexes(root_dir, regexes, file_suffix="*.php"):
  comments = ['/^\\#/d', '/\\/\\*/,/*\\//d; /^\\/\\//d; /^$/d;']
  cmd_base = "find " + root_dir + " -name '" + file_suffix + "' -type f -print0 | xargs -0 sed -i "

  for comment in comments:
    cmd = cmd_base + "'" + comment + "'"
#    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    temp = process.communicate()

  result = [];
  regex = "|".join(regexes)
#  for regex in regexes:
  cmd = "grep -i -E \"" + regex + "\" " + root_dir + " --include " + file_suffix +"  -n --no-messages --with-filename -r"
#  print cmd
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
  temp = process.communicate()
#  print temp
  if temp:
    return parse_grep_output(temp[0], root_dir)
  
def parse_grep_output(grep_out, root_dir):
  result = {};
  for line in grep_out.splitlines():
    ar = line.split(":")
    if len(ar) >= 3:
      if (ar[0].find(root_dir) >= 0):
        filename = ar[0]
        filename = filename.replace(root_dir, "") # remove data root directory from filename
        line_num = ar[1]
    #    print ar[2]
    #    print ar[2:]
        code = "".join(ar[2:])
        if filename not in result:
          result[filename] = []
        result[filename].append({"line":line_num, "code_sample": code})
      else:
        print "Warning: grep output line: " + line + " does not match expected form"
    else:
      print "Warning: grep output line: " + line + " does not match expected form"
  return result

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
		
