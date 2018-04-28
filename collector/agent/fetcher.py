





    def request_recent_height(self):
        # block id: 0 - recent_height
        url_rpc = self.url_base + '/' + FLAGS.get_block_count
        try:
            r = requests.post(url_rpc)
            chain_height = get_data_part(r)
            return chain_height[FLAGS.block_count]

        except Exception, e:
            self.logger.error("Agent.GetBytomDataAgent request_recent_height ERROR:" + str(e))
            raise Exception("request_recent_height error: %s" % str(e))
            return None


    
    def request_block_info(self, block_height):

        data_dict = {FLAGS.get_block_height_arg: block_height}
        url_rpc = self.url_base + '/' + FLAGS.get_block

        r = requests.post(url_rpc, json.dumps(data_dict))
        block_info =  get_data_part(r)
        return block_info