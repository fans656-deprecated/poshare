import os

a = [os.path.join(path, f)
        for path, _, files in os.walk('.')
        for f in files
        if f.endswith('.py')
        and 'classroom' in path]
for f in a:
    print f
print 'line of code: ', sum(len(open(f).readlines()) for f in a)
