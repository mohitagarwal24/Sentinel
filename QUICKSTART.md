# 🚀 Sentinel Quick Start

## What is Sentinel?
Sentinel is a blockchain-backed platform for **trustless, fair, and secure** open-source collaboration using:
- **Two-sided staking protocol** (owners + contributors)
- **Verifiable AI agents** for code review
- **Polkadot zk-based identity verification**

## 🏃‍♂️ Quick Start (3 steps)

### 1. Run Setup Script
```bash
./setup.sh
```

### 2. Configure Environment
Edit these files with your API keys:
- `.env` (backend config)
- `monorepo/.env.local` (frontend config)

### 3. Start the Application

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
python main_agent.py
```

**Terminal 2 - Frontend:**
```bash
cd monorepo
npm run dev
```

**Access:** http://localhost:3000

## 🔑 Required API Keys

| Service | Where to Get | Environment File |
|---------|-------------|------------------|
| GitHub OAuth | GitHub Developer Settings | `monorepo/.env.local` |
| GitHub Token | GitHub Personal Access Tokens | `.env` |
| WalletConnect | https://cloud.walletconnect.com/ | `monorepo/.env.local` |

## 📚 Resources
- **Docs:** https://ironjams-organization.gitbook.io/Sentinelv0
- **Demo:** https://www.youtube.com/watch?v=BJkFdprHhmY
- **Contract:** 0x0156962e58CA27B884a0ea120c184b2355A83D50 (Polkadot Paseo)

---
*Need help? Check `SETUP.md` for detailed instructions.*
