import json
import streamlit
from streamlit_agraph import agraph, Node, Edge, Config


def load_graph_data():
    nodes = []
    edges = []
    with open("./data/marvel.json", encoding="utf8") as f:
        marvel_file = json.loads(f.read())
        nodes.append(
            Node(id=marvel_file["name"],
                 label=marvel_file["name"],
                 shape="circularImage",
                 image=marvel_file["img"])
        )
        for sub_graph in marvel_file["children"]:
            nodes.append(Node(id=sub_graph["name"]))
            edges.append(Edge(source=sub_graph["name"], target=marvel_file["name"], label="subgroup_of"))
            for node in sub_graph["children"]:
                nodes.append(Node(id=node["hero"],
                                  title=node["link"],
                                  shape="circularImage",
                                  image=node["img"],
                                  group=sub_graph["name"],
                                  )
                             )
                edges.append(Edge(source=node["hero"], target=sub_graph["name"], label="blongs_to"))
    return nodes, edges

nodes, edges = load_graph_data()

from streamlit_agraph.config import Config, ConfigBuilder

# 1. Build the config (with sidebar to play with options) .
config_builder = ConfigBuilder(nodes)
config = config_builder.build()

# 2. If your done, save the config to a file.
config.save("config.json")

# 3. Simple reload from json file (you can bump the builder at this point.)
config = Config(from_json="config.json")


return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)


