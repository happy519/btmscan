import sys
from collector import agent
from tools import flags

FLAGS = flags.FLAGS

if __name__ == "__main__":
    FLAGS(sys.argv)
    my_agent = agent.GetBytomDataAgent()
    my_agent.sync_all()
