from hashlib import sha256
import datetime
import copy

class Block:
    def __init__(self, index, timestamp, transaction, prev_hash, nonce):
        ''' Initialization block'''
        self.index = index
        self.timestamp = timestamp
        self.transaction = transaction
        self.prev_hash = prev_hash
        self.nonce = nonce

    def compute_hash(self):
        ''' computes basic in-built hash and return hash code '''
        hash_code = sha256(str(self.__dict__).encode()).hexdigest()
        return hash_code


class BlockChain:
    def __init__(self):
        # initialize the Blockchain and create the first Empty block of the chain and append to blockchain
        self.transt = []
        self.chain = []
        block = Block(0, datetime.datetime.now(), {}, "0", 0)
        block.hash = block.compute_hash()
        self.chain.append(block)

    @property
    def last_block(self):
        # returns last block
        return self.chain[-1]

    def proof_of_work(self, block):
        # finds the perfect hash value and updates the nonce of the block
        # return perfect computed hash value
        block.nonce = 1
        computed_hash = block.compute_hash()
        while not computed_hash.startswith("0000"):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def new_transaction(self):
        # creates new transaction
        lat = float(input("Enter Latitude: "))
        if lat < -90 or lat > 90:
            print("Latitude is out of range!")
            return False
        long = float(input("Enter Longitude: "))
        if long < -180 or long > 180:
            print("longitude is out of range!")
            return False
        latlong = {'lat': lat, 'long': long}
        place_id = sha256(str(latlong).encode()).hexdigest()
        from_name = input("Enter Name of previous owner: ")
        if self.search_place_id(place_id, from_name) is True:
            print("\n\nThis record already exits and the previous owner name doen't match with the current owner entered")
            return False
        to_name = input("Enter Name of current owner: ")
        area = float(input("Enter sqft. area: "))
        self.transt.append(
            {'lat': lat, 'long': long, 'place_id': place_id, 'from_name': from_name, 'to_name': to_name, 'area': area})
        # self.transt.append({'lat': lat, 'long': long, 'place_id': place_id})
        return True

    def search_place_id(self, place_id, from_name):
        # Check if the place already exits in the chain
        # Returns True if already exits
        flag=0
        i = iter(self.chain)
        completed_iterating = False
        while not completed_iterating:
            try:
                k = i.__next__()
                plcid = "".join(map(str, [d['place_id'] for d in k.transaction]))
                toname = "".join(map(str, [d['to_name'] for d in k.transaction]))
                if place_id == plcid and from_name != toname:
                    flag=1
                elif place_id == plcid and from_name == toname:
                    flag = 0
            except StopIteration:
                completed_iterating = True
                if flag==1:
                    print("place id computed than sent: ", plcid, place_id)
                    print("To_name computed than from_name: ", from_name, toname)
                    return True

        return False

    def create_block(self):
        # creates block, calculates the perfect hash code, adds block to the chain
        # returns the newly added block
        if not self.transt:
            print("No transaction data present!")
            return False
        last_block = self.last_block
        block = Block(index=self.last_block.index + 1, timestamp=datetime.datetime.now(), transaction=self.transt,
                      prev_hash=last_block.hash, nonce=0)
        computed_hash_value = self.proof_of_work(block)
        if not self.Mining(block, computed_hash_value):
            self.transt = []
            return False
        self.transt = []
        return block

    def Mining(self, block, computed_hash_value):
        # verifies the has code, verifies the previous hash values, assigns hash value to block, appends block to chain
        previous_hash = self.last_block.hash
        if previous_hash != block.prev_hash:
            print("previous_hash != block.prev_hash")
            return False
        if not self.valid(block, computed_hash_value):
            print("validity function returned False")
            return False
        block.hash = computed_hash_value
        self.chain.append(block)
        print("\n ****** Block is added to chain ******")
        return True

    def valid(self, block, computed_hash_value):
        # checks if the block is valid
        if computed_hash_value.startswith("0000") and block.compute_hash() == computed_hash_value:
            return True
        else:
            print("\n\nValidity function is False")
            return False

    def update_block(self):
        # Update the block timestamp with the current timeshamp for testing purpose
        # If the block data is updated, the computed hash value will vary making the block invalid
        # Testing purpose for check_validity function
        j=int(input("\nEnter the index of the block that you want to update: "))
        while self.last_block.index < j or j < 1 :
            print("Invalid index entered!")
            j=int("Enter the index of the block that you want to update: ")
        i = iter(self.chain)
        completed_iterating = False
        while not completed_iterating:
            try:
                k = i.__next__()
                if k.index == j:
                    k.timestamp=datetime.datetime.now()
                    print("\n\nWe have updated the timestamp for testing purpose!")
                    return
            except StopIteration:
                completed_iterating = True
                print("\nCouldn't update the blockchain!")

    def check_validity(self):
        # Check the validity of the blockchain
        # Again try to compute the hash and match it with the current assigned hash of the block
        # if the hash matched, the function is valid
        i = iter(self.chain)
        k = i.__next__()
        completed_iterating = False
        while not completed_iterating:
            try:
                k = i.__next__()
                # As hash value and nonce is already calculated for the block
                # we need to get rid of it to compute the hash of only the data of the transaction
                temp=copy.deepcopy(k)
                temp.__dict__.pop('hash')
                temp.nonce=1
                computed_hash_value = self.proof_of_work(temp)
                if k.hash != computed_hash_value:
                    print("\n\nThe blockchain is invalid at block ", k.index)
                    print("You will have to delete the blockchain and create a new one!")
                    return False
            except StopIteration:
                completed_iterating = True
                print("\n\n************* The Blockchain is Valid! **************\n")
                return True


    def display_chain(self):
        # display blockchain
        # create iterator to traverse the chain
        i = iter(self.chain)
        completed_iterating = False
        while not completed_iterating:
            try:
                k = i.__next__()
                print("************************************************************************************")
                print("Hash Value: ", k.hash)
                print("Index: ", k.index)
                print("Timestamp: ", k.timestamp)
                print("Latitude: ", "".join(map(str, [d['lat'] for d in k.transaction])))
                print("Longitude: ", "".join(map(str, [d['long'] for d in k.transaction])))
                print("Place ID: ", "".join(map(str, [d['place_id'] for d in k.transaction])))
                print("Last Owner: ", "".join(map(str, [d['from_name'] for d in k.transaction])))
                print("Current Owner: ", "".join(map(str, [d['to_name'] for d in k.transaction])))
                print("Area in sqft.: ", "".join(map(str, [d['area'] for d in k.transaction])))
                print("Previous Hash: ", k.prev_hash)
                print("Nonce: ", k.nonce)
            except StopIteration:
                completed_iterating = True


if __name__ == '__main__':
    blockchain = BlockChain()
    ch = 0
    while (ch != 6):
        print("\n")
        print("1.Insert a block")
        print("2.Display Blockchain")
        print("3.Check if block chain is valid")
        print("4.Update block (This will make the blockchain invalid)")
        print("5.Delete Blockchain")
        print("6.EXIT")
        ch = int(input("Enter Your Choice:"))
        if ch == 1:
            if blockchain.last_block.index == 0:
                if blockchain.new_transaction():
                    blockchain.create_block()
            else:
                if blockchain.check_validity():
                    if blockchain.new_transaction():
                        blockchain.create_block()
        elif ch == 2:
            if blockchain.last_block.index == 0:
                print("These are no blocks created ")
            else:
                blockchain.display_chain()
        elif ch == 3:
            if blockchain.last_block.index == 0:
                print("These are no blocks created ")
            else:
                blockchain.check_validity()
        elif ch == 4:
            if blockchain.last_block.index == 0:
                print("These are no blocks created ")
            else:
                blockchain.display_chain()
                blockchain.update_block()
        elif ch == 5:
            del blockchain
            print("Blockchain is deleted!")
            blockchain = BlockChain()
        elif ch == 6:
            break;
        else:
            print("Unknown input. Kindly enter correct choice!")


