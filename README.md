# Preprocessing-Data-in-Python

"""
Command line arguments

1. Extract columns with missing values
   
python file.py data.csv --action extract_columns

Ex:
python source.py house-prices.csv --action extract_columns 


2. Count the number of lines with missing data
   
python file.py data.csv --action count_rows  

Ex:
python source.py house-prices.csv --action count_rows  

3. Fill in the missing value using mean, median (for numeric properties) and mode (for the categorical attribute).

python file.py data.csv --action fill_nan --method=mean --column col_name --out=result.csv

python file.py data.csv --action fill_nan --method=median --column col_name  --out=result.csv

python file.py data.csv --action fill_nan --method=mode --column col_name --out=result.csv

Ex:
python source.py house-prices.csv --action fill_nan --method=mean --column LotFrontage --out=result.csv

python source.py house-prices.csv --action fill_nan --method=median --column LotFrontage  --out=result.csv

python source.py house-prices.csv --action fill_nan --method=mode --column MasVnrType --out=result.csv

4. Deleting rows containing more than a particular number of missing values
   
(Example: delete rows with the number of missing values is more than 50% of the number of attributes).

python file.py data.csv --action del_rows --ratio <ratio_value [0,1]> --out=result.csv

Ex:
python source.py house-prices.csv --action del_rows --ratio 0.15 --out=result.csv

5. Deleting columns containing more than a particular number of missing values (Example: delete columns with the number of missing values is more than 50% of the number of samples).

python file.py data.csv --action del_cols --ratio <ratio_value [0,1]> --out=result.csv

Ex:
python source.py house-prices.csv --action del_cols --ratio 0.5 --out=result.csv

6. Delete duplicate samples
   
python file.py data.csv --action drop_dup --out=result.csv

Ex.
python source.py house-prices.csv --action drop_dup --out=result.csv

7. Normalize a numeric attribute using min-max and Z-score methods.
   
python file.py data.csv --action normalize_num --method=min_max --column <col_name> --out=result.csv

python file.py data.csv --action normalize_num --method=zscore --column <col_name> --out=result.csv

Ex.
python source.py house-prices.csv --action normalize_num --method=min_max --column SalePrice --out=result.csv

python source.py house-prices.csv --action normalize_num --method=zscore --column SalePrice --out=result.csv

8. Performing addition, subtraction, multiplication, and division between two numerical attributes.
   
python file.py data.csv --action performing_arithmetic --method=add --column <col_1>,<col_2> --new_column <newCol> --out=result.csv

python file.py data.csv --action performing_arithmetic --method=sub --column <col_1>,<col_2> --new_column <newCol> --out=result.csv

python file.py data.csv --action performing_arithmetic --method=mul --column <col_1>,<col_2> --new_column <newCol> --out=result.csv

python file.py data.csv --action performing_arithmetic --method=div --column <col_1>,<col_2> --new_column <newCol> --out=result.csv

Ex.
python source.py house-prices.csv --action performing_arithmetic --method=add --column 1stFlrSF,2ndFlrSF --new_column newCol --out=result.csv

python source.py house-prices.csv --action performing_arithmetic --method=sub --column 1stFlrSF,2ndFlrSF --new_column newCol --out=result.csv

python source.py house-prices.csv --action performing_arithmetic --method=mul --column 1stFlrSF,2ndFlrSF --new_column newCol --out=result.csv

python source.py house-prices.csv --action performing_arithmetic --method=div --column 1stFlrSF,2ndFlrSF --new_column newCol --out=result.csv


""" 
