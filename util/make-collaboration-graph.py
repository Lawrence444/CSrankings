from csrankings import *
from graphviz import *
import csv
#import networkx as nx
#import matplotlib.pyplot as plt

aicolor = "#32CD32"     # limegreen
syscolor = "#0000ff"    # blue
theorycolor = "#ffff00" # yellow
intercolor = "#ffc0cb"  # pink

colorList = [aicolor, aicolor, aicolor, aicolor, aicolor, syscolor, syscolor, syscolor, syscolor, syscolor, syscolor, syscolor, syscolor, syscolor, syscolor, theorycolor, theorycolor, theorycolor, intercolor, intercolor, intercolor, intercolor, syscolor, syscolor ]

# colorList = ["#f30000", "#0600f3", "#00b109", "#14e4b4", "#0fe7fb", "#67f200", "#ff7e00", "#8fe4fa", "#ff5300", "#640000", "#3854d1", "#d00ed8", "#7890ff", "#01664d", "#04231b", "#e9f117", "#f3228e", "#7ce8ca", "#ff5300", "#ff5300", "#7eff30", "#9a8cf6", "#79aff9", "#bfbfbf", "#56b510", "#00e2f6", "#ff4141", "#61ff41" ]

areaList = [ { "area" : "ai", "title" : "AI" },
	    { "area" : "vision", "title" : "Vision" },
	    { "area" : "mlmining", "title" : "ML" },
	    { "area" : "nlp",  "title" : "NLP" },
	    { "area" : "ir", "title" : "Web & IR" },
	    { "area" : "arch", "title" : "Arch" },
	    { "area" : "comm", "title" : "Networks"},
	    { "area" : "sec", "title" : "Security"},
	    { "area" : "mod", "title" : "DB"},
	    { "area" : "hpc", "title" : "HPC"},
	    { "area" : "mobile", "title" : "Mobile"},
	    { "area" : "metrics", "title" : "Metrics"},
	    { "area" : "ops", "title" : "OS" },
	    { "area" : "plan", "title" : "PL" },
	    { "area" : "soft", "title" : "SE" },
	    { "area" : "act", "title" : "Theory" },
	    { "area" : "crypt", "title" : "Crypto" },
	    { "area" : "log", "title" : "Logic" },
	    { "area" : "graph", "title" : "Graphics" },
	    { "area" : "chi", "title" : "HCI" },
	    { "area" : "robotics", "title" : "Robotics" },
	    { "area" : "bio", "title" : "Comp. Biology" },
	    { "area" : "da", "title" : "Design Automation" },
	    { "area" : "bed", "title" : "Embedded Systems" } ]


def makegraph(institution,fname):
    edges = {}
    dot = Graph(comment=institution,engine='circo')
    # graph = nx.Graph()

    for author in pubs:
        if author in aliases:
            author = aliases[author]
        if facultydict[author] == institution:
            if not author in facultydict:
                # Not in DB.
                continue
            if not author in coauthors:
                dot.node(author.decode('utf8'),color=authorColor[author],style="filled")
                # graph.add_edge(author.decode('utf8'),author.decode('utf8'))
                continue
            foundOne = False
            for coauth in coauthors[author]:
                if coauth in aliases:
                    coauth = aliases[coauth]
                if coauth in facultydict:
                    if facultydict[coauth] == institution:
                        foundOne = True
                        if not (author+coauth) in edges:
                            dot.edge(author.decode('utf8'),coauth.decode('utf8'))
                            # graph.add_edge(author.decode('utf8'),coauth.decode('utf8'))
                        dot.node(author.decode('utf8'),color=authorColor[author],style="filled")
                        if not coauth in pubs:
                            # Not in DB
                            continue
                        dot.node(coauth.decode('utf8'),color=authorColor[coauth],style="filled")
                        edges[author+coauth] = True
                        edges[coauth+author] = True
            if not foundOne:
                # Had co-authors but not at this institution.
                dot.node(author.decode('utf8'),color=authorColor[author],style="filled")
                # graph.add_edge(author.decode('utf8'),author.decode('utf8'))

    dot.render(fname)
    # print(dot.source.encode('utf8'))
    
    # pos = nx.nx_agraph.graphviz_layout(graph)
    #pos = nx.spring_layout(graph,iterations=20)
    #nx.draw_networkx_edges(graph,pos)
    #nx.draw_networkx_nodes(graph,pos)
    #nx.draw_networkx_labels(graph,pos)
    #plt.axis('off')
    # plt.rcParams['text.usetex'] = False
    #plt.figure(figsize=(16,16))
    #plt.savefig("test.png",dpi=300)
    #plt.show()

# name,affiliation
facultydict = {}
with open('faculty-affiliations.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['name'].strip()
        aff = row['affiliation'].strip()
        facultydict[name] = aff

# author,coauthor,year,area
coauthors = {}
with open('faculty-coauthors.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        author = row['author'].strip()
        coauthor = row['coauthor'].strip()
        if not coauthors.has_key(author):
            coauthors[author] = []
        coauthors[author].append(coauthor)
        #if not coauthors.has_key(coauthor):
        #    coauthors[coauthor] = []
        #coauthors[coauthor].append(author)

# alias,name
aliases = {}
with open('dblp-aliases.csv','rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        alias = row['alias'].strip()
        name = row['name'].strip()
        aliases[alias] = name

# Now build up the color mapping.
# color: int -> color
color = {}
i = 0
for c in colorList:
    color[i] = c
    i = i + 1

# areaColor: area name -> color
areaColor = {}
i = 0
for a in areaList:
    areaName = a['area']
    areaColor[areaName] = color[i]
    i = i + 1

pubs = {}

# "name","dept","area","count","adjustedcount","year"

with open('generated-author-info.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        author = row['name'].strip()
        area = row['area'].strip()
        if author in aliases:
            author = aliases[author]
        if not author in pubs:
            pubs[author] = {}
        if not area in pubs[author]:
            pubs[author][area] = 0
        pubs[author][area] = pubs[author][area] + 1

# Compute color for each author.
# First, find max area for each author.

maxareas = {}

for author in pubs:
    maxarea = None
    maxcount = 0
    for area in pubs[author]:
        if pubs[author][area] > maxcount:
            maxarea = area
            maxcount = pubs[author][area]
    maxareas[author] = maxarea

authorColor = {}

for author in maxareas:
    authorColor[author] = areaColor[maxareas[author]]

        
#institution = "University of Massachusetts Amherst"
#makegraph(institution,'umass')
#institution = "University of Washington"
#makegraph(institution,'washington')
#institution = "University of Texas at Austin"
#makegraph(institution,'texas')
#institution = "University of California - San Diego"
#makegraph(institution,'ucsd')
institution = "University of Illinois at Urbana-Champaign"
#makegraph(institution,'uiuc')
#institution = "Purdue University"
#makegraph(institution,'purdue')
#institution = "Cornell University"
#makegraph(institution,'cornell')
institution = "Carnegie Mellon University"
#makegraph(institution,'cmu')
#institution = "Princeton University"
#makegraph(institution,'princeton')
institution = "California Institute of Technology"
#makegraph(institution,'caltech')
#institution = "Harvard University"
#makegraph(institution,'harvard')
#institution = "Yale University"
#makegraph(institution,'yale')
#institution = "University of California - Berkeley"
#makegraph(institution,'berkeley')
#institution = "Stanford University"
#makegraph(institution,'stanford')
