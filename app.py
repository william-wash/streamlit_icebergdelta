import pandas as pd
import matplotlib.pyplot as plt
from pywaffle import Waffle
from matplotlib import rcParams
import streamlit as st
from requests_html import HTMLSession
session = HTMLSession()


iceberg="https://github.com/apache/iceberg/pulse_diffstat_summary?period=monthly"
iceberg_pr="https://github.com/apache/iceberg/pulse/monthly#open-pull-requests"
delta="https://github.com/delta-io/delta/pulse_diffstat_summary?period=monthly"
delta_pr="https://github.com/delta-io/delta/pulse/monthly#open-pull-requests"

r = session.get(delta)
d=r.html.text.split(" ")
d_authors=int(d[2].replace(",",""))
d_commits=int(d[11].replace(",",""))
d_files=int(d[18].replace(",",""))
d_adds=int(d[26].replace(",",""))
d_dels=int(d[29].split()[0].replace(",",""))



r=session.get(delta_pr)
for item in r.html.text.split("\n"):
    if "Active pull requests" in item:
        d_pr = int(item.split(" ")[0].replace(",",""))

print ("Delta Authors %s Commits %s Files %s Adds %s Dels %s Prs %s" % (d[2], d[11], d[18], d[26], d[29].split()[0], d_pr))


r = session.get(iceberg)
i=r.html.text.split(" ")
i_authors=int(i[2].replace(",",""))
i_commits=int(i[11].replace(",",""))
i_files=int(i[18].replace(",",""))
i_adds=int(i[26].replace(",",""))
i_dels=int(i[29].split()[0].replace(",",""))

r=session.get(iceberg_pr)

for item in r.html.text.split("\n"):
    if "Active pull requests" in item:
        i_pr = int(item.split(" ")[0].replace(",",""))

print ("Iceberg Authors %s Commits %s Files %s Adds %s Dels %s Prs %s " % (i[2], i[11], i[18], i[26], i[29].split()[0], i_pr))



# Set params
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Futura']

additions = {'Apache Iceberg': i_adds, 'Delta Lake': d_adds,}
deletions = {'Apache Iceberg': i_dels, 'Delta Lake': d_dels,}
prs = {'Apache Iceberg': i_pr, 'Delta Lake': d_pr,}
authors = {'Apache Iceberg': i_authors, 'Delta Lake': d_authors,}
commits = {'Apache Iceberg': i_commits, 'Delta Lake': d_commits,}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=20,
        plots={
        511: {
            'values': additions,
            'labels': [f"{k} ({v})" for k, v in additions.items()],
            'legend': {'loc': 'lower left','bbox_to_anchor': (0, -0.3),'ncol': len(additions),'framealpha': 0,'fontsize': 9},
            'title': {'label': 'Code Additions','loc': 'left','fontdict': {'fontsize': 16}},
            'colors': ["#2779bd", "#dc361d",]
        },
        512: {
            'values': deletions,
            'labels': [f"{k} ({v})" for k, v in deletions.items()],
            'legend': {'loc': 'lower left','bbox_to_anchor': (0, -0.3),'ncol': len(deletions),'framealpha': 0,'fontsize': 9},
            'title': {'label': 'Code Deletions','loc': 'left','fontdict': {'fontsize': 16}},
            'colors': ["#2779bd", "#dc361d",]
        },
        513: {
            'values': prs,
            'labels': [f"{k} ({v})" for k, v in prs.items()],
            'legend': {'loc': 'lower left','bbox_to_anchor': (0, -0.3),'ncol': len(prs),'framealpha': 0,'fontsize': 9},
            'title': {'label': 'Pull Request (PR) Activity (merged, opened)','loc': 'left','fontdict': {'fontsize': 16}},
            'colors': ["#2779bd", "#dc361d",]
        },
        514: {
            'values': authors,
            'labels': [f"{k} ({v})" for k, v in authors.items()],
            'legend': {'loc': 'lower left','bbox_to_anchor': (0, -0.3),'ncol': len(authors),'framealpha': 0,'fontsize': 9},
            'title': {'label': 'PR Authors','loc': 'left','fontdict': {'fontsize': 16}},
            'colors': ["#2779bd", "#dc361d",]
        },
        515: {
            'values': commits,
            'labels': [f"{k} ({v})" for k, v in commits.items()],
            'legend': {'loc': 'lower left','bbox_to_anchor': (0, -0.3),'ncol': len(commits),'framealpha': 0,'fontsize': 9},
            'title': {'label': 'Commits','loc': 'left','fontdict': {'fontsize': 16}},
            'colors': ["#2779bd", "#dc361d",]
        },
    },
)

fig.set_facecolor('#eeede7')
fig.set_size_inches(10, 10)
st.pyplot(fig)
