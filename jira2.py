import datetime
from collections import Counter
from jira import JIRA

curdate = datetime.datetime.now()

options = {
    'server': 'http://jira.konts.lv'}
jira = JIRA(options)
url = 'http://jira.konts.lv'
authed_jira = JIRA(options, basic_auth=('kudelale', 'London123'))

#boards = authed_jira.boards()
#[print(board.name, 'board_id =', board.id) for board in boards]
#board_id = 43
#print("Customer board: %s (%s)" % (boards[8].name, board_id))

print('Current user:', authed_jira.current_user())
#projects = authed_jira.projects()
#for project in projects:
#   print(project.key, project.name)

issues = authed_jira.search_issues('status in (Open, "In Progress","Workaround provided", Reopened) AND assignee in (kudelale) and due < endOfWeek() ORDER BY updatedDate DESC', maxResults=10000)   
#print('Issues for current user: ', issues)

d = datetime.date(curdate.year, curdate.month, curdate.day+7)
s = d.strftime('%Y-%m-%d')

print('New date will be at: ', s)
print('Total number of overdue issues: ',len(issues))
print('Total number of issues: ',len(authed_jira.search_issues('assignee = currentUser() AND resolution = unresolved ORDER BY priority', maxResults=10000)))
print('Number of closed issues since beginning of year: ',len(authed_jira.search_issues('assignee = currentUser() AND status = Closed AND resolved >= startOfYear() AND resolution != Duplicate AND issueKey > CSS-30000 ORDER BY resolved ASC, created DESC, updated DESC', maxResults=10000)))
print('Overdue issues:')
for issue in issues:
	print(issue, issue.fields.summary)
for issue in issues:

	for field_name in issue.raw['fields']:
		if field_name == 'duedate' and issue.raw['fields']['customfield_10029']['value'] == 'Customer':
			print(issue, issue.fields.summary)		
			print("Field:", field_name, "Value:", issue.raw['fields'][field_name])
			try:
				issue.update(duedate=s)
			except:
				print('Not possible for issue:', issue)
			print("Field:", field_name, "New value:", s)
   

#[print("Field:", field_name, "Value:", issue.raw['fields'][field_name]) for field_name in issue.raw['fields'] if field_name == 'duedate']