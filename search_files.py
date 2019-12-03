# Allows you to search multiple files for a string
# by  gmastrokostas, from http://www.sfentona.net/?p=2565
""" given a base directory and a string, searches all subdirectories for files and searches all files for the string """
import os

#Specify default base directory
base_dir = 'f:\@python\coursera'

directory = raw_input('Enter base dir; press ENTER for default')
if directory != None:
    base_dir = directory
print "Enter search string"
s_string = raw_input('>')

print "base_dir:", base_dir
print "search string:", s_string




# create a list of all paths to files
# try:
#     subdirs = os.listdir(base_dir)
# except OSError, e:
# 	print "base directory %s does not exist." % base_dir
# for subdirectory in subdirs:
# 	try:
# 	    sub2 = os.listdir(subdirectory)
# 	except OSError, e:
# 		print e
	



# to_append = ['/wk 1/', '/wk 2/', '/wk 3/', '/wk 4/']

# for path in sd_tlist:
# 	for apdr in to_append:
# 		print "sd_tlist:", sd_tlist
# 		sd_tlist[sd_tlist.index(path)] = path + apdr

# print "sd_tlist:", sd_tlist

# # create subdirectory path lists


# pattern = re.compile ('normalize') # term to search for
 
# for src_dict in sd_tlist:
#     for yum_files in os.listdir(src_dict): # obtain list of files in directory
#         files = os.path.join(src_dict, yum_files) #join the full path with the names of the files.
#         strng = open(files) #We need to open the files
#         for lines in strng.readlines(): #We then need to read the files
#             if re.search(pattern, lines): #If we find the pattern we are looking for
#                 print re.split(r'=', lines)[1] #We split using as a delimeter the = sign.
#                 #INSERT WHATEVER CODE YOU WANT