from strep.index_scale import load_database, scale_and_rate
from strep.elex.app import Visualization

fname = "./results.csv"
# load database and meta information (if available)
database, meta = load_database(fname)
# index-scale and rate database
rated_database = scale_and_rate(database, meta)
# start the interactive exploration tool
app = Visualization(rated_database)
app.run(port=8899)