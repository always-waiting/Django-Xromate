import re

def urlinfo(request):
    path = request.path
    try:
        project = re.search("/projects/([^/]+)/?", path).group(1)
        #print "project: %s##" % project
    except (AttributeError,IndexError) as e:
        project = ''
    try:
        flowcell = re.search("/flowcells/([^/]+)/?", path).group(1)
    except (AttributeError,IndexError) as e:
        flowcell = ''
    try:
        sample = re.search("/samples/([^/]+)/?", path).group(1)
    except (AttributeError,IndexError) as e:
        sample = ''
    return {
        'project': project,
        'flowcell': flowcell,
        'sample': sample,
    }
