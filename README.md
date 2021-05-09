# BlockChain
Implementation of BlockChain in Python

### Methods Implemented Class Block:
* Initialization of Block - __init__()
* Compute Hash for Block - compute_hash()
 
****

### Methods Implemented Class BlockChain:
* Initialization of Blockchain - __init__()
* Calculate hash value by incrementing nonce value - proof_of_work()
* Create new Transaction - new_transaction()
* Check for existing place that already is entered in the Blockchain - search_place_id()
* Create New Block - create_block()
* Verifies the previous hash values and assigns computed hash value to the newly created block - Mining()
* Check for block validity - valid()
* Edit an block to test whether the check_validity method is working fine - update_block()
* Checks validity of the entire Blockchain by again computing the hash code for each block - check_validity()
* Display Blockcahin - display_chain()

****

### Property of Class BlockChain:
* Get the last block of the Blockchain - last_block()

