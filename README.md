# Octopus Energy Tracker

📊 A Python tool to fetch and visualize your daily energy consumption and costs from **Octopus Energy**, with detailed tariff breakdown and savings analysis.

Track your spending across different tariff periods and see exactly how much you're saving with dynamic time-of-use pricing.

## Features

✨ **Visualizations:**
- 3-panel weekly dashboard with daily consumption, cost comparison, and savings
- Color-coded tariff periods (shoulder, mid-peak, peak)
- Side-by-side comparison of Octopus vs flat-rate pricing
- Line graphs showing cumulative costs and trends

🔒 **Security:**
- API credentials stored in environment variables (`.env`)
- Credentials never committed to repository
- `.env` automatically excluded via `.gitignore`

📊 **Analytics:**
- Weekly consumption summary and daily breakdown
- Tariff period analysis (see which times cost you most)
- Savings calculation vs flat-rate comparison
- Automatic fallback to demo data if API unavailable

## Quick Start

1. **Clone the repository:**

   ```bash
   git clone https://github.com/YOUR_USERNAME/octopus-energy-tracker.git
   cd octopus-energy-tracker
   ```

2. **Create virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure credentials:**
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your Octopus Energy credentials (get these from your [account settings](https://octopus.energy/dashboard/developer/)):
     - `OCTOPUS_API_KEY`: Your API key
     - `OCTOPUS_MPAN`: Your meter point identification number
     - `OCTOPUS_SERIAL_METER`: Your meter serial number

   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

5. **Run the script:**

   ```bash
   export $(cat .env | xargs)
   python main.py
   ```

### IDE Debugging

**PyCharm:**
1. Open `Run` → `Edit Configurations...`
2. Select your Python configuration (or create a new one)
3. Under `Environment variables`, add:
   ```
   OCTOPUS_API_KEY=your_api_key;OCTOPUS_MPAN=your_mpan;OCTOPUS_SERIAL_METER=your_serial_meter
   ```
   (Use `;` as separator on Windows, `:` on macOS/Linux)
4. Click `Apply` and debug normally

**VS Code:**
1. Add to `.vscode/launch.json`:
   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Python: Main",
         "type": "python",
         "request": "launch",
         "program": "${workspaceFolder}/main.py",
         "console": "integratedTerminal",
         "env": {
           "OCTOPUS_API_KEY": "your_api_key",
           "OCTOPUS_MPAN": "your_mpan",
           "OCTOPUS_SERIAL_METER": "your_serial_meter"
         }
       }
     ]
   }
   ```
2. Run with `F5` or `Run → Start Debugging`

**Command Line:**
```bash
export $(cat .env | xargs)
python main.py
```

**Note:** `.env` is in `.gitignore` so your credentials will never be accidentally committed.

## Output

The script displays:

- **3-panel weekly visualization** with daily consumption, cost comparison, and savings
- **Summary statistics**: Total consumption, costs, and savings
- **Daily breakdown**: Consumption and costs for each day
- **Period breakdown**: Costs by tariff period across the week

## Project Structure

```
octopus-energy-tracker/
├── main.py              # Visualization and reporting
├── data.py              # API data fetching
├── consumption.py       # Data processing and tariff calculations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## How It Works

1. **`data.py`**: Fetches hourly consumption data from Octopus Energy API for the last 7 days
2. **`consumption.py`**: Processes the raw data and applies current tariff rates
3. **`main.py`**: Generates visualizations and calculates savings

The script automatically falls back to demo data if the API is unavailable, so you can always test the visualization.

## Tariff Rates (Current)

| Period | Time | Rate |
|--------|------|------|
| Off-peak (night) | 00:00 - 04:00 | 28.82p/kWh |
| Shoulder | 04:00 - 07:00 | 14.13p/kWh |
| Mid-peak | 07:00 - 13:00 | 28.82p/kWh |
| Shoulder | 13:00 - 16:00 | 14.13p/kWh |
| Peak (evening) | 16:00 - 19:00 | 43.22p/kWh |
| Off-peak (evening) | 19:00 - 22:00 | 28.82p/kWh |
| Shoulder | 22:00 - 00:00 | 14.13p/kWh |

Update these in `consumption.py` if your tariff changes.

## Troubleshooting

**"Missing Octopus credentials"**
- Make sure you've created `.env` file and added all three credentials
- Check that environment variables are correctly set: `echo $OCTOPUS_API_KEY`

**"No consumption data available"**
- The API might be temporarily unavailable
- The script will use demo data to show you how the visualizations work
- Check your API key is valid on [Octopus Dashboard](https://octopus.energy/dashboard/developer/)

**IdealIDE debugging not working**
- Ensure environment variables are set in your IDE's run configuration
- Test from command line first: `export $(cat .env | xargs) && python main.py`

## Contributing

Contributions are welcome! Feel free to:
- Report bugs as GitHub issues
- Suggest new features
- Submit pull requests with improvements

## License

MIT License - feel free to use this project however you like.

## Disclaimer

This is an unofficial tool not affiliated with Octopus Energy. Use at your own discretion.
