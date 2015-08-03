import click


@click.command()
@click.option('--num-versions', '-n', default=2, help='The number of versions')
@click.option('--shuffle-problems', '-sp', is_flag=True, help='Also shuffle problems')
@click.argument('examfile', type=click.File('r'), required=True)

def main(examfile, num_versions, shuffle_problems):
    """A multiple choice question shuffler"""
    shuffle_mcqs(examfile, num_versions, shuffle_problems)

import re, os
from random import shuffle

def shuffle_items(p):
    items = re.findall(r'(\\item.*)', p.group(0))
    shuffle(items)
    s = re.sub(r'(\\item.*)',lambda m: items.pop(), p.group(0))
    return s

def shuffle_mcqs(examfile, num_versions=2, shuffle_problems=False):
    versions = range(1,num_versions+1)
    exam = examfile.read()
    for v in versions:
        exam_v = re.sub("Version XX","Version " + str(v), exam)
        exam_v = re.sub("version XX","version " + str(v), exam_v)
        exam_v = re.sub(r'%BeginMCItems(.*?)%EndMCItems', shuffle_items, exam_v, flags=re.DOTALL|re.MULTILINE)
        problems = re.findall(r'%BeginMCProblem(.*?)%EndMCProblem', exam_v, flags=re.DOTALL|re.MULTILINE)
        if shuffle_problems:
            shuffle(problems)
        exam_v = re.sub(r'%BeginMCProblem(.*?)%EndMCProblem', lambda m: problems.pop(0), exam_v, flags=re.DOTALL|re.MULTILINE)
        fvn = examfile.name[:-4] + "-" + str(v) + ".tex"
        fv = open(fvn, 'w')
        fv.write(exam_v)
        fv.close()
        click.echo("Wrote " + os.path.abspath(fv.name))
    examfile.close()
