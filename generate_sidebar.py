import os

content = '''-   About me
    -   [My technology blog](https://www.cometeme.tech)
    -   [My GitHub](https://github.com/cometeme)
'''

with open('docs/_sidebar.md', 'w') as f:
    for oj in sorted(filter(lambda x: '.' not in x, os.listdir('docs'))):
        f.write('-  {}\n'.format(oj))
        
        problems = sorted(filter(lambda x: '.md' in x, os.listdir('docs/{}'.format(oj))), key=lambda x : x.rjust(20, '0'))

        for problem in problems:
            with open('docs/{}/{}'.format(oj, problem)) as p:
                f.write(
                    '   -   [{}]({})\n'.format(p.readline().strip(' #\n'), '/{}/{}'.format(oj, problem)))

        f.write('\n')

    f.write(content)
