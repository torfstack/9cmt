import urllib2
import validators
import json
import sys, getopt

htmlCodes = (
	("'", '&#39;'),
	("'", '&#039;'),
	('"', '&quot;'),
	('>', '&gt;'),
	('<', '&lt;'),
	('&', '&amp;')
)

def likes(cmt):
	return cmt['likeCount']

def author(cmt):
	return cmt['user']['displayName']

def hasUrl(cmt):
	for part in cmt['text'].split(" "):
		if validators.url(part):
			return True
	return False

def clean(cmt):
	s = cmt
	for code in htmlCodes:
		s = s.replace(code[1], code[0])
	return s

def appendSpaces(text):
	return text.replace("\n", "\n  ")

def main(argv):
	gagid = "aAxVyE2"
	count = -1
	path = "comments.txt"

	try:
		opts, args = getopt.getopt(argv,"hg:c:p:",["gagid=", "comments=", "path="])
	except getopt.GetoptError:
		print("usage: 9cmt.py -g <gagid> -c <#comments> -p <outputfilepath>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print("usage: 9cmt.py -g <gagid> -c <#comments> -p <outputfilepath>")
			sys.exit()
		elif opt in ("-g", "--gagid"):
			gagid = arg
		elif opt in ("-c", "--comments"):
			count = int(arg)
		elif opt in ("-p", "--path"):
			path = arg

	template = "https://comment-cdn.9gag.com/v1/cacheable/comment-list.json?appId=a_dd8f2b7d304a10edaf6f29517ea0ca4100a43d1b&url=http://9gag.com/gag/{}&count={}&level=2&order=score&mentionMapping=true";
	url = template.format(gagid, count)
	resp = json.load(urllib2.urlopen(url))
	i = 1
	file = open(path, "w")
	if count < 0:
		count = int(resp['payload']['total'])
	for comment in resp['payload']['comments']:
		if count==0:
			sys.exit(0)
		if not hasUrl(comment):
			file.write("Comment #{} -- Author: {} -- Likes: {}\n".format(i,author(comment),likes(comment)))
			file.write(clean(comment['text'].strip())+"\n\n")
			count=count-1
			if comment['childrenTotal'] > 0:
				child_url = url + "&refCommentId={}".format(comment['children'][0]['commentId'])
				child_resp = json.load(urllib2.urlopen(child_url))
				j = 1
				for child_cmt in child_resp['payload']['comments']:
					if count==0:
						sys.exit(0)
					if not hasUrl(child_cmt):
						file.write("  Comment #{}.{} -- Author: {} -- Likes:{}\n".format(i,j,author(child_cmt),likes(child_cmt)))
						file.write("  "+appendSpaces(clean(child_cmt['text'].strip()))+"\n\n")
						j=j+1
						count=count-1
				i=i+1

if __name__ == "__main__":
	main(sys.argv[1:])
