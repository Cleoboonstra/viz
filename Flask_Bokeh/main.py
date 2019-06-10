# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from scripts.OutputFile import hv_graph
# Each tab is drawn by one script
from scripts.histogram import histogram_tab
from scripts.density import density_tab
from scripts.table import table_tab
from scripts.draw_map import map_tab
from scripts.routes import route_tab
from scripts.matrix import matrix_tab
from scripts.matrix_reorder import matrix_reorder_tab
from scripts.Node_link import  node_link_tab
# Using included state data from Bokeh for map
from bokeh.sampledata.us_states import data as states

# Read data into dataframes
# FLIGHTS
flights = pd.read_csv(join(dirname(__file__), 'data', 'flights.csv'), index_col=0).dropna()
# EXAMPLE DATA SETS AUTHOR
GAS = pd.read_csv('data/GephiMatrix_author_similarity.csv', na_values=[''], keep_default_na=False)
GCA= pd.read_csv('data/GephiMatrix_co-authorship.csv',delimiter=';')
GCC = pd.read_csv('data/GephiMatrix_co-citation.csv',delimiter=';')

# WIKIPEDIA
node_df = pd.read_csv('data/articles.tsv',delimiter='\t')  # 4603 articles
links_df = pd.read_csv('data/links.tsv',delimiter='\t')
cat = pd.read_csv('data/categories.tsv', delimiter='\t')
# Formatted Flight Delay Data for map
map_data = pd.read_csv(join(dirname(__file__), 'data', 'flights_map.csv'), header=[0,1], index_col=0)

# Create each of the tabs
# tab1 = histogram_tab(flights)
# tab2 = density_tab(flights)
# tab3 = table_tab(flights)
# tab4 = map_tab(map_data, states)
# tab5 = route_tab(flights)
tab6 = matrix_tab(GAS)
tab7 = matrix_reorder_tab(GAS)
tab8 = node_link_tab(hv_graph)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab6, tab7, tab8])

# Put the tabs in the current document for display
curdoc().add_root(tabs)


