import simplejson

f = open('infos.json', 'r')

count = 0
for line in f:
    try:
        info = simplejson.loads(line)
        count += len(info['news']['images'])
    except Exception, err:
        print err

print count
