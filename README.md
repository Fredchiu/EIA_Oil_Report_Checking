# EIA_Oil_Report
To check U.S. EIA oil report every week by Python2.7

## Tested Environment
Ubuntu 16.04 & Python 2.7

## Python Library to install
1. requests
2. beautifulsoup4
3. pdfminer

## Program progress & function
* Download Report from EIA in pdf format and check if the file is exist or not.
* Using pdfminer tranfer to text content
* Using Regular Expression to get the data we need.(Increse / Decrese / Remain )
![realtime_running_pic](https://github.com/Fredchiu/EIA_Oil_Report/blob/master/EIA_report_progressing.png)
# Note
The report format is almost the same,but you may get error by using Regular expression method.

The reson is like this example as below:
Normally re matching "the value" and "the words" are in the same line.
![sameline](https://github.com/Fredchiu/EIA_Oil_Report/blob/master/EIAreport_sameline.png)

However, sometimes are not!!!    
![nextline](https://github.com/Fredchiu/EIA_Oil_Report/blob/master/EIAreport_nextline.png)

## EIA will update report every Wednesday Night 21:00 EST time zone
   Comparison with previous prediction will be updated later.
