from collections import Counter
import random, datetime

# todos:
# protokollant selbst bestimmen

def ctrToString(ctr):
	return '\n'.join(['({}, {})'.format(key, value) for key, value in ctr.items()])

def stringToCtr(string):
	lines = string.splitlines()
	ctr = Counter()
	for line in lines:
		left, right = line.strip('()').split(',')
		ctr[left.upper()] = int(right)
	return ctr

try:
	with open('recorder.db', 'r') as f:
		ctr = stringToCtr(f.read())
	print('Loaded db:')
	print(', '.join(ctr.keys()))
except:
	ctr = Counter()
	print('No recorder.db file. Creating new counter.')

ctr_sum = sum(ctr.values())
ctr_len = len(ctr)
try:
	ctr_avg = ctr_sum // ctr_len
except:
	ctr_avg = 1

participant_string = input('Participants: ')

participants = [p.strip().upper() for p in participant_string.replace(';', ',').split(',')]

participants_sum = sum([ctr[p] for p in participants])
if participants_sum == 0:
	participants_sum = len(participants)

print('Probabilities:')

ballotbox = []

for p in participants:
	if not p in ctr:
		ctr[p] = ctr_avg
	print('{:6} {:<5} {:.1%}'.format(p, ctr[p], ctr[p] / participants_sum))
	ballotbox = ballotbox + [p] * ctr[p]

while True:
	choice = random.choice(ballotbox)

	print()
	print('##{}##################'.format('#' * len(choice)))
	print('# {} is the recorder #'.format(choice))
	print('##{}##################'.format('#' * len(choice)))
	print()
	
	while True:
		accept_choice_string = input('Accept choice? [Y/n] ')
		
		if accept_choice_string.strip() in ['Y', 'y', '']:
			accept_choice = True
			break
		elif accept_choice_string.strip() in ['N', 'n']:
			accept_choice = False
			break
			
	if accept_choice:
		break
		
with open('recorder.history', 'a') as f:
	f.write(str(datetime.datetime.now()))
	f.write('\nPre:\n')
	f.write(ctrToString(ctr))
	f.write('\nRecorder: ')
	f.write(choice)

ctr[choice] -= 1

if ctr[choice] == 0:
	for p in ctr:
		ctr[p] += 1

with open('recorder.db', 'w') as f:
	f.write(ctrToString(ctr))

print('Updated recorder.db')

with open('recorder.history', 'a') as f:
	f.write('\nPost:\n')
	f.write(ctrToString(ctr))
	f.write('\n\n')
