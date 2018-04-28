    def request_mongo_recent_height(self):
        height = None
        try:
            state = self.mongo_cli.get(FLAGS.db_status, {})

            if state is None:
                # self.mongo_recent_height = -1
                height = -1

            else:
                height = state[FLAGS.block_height]
                # print "ok! " + str(self.mongo_recent_height)

        except Exception, e:
            self.logger.error("Agent.GetBytomDataAgent request_mongo_recent_height ERROR:" + str(e))
            raise Exception("request_mongo_recent_height error: %s" % str(e))

        return height

    def set_mongo_recent_height(self, height):
        try:
            state = self.mongo_cli.update_one(FLAGS.db_status, {}, {'$set': {FLAGS.block_height: height}}, True)
        except Exception, e:
            self.logger.error("Agent.GetBytomDataAgent set_mongo_recent_height ERROR:" + str(e))
            raise Exception("set_mongo_recent_height error: %s" % str(e))