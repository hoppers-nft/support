
### Requirements
* `vyperlang v0.3.2`
* `brownie`

### Summary
FLY airdrop to each APA, vested for a year.
Allocation depends on the category. 

Since category is an offchain attribute, we need to bring that information onto the chain.

Done with bitpacking where each category is represented by 3 bits. Resulting in an array of 118 `uint256` elements.

#### Allocation
0. Per Common: 50 $FLY
1. Per Rare: 84 $FLY
2. Per Exceptional: 166 $FLY
3. Per Epic: 416 $FLY
4. Per Legendary: 2500 $FLY


### Test
`brownie test`

### Generate bitarrays with categories:

`brownie run scripts/scraper.py --network avax-main`