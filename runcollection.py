import sys
from collector.agent import GetBytomDataAgent
from collector import flags

FLAGS = flags.FLAGS

if __name__ == "__main__":
    FLAGS(sys.argv)
    my_agent = GetBytomDataAgent()
    my_agent.sync_all()
