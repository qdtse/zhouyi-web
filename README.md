# Zhouyi Divination System (周易卜卦系统)

An ancient Chinese divination system built with Python (FastAPI) and modern Web technologies. It includes Meihua Yishu (Plum Blossom Divination), Zhuge Shenshu, Bazi (Four Pillars of Destiny), Ziwei Dou Shu, and more.

## Features

- **Text Divination**: Analyze names, companies, or phone numbers using Meihua Yishu.
- **Zhuge Shenshu**: Traditional 384 lots divination.
- **Number Divination**: Cast hexagrams using two numbers.
- **Time Divination**: Cast hexagrams based on current date and time.
- **Random Divination**: Virtual coin tossing (6 lines).
- **Ziwei Dou Shu**: Generate natal charts (Star Chart).
- **Bazi Analysis**: Four Pillars of Destiny analysis and Five Elements balance.
- **Marriage Compatibility**: Check compatibility based on Bazi.
- **Multi-language Support**: Chinese, English, and French.

## Installation

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn lunar_python pdfplumber
   ```

2. Run the server:
   ```bash
   python server.py
   ```

3. Open browser at `http://localhost:8000`

## License & Copyright

**Copyright (C) 2026 Sugarworm**

This program is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License as published by the Free Software Foundation**, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
