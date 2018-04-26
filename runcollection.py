import sys
from agent.agent import GetBytomDataAgent
import flags
import log

FLAGS = flags.FLAGS

if __name__ == "__main__":
    FLAGS(sys.argv)
    agent = GetBytomDataAgent()
    agent.sync_all()
