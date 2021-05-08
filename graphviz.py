from graphviz import Digraph
import os

# os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
s = Digraph(node_attr={'shape': 'circle'}, strict=True)
# s.attr(style='filled')
# s.attr(color='lightgrey')

s.edges([('Tagged Site', 'Tagged Hourly Data')
            , ('Tagged Site', 'Tagged 6 Dims')
            , ('Tagged 6 Dims', 'Tagged Hourly Data')
            , ('Tagged Hourly Data', 'Contacts')
            , ('Contacts', 'Site')
         ])

s.node('Tagged Site', label='', style='filled', fillcolor='red1', image='Tagged.png')
s.node('Tagged Hourly Data', style='filled', fillcolor='pink1', URL='http://www.yahoo.com/')
s.node('Tagged 6 Dims', style='filled', fillcolor='pink1')

s.node('Contacts', style='filled', fillcolor='green1')
s.node('Site', style='filled', fillcolor='green1')

s.graph_attr["nodesep"] = "1.5"
s.format = 'svg'
s.render('./outputFlow/Tagged', view=False)
s
###Sub Graph
with s.subgraph(name='cluster1') as dimfile:
    dimfile.attr(style='filled')
    dimfile.attr(color='lightgreen')
    dimfile.attr(label='Dimension Files')
    dimfile.node_attr.update(style='filled', color='white')
    dimfile.edges([('Geographic', 'Merged Dim')
                      , ('B2B', 'Merged Dim')
                      , ('MOBILE App Installs', 'Merged Dim')
                      , ('DEVICE', 'Merged Dim')
                      , ('Demographic', 'Merged Dim')
                      , ('ABM', 'Merged Dim')

                   ])

s.edge('Tagged Site', 'Tagged Data', 'Add Date of the file as Attribute')
s.edge('Merged Dim', 'Tagged Data', 'Join on Categories')
# s.edge('cluster1', 'cluster0')
s.edge('Merged Dim', 'Tagged Data', ltail='cluster0', lhead='cluster1')
s.graph_attr["nodesep"] = "1.5"
s.format = 'svg'
s.render('./viz/dr/Tagged21', view=False)
