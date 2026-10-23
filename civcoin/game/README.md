# CivCoin game prototype

A single-page strategy game: you and three AI rivals trade CivCoin, form alliances, and move through eras on a canvas map. Open `civcoin_game_prototype.html` in a browser to play.

## Contract address

The game reads the CivCoin contract address from the first of these that holds a valid `0x…` address:

1. The URL: `civcoin_game_prototype.html?contract=0xYourContract`
2. The **Contract address** field on the page (saved in this browser's localStorage)
3. `window.CIVCOIN_CONFIG.contractAddress` near the top of the HTML file

The contract is expected to expose `mint(address,uint256)`, `burn(address,uint256)`, `balanceOf(address)` and `transfer(address,uint256)`.

## Offline mode

When MetaMask isn't installed, ethers.js can't load (no internet), no contract address is set, or the wallet isn't connected, the game runs offline. Withdraw and Deposit then move CivCoin between your in-game balance and a local vault stored in the browser, so the whole game is playable without a wallet. The label under the controls shows which mode you're in and why.
