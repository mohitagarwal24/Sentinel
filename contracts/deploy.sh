#!/bin/bash

echo "🚀 Deploying DecentralizedIssueTracker to Sepolia..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file with your PRIVATE_KEY and API keys."
    echo "You can copy from .env.example and fill in your values."
    exit 1
fi

# Load environment variables
source .env

# Check if PRIVATE_KEY is set
if [ -z "$PRIVATE_KEY" ]; then
    echo "❌ PRIVATE_KEY not set in .env file!"
    exit 1
fi

echo "📋 Deployment Options:"
echo "1. Deploy with Infura RPC (requires INFURA_API_KEY)"
echo "2. Deploy with public RPC (no API key needed)"
echo "3. Deploy without verification (fastest)"

read -p "Choose option (1-3): " choice

case $choice in
    1)
        if [ -z "$INFURA_API_KEY" ]; then
            echo "❌ INFURA_API_KEY not set in .env file!"
            exit 1
        fi
        echo "🔄 Deploying with Infura RPC and verification..."
        forge script script/Deploy.s.sol:DeployDecentralizedIssueTracker \
            --rpc-url sepolia \
            --broadcast \
            --verify \
            --etherscan-api-key $ETHERSCAN_API_KEY \
            -vvvv
        ;;
    2)
        echo "🔄 Deploying with public RPC and verification..."
        forge script script/Deploy.s.sol:DeployDecentralizedIssueTracker \
            --rpc-url https://rpc.sepolia.org \
            --broadcast \
            --verify \
            --etherscan-api-key $ETHERSCAN_API_KEY \
            -vvvv
        ;;
    3)
        echo "🔄 Deploying without verification (fastest)..."
        forge script script/Deploy.s.sol:DeployDecentralizedIssueTracker \
            --rpc-url https://rpc.sepolia.org \
            --broadcast \
            -vvvv
        ;;
    *)
        echo "❌ Invalid option!"
        exit 1
        ;;
esac

echo "✅ Deployment complete!"
echo "📝 Check the output above for the contract address."
echo "🔍 You can verify your contract on Etherscan: https://sepolia.etherscan.io/"
