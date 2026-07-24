const { ethers } = require("ethers");
const fs = require("fs");
const path = require("path");
require("dotenv").config();

const RPC_ENDPOINTS = [
  process.env.RPC_URL,
  "https://ethereum.publicnode.com",
  "https://1rpc.io/eth",
  "https://eth.drpc.org",
  "https://core.gashawk.io/rpc",
].filter(Boolean);

const PAIR_ADDRESS = ethers.getAddress("0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc");
const ABI = JSON.parse(fs.readFileSync(path.join(__dirname, "abis/IUniswapV2Pair.json")));

async function getWorkingProvider() {
  for (const url of RPC_ENDPOINTS) {
    try {
      console.log(`Trying: ${url}`);
      const provider = new ethers.JsonRpcProvider(url, { chainId: 1, name: "homestead" });
      provider.on("error", () => {}); await provider.getBlockNumber();
      console.log(`Connected: ${url}`);
      return provider;
    } catch (e) {
      console.log(`Failed: ${url} — ${e.shortMessage || e.message}`);
    }
  }
  throw new Error("All RPC endpoints failed.");
}

async function getPrice(pairContract) {
  const reserves = await pairContract.getReserves();
  const price = (Number(reserves[0]) / 1e6) / (Number(reserves[1]) / 1e18);
  return price;
}

async function main() {
  console.log("--- Web3 Trading Engine Started ---");
  const provider = await getWorkingProvider();
  const pairContract = new ethers.Contract(PAIR_ADDRESS, ABI, provider);
  console.log(`Monitoring Pair: ${PAIR_ADDRESS}`);

  const initialPrice = await getPrice(pairContract);
  console.log(`Initial WETH Price: $${initialPrice.toFixed(2)}`);

  provider.on("block", async (blockNumber) => {
    try {
      const price = await getPrice(pairContract);
      console.log(`[Block ${blockNumber}] WETH Price: $${price.toFixed(2)}`);
    } catch (e) {
      console.error(`Block ${blockNumber} error:`, e.shortMessage || e.message);
    }
  });
}

main().catch(console.error);
