import os
import os.path as osp

def make_full_dropdown():
    return '\n'.join(map(make_dropdown_str, ['Ant', 'Cheetah', 'Hand', 'Swimmer']))

def make_dropdown_str(name):
    return ("<li class='dropdown'>\n"+\
    "  <a class='dropdown-toggle' data-toggle='dropdown' href='#'>%s <span class='caret'></span></a>\n"%str.title(name)+\
    "  <ul class='dropdown-menu'>\n"+\
    "    <li><a data-toggle='tab' onclick=change_contents('%s-valor-categorical')>VALOR, Categorical</a></li>\n"%str.lower(name)+\
    "    <li><a data-toggle='tab' onclick=change_contents('%s-valor-curriculum')>VALOR, Curriculum</a></li>\n"%str.lower(name)+\
    "    <li><a data-toggle='tab' onclick=change_contents('%s-vic-categorical')>VIC, Categorical</a></li>\n"%str.lower(name)+\
    "    <li><a data-toggle='tab' onclick=change_contents('%s-vic-curriculum')>VIC, Curriculum</a></li>\n"%str.lower(name)+\
    "    <li><a data-toggle='tab' onclick=change_contents('%s-diayn-categorical')>DIAYN, Categorical</a></li>\n"%str.lower(name)+\
    "    <li><a data-toggle='tab' onclick=change_contents('%s-diayn-curriculum')>DIAYN, Curriculum</a></li>\n"%str.lower(name)+\
    "  </ul>\n"+\
    "</li>")

def pane_str(root, files):
    if len(root.split('/')) == 4:
        _, env, algo, dist = root.split('/')
    else:
        _, env, algo = root.split('/')
        dist = 'curriculum'
    name = '-'.join([env, algo, dist])
    header = ', '.join([str.title(env), str.upper(algo), str.title(dist)])

    return name, ("<div id='%s' class='tab-pane fade in'>\n"%name+\
    "  <h3>%s</h3>\n"%header+\
    "  <p>Options trained with %s context distribution:<p>\n"%dist+\
    full_vid_str(root, files) + '\n' + \
    "</div>")

def full_vid_str(root, files):
    all_vid_strs = [vid_str(osp.join(root, file)) for file in files]
    row_strs = ['<center>']
    for j in range(0,10,3):
        row_strs.append(''.join(all_vid_strs[slice(j,j+3)]))
    row_strs.append('</center>')
    return '\n'.join(row_strs)

def vid_str(src):
    return ("<video width='320' height='240' controls autoplay loop>\n"+\
           "  <source src='%s' type='video/mp4'>\n"+\
           "Your browser does not support the video tag.\n"+\
           "</video>")%src

stuff = dict()
for root, _, files in os.walk('videos'):
    for file in files:
        if 'mp4' in file:
            if root in stuff:
                stuff[root].append(file)
            else:
                stuff[root] = [file]
            print(os.path.join(root,file))

all_pane_strs = [pane_str(root, files) for root, files in stuff.items()]

for ps in all_pane_strs:
    with open(ps[0], 'w') as f:
        f.write(ps[1])
        f.close()