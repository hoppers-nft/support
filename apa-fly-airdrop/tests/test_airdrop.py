import pytest, brownie


@pytest.fixture
def fly(ERC20, accounts):
    fly = ERC20.deploy("FLY", "FLY", 18, 0, {"from": accounts[0]})
    fly.mint(accounts[0], 10e8, {"from": accounts[0]})
    return fly


@pytest.fixture
def apa(ERC721, accounts):
    apa = ERC721.deploy({"from": accounts[0]})
    apa.mint(accounts[0], 0, {"from": accounts[0]})
    return apa


@pytest.fixture
def airdrop_contract(Airdrop, chain, accounts, fly, apa):
    yield Airdrop.deploy(apa, fly, chain.time(), 60 * 60 * 24, {"from": accounts[0]})


def test_all_tokens(Airdrop, apa, fly, chain, accounts):
    start = chain.time()
    duration = 60 * 60 * 24 * 365
    batch = 100

    airdrop_contract = Airdrop.deploy(
        apa, fly, chain.time(), duration, {"from": accounts[0]}
    )

    # Should have not changed
    assert airdrop_contract.claimable([0]) == 0

    # Prepare arguments
    tokens = []
    for i in range(10_000):
        tokens.append(i)
    assert len(tokens) == 10_000

    tokensFullReward = 1_000_680 * 10**18

    # Fund Airdrop Contract
    fly.mint(airdrop_contract, tokensFullReward, {"from": accounts[0]})

    # Should be there kinda half (minted before)
    chain.sleep(int(duration / 2))
    chain.mine()

    claimable = 0
    for i in range(int(10_000 / batch)):
        claimable += airdrop_contract.claimable(tokens[i * batch : i * batch + batch])

    assert int(claimable / 10**18) == int(
        ((tokensFullReward * (chain.time() - start)) / duration) / 10**18
    )

    # Should all be there
    chain.sleep(int(duration / 2))
    chain.mine()
    claimable = 0
    for i in range(int(10_000 / batch)):
        claimable += airdrop_contract.claimable(tokens[i * batch : i * batch + batch])
    assert claimable == tokensFullReward

    assert airdrop_contract.claimable([102]) == 2500*1e18

    # Make sure other people cannot claim
    beforeBalance = fly.balanceOf(accounts[1])
    with brownie.reverts():
        airdrop_contract.claim(tokens[:50], {"from": accounts[1]})
    assert fly.balanceOf(accounts[1]) == beforeBalance

    # Make sure the owner received FLY
    beforeBalance = fly.balanceOf(accounts[0])
    for i in range(int(10_000 / batch)):
        airdrop_contract.claim(
            tokens[i * batch : i * batch + batch], {"from": accounts[0]}
        )
    assert fly.balanceOf(accounts[0]) == beforeBalance + tokensFullReward

    # Should be 0
    chain.sleep(60 * 60 * 12 * 3)
    chain.mine()
    claimable = 0
    for i in range(int(10_000 / batch)):
        claimable += airdrop_contract.claimable(tokens[i * batch : i * batch + batch])
    assert claimable == 0
