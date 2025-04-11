
# EC2 Visualizations with AWS S3 Integration

## **Overview**
This project generates visualizations for stock data of major banks using Python, Matplotlib, and Pandas. The script retrieves historical stock data from the Financial Modeling Prep (FMP) API, processes it, and creates several plots. It automatically uploads the visualizations to an AWS S3 bucket for storage and public access.


## **Features**
1. **Data Retrieval**:
   - Fetch historical stock data for major banks (`JPM`, `BAC`, `C`, `WFC`, and `GS`) using the FMP API.
2. **Visualizations**:
   - Generate boxplots, scatterplots, and histograms of the stock prices.
3. **S3 Integration**:
   - Automatically upload the generated visualization (`bank_data_plots.png`) to an S3 bucket.
4. **Scalable Setup**:
   - Hosted on an Amazon EC2 instance for cloud-based execution and storage.


## **Requirements**
### **Local Environment**
- Python 3.9 or higher
- `pip` (Python package manager)

### **Python Packages**
Install the required Python packages:
```bash
pip install pandas
pip install matplotlib
pip install boto3
pip install requests
