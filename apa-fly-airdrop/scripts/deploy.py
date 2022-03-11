from brownie import Airdrop, accounts

def main():
    acct = accounts.load('deploy')

    APA = "0x880fe52c6bc4ffffb92d6c03858c97807a900691"
    FLY = "0x78ea3fef1c1f07348199bf44f45b803b9b0dbe28"
    startTime = 1647108000 # 12 march 6 pm UTC
    vestingDuration = 15780000 # 6 months

    # 0.03134475 gas
    Airdrop.deploy(APA, FLY, startTime, vestingDuration, {'from': acct})

# brownie run scripts/deploy.py --network avax-test
# brownie run scripts/deploy.py --network avax-main