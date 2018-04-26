import sys
from agent.agent import GetBytomDataAgent
import flags
import log

FLAGS = flags.FLAGS

if __name__ == "__main__":
    FLAGS(sys.argv)
    my_agent = GetBytomDataAgent()
    my_agent.sync_all()
