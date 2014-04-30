import nose
import sys
loop = 1
if sys.argv[1] == '--loop':
    loop = sys.argv[2]
inputs = ['', '--with-plan-loader', '--with-device-config', '--with-file-output','--verbosity=2']
for i in range(int(loop)):
    nose.run(argv=inputs)