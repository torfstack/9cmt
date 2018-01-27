import urllib2
import validators
import json
import sys

htmlCodes = (
	("'", '&#39;'),
	('"', '&quot;'),
	('>', '&gt;'),
	('<', '&lt;'),
	('&', '&amp;')
)

def likes(cmt):
	return cmt['likeCount']

def author(cmt):
	return cmt['user']['displayName']

def clean(cmt):
	s = cmt
	for code in htmlCodes:
		s = s.replace(code[1], code[0])
	return s

gagid = "aAxVyE2"
print "Cool stuff"
number_cmts = 10
count = 10
template = "https://comment-cdn.9gag.com/v1/cacheable/comment-list.json?appId=a_dd8f2b7d304a10edaf6f29517ea0ca4100a43d1b&url=http://9gag.com/gag/{}&count={}&level=2&order=score&mentionMapping=true";
url = template.format(gagid, number_cmts)
#print template
resp = json.load(urllib2.urlopen(url))
refCom = "&refCommentId={}"
i = 1
file = open("/home/riyil/Code/9cmt/comments.txt", "w")
for comment in resp['payload']['comments']:
	if count==0:
		sys.exit(0)
	if not validators.url(comment['text'].strip()):
		file.write("Comment #{} -- Author: {} -- Likes: {}\n".format(i,author(comment),likes(comment)))
		file.write(clean(comment['text'])+"\n\n")
		count=count-1

		#print comment['commentId']
		#print template+refCom.format(comment['commentId'])
		if comment['childrenTotal'] > 0:
			child_url = url + "&refCommentId={}".format(comment['children'][0]['commentId'])
			child_resp = json.load(urllib2.urlopen(child_url))
			j = 1
			for child_cmt in child_resp['payload']['comments']:
				if count==0:
					sys.exit(0)
				if not validators.url(child_cmt['text'].strip()):
					file.write("  Comment #{}.{} -- Author: {} -- Likes:{}\n".format(i,j,author(child_cmt),likes(child_cmt)))
					file.write("  "+clean(child_cmt['text'])+"\n\n")
					j=j+1
					count=count-1
			i=i+1