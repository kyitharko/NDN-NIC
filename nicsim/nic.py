from nic_bloom_filter import NicBloomFilter

class Nic:
    def __init__(self, mBuckets):
        self.bf1 = NicBloomFilter(m)
        self.bf2 = NicBloomFilter(m)

    def processPacket(self, netType, name):
        #name is a URI with '/'
        accepted = False
        reasonCode = []

        prefixes = ['/'] 
        components = name.split('/')
     
        for i in range(2,components+1):
            prefix = '/'.join(components[:i])
            prefixes.append(prefix)

        print prefixes

        for prefix in prefixes:
            result = self.bf1.query(prefix)
            if result != False:
                accepted = True
                reasonCode += result

            result = self.bf2.query(name)
            if result != False:
                accepted = True
                reasonCode += result

        return accepted, reasonCode                        


if __name__ == "__main__":
	nic = Nic()
	