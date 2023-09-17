#Preprocessing Data in Python

import csv
import argparse

def mean(numbers):
    return sum(numbers)/len(numbers)

def median(numbers):
    sorted_numbers = sorted(numbers)
    mid = len(sorted_numbers) // 2
    
    if len(sorted_numbers) % 2 == 0:
            return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    else:
            return sorted_numbers[mid]
        
def mode(numbers):
    freq = {}
    for n in numbers:
        if n in freq:
            freq[n] += 1
        else:
            freq[n] = 1
    mode = max(freq, key=freq.get)
    return mode    

def std(numbers):
    avg = mean(numbers)
    squared_diff = [(num - avg) ** 2 for num in numbers]
    var = sum(squared_diff) / len(numbers)
    return var ** 0.5


# FUNCTIONS 1: Extract columns with missing values
def extract_columns_with_missing_values(input_file):
    #Open the CSV file
    with open(input_file, 'r') as f:
        data = csv.reader(f)
        
        #Get the header row and index of columns with missing values
        header = next(data)
        missing_indices = set()
        for row in data:
            while '' in row:
                idx=row.index('')
                missing_indices.add(idx)
                row[idx]='none'
                  
        print("Columns with missing values:")
        for i in sorted(missing_indices):
            print(header[i])

# FUNCTIONS 2: Count the number of lines with missing data
def count_missing_rows(input_file):
    #Open the CSV file
    with open(input_file, 'r') as f:
        data = csv.reader(f)

        #Count the number of rows with missing values
        num_missing_rows = 0
        for row in data:
            if '' in row:
                num_missing_rows += 1

        print("Number of rows with missing values: {}".format(num_missing_rows))

# FUNCTIONS 3: Fill in the missing value using mean, median (for numeric properties) and mode (for the categorical attribute).        
def fill_missing_values(input_file,method,column,output_file):
    with open(input_file, "r") as fi:
        reader = csv.reader(fi)
        header = next(reader)
        data = [row for row in reader]
        col_idx=header.index(column)
        
    
        if method == 'mean':
            col_values = [float(row[col_idx]) for row in data if row[col_idx] != ""]
            
            #Calculate mean values
            col_mean=mean(col_values)
            
            #Fill missing values
            for row in data:
                if row[col_idx] == "":
                    row[col_idx] = str(col_mean)
                    
            print("Filled missing values with mean= {}".format(col_mean))
        
        if method =='median':
            col_values = [float(row[col_idx]) for row in data if row[col_idx] != ""]
            
            #Calculate median values
            col_median =median(col_values)
                
            #Fill missing values
            for row in data:
                if row[col_idx] == "":
                    row[col_idx] = str(col_median)    
                    
            print("Filled missing values with median= {}".format(col_median))   
            
        if method =='mode':
            col_values = [row[col_idx] for row in data if row[col_idx] != ""]
            
            #Find mode values
            col_mode=mode(col_values)
            
            #Fill missing values
            for row in data:
                if row[col_idx] == "":
                    row[col_idx] =col_mode

            print("Filled missing values with mode= {}".format(col_mode))
        
        #Wrtter data to file     
        with open(output_file, "w", newline="") as fo:
            writer = csv.writer(fo)
            writer.writerow(header)
            writer.writerows(data)

#FUNCTION 4: Deleting rows containing more than a particular number of missing values
def del_rows(input_file, ratio,output_file):
    with open(input_file, 'r') as fi, open(output_file, 'w', newline='') as fo:
        data = csv.reader(fi)
        header = next(data)
        
        writer = csv.writer(fo)
        writer.writerow(header)
        
        for row in data:
            missing_count = sum([1 for value in row if value == ''])
            if missing_count / len(row) <= ratio:
                writer.writerow(row)
                
    print("Rows with more than {} missing values have been removed.".format(ratio))
    
#FUNCTION 5: Deleting columns containing more than a particular number of missing values
def del_cols(input_file,ratio,output_file):
    with open(input_file, 'r') as fi:
        reader = csv.reader(fi)
        header = next(reader)
        data = [row for row in reader]

        #Count the number of missing values for each column
        num_missing_values = [0] * len(header)
        for row in data:
            for i, value in enumerate(row):
                if value.strip() == '':
                    num_missing_values[i] += 1

        #Remove the columns with missing values more than ratio
        columns_to_keep = [i for i, num_missing in enumerate(num_missing_values) if num_missing <= ratio*len(data)]
        filtered_data = [[row[i] for i in columns_to_keep] for row in data]

        with open(output_file, 'w', newline='') as fo:
            writer = csv.writer(fo)
            writer.writerow(header[i] for i in columns_to_keep)
            writer.writerows(filtered_data)
            
        print("Columns with more than {} missing values have been removed.".format(ratio))
    
#FUNCTION 6: Delete duplicate samples.
def drop_duplicate(input_file, output_file):
    with open(input_file,'r') as fi,open(output_file, 'w', newline='') as fo:
        data = csv.reader(fi)
        header = next(data)
        
        writer = csv.writer(fo)
        writer.writerow(header)
        
        seen = []
        for row in data:
            if row not in seen:
                seen.append(row)
                writer.writerow(row)
                
        print("Duplicate samples was deleted.")
        
#FUNCTION 7: Normalize a numeric attribute using min-max and Z-score method
def normalize_min_max(data, column_index):
    column_data = [float(row[column_index]) for row in data if row[column_index] != '']
    column_min = min(column_data)
    column_max = max(column_data)

    for row in data:
        if row[column_index] != '':
            row[column_index] = (float(row[column_index]) - column_min) / (column_max - column_min)

    return data

def normalize_zscore(data,column_index):
    mu = mean(list(float(row[column_index]) for row in data))
    sigma = std(list(float(row[column_index]) for row in data))
    
    if sigma == 0:
        for row in data:
            if row[column_index] != '':
                row[column_index]=0
                return data
            
    for row in data:
        if row[column_index] != '':
            row[column_index]=(float(row[column_index]) - mu) / sigma
    return data

def normalize_numeric(input_file,method,column,output_file):
    with open(input_file, 'r') as fi:
        reader = csv.reader(fi)
        header = next(reader)
        
        data = [row for row in reader]
        column_index=header.index(column)
        
        if method=='min_max':
            data=normalize_min_max(data,column_index)
            print("The attribute is normalized by using min-max scaling.")
            
        if method=='zscore':
            data=normalize_zscore(data,column_index)
            print("The attribute is normalized by using z-score normalization.")
            
        with open(output_file, 'w', newline='') as fo:
            writer = csv.writer(fo)
            writer.writerow(header)
            writer.writerows(data)
            
#FUNCTION 8: Performing addition, subtraction, multiplication, and division between two numerical attributes
def add_columns(data, col1, col2):
    for row in data:
        if row[col1] and row[col2]:
            row.append(float(row[col1]) + float(row[col2]))
    return data   

def subtract_columns(data, col1, col2):
    for row in data:
        if row[col1] and row[col2]:
            row.append(float(row[col1]) - float(row[col2]))
    return data

def multiply_columns(data, col1, col2):
    for row in data:
        if row[col1] and row[col2]:
            row.append(float(row[col1]) * float(row[col2]))
    return data

def divide_columns(data, col1, col2):
    for row in data:
        if row[col1] and row[col2] and float(row[col2]) != 0:
            row.append(float(row[col1]) / float(row[col2]))
    return data

def performing_arithmetic_operations(input_file,method,columns,new_col,output_file):
    with open(input_file, 'r') as fi:
        reader = csv.reader(fi)
        header = next(reader)
        
        data = [row for row in reader]
        columns=columns.split(',')
        col1=header.index(columns[0])   
        col2=header.index(columns[1])
        
        if method == 'add':
            data=add_columns(data,col1,col2)
            print("Performing addition between {} and {} to {}.".format(columns[0],columns[1],new_col))
            
        elif method == 'sub':
            data=subtract_columns(data,col1,col2)
            print("Performing subtraction between {} and {} to {}.".format(columns[0],columns[1],new_col))
            
        elif method == 'mul':
            data=multiply_columns(data,col1,col2)
            print("Performing multiplication between {} and {} to {}.".format(columns[0],columns[1],new_col))
            
        elif method == 'div':
            data=divide_columns(data,col1,col2)
            print("Performing division between {} and {} to {}.".format(columns[0],columns[1],new_col))
            
        header.append(new_col) #Add new column to header
        
        with open(output_file, 'w', newline='') as fo:
            writer = csv.writer(fo)
            writer.writerow(header)
            writer.writerows(data)
        
def main():
    #Create an argument parser
    parser = argparse.ArgumentParser(description='Process CSV files with missing values')

    #Add command line arguments
    parser.add_argument('input_file', type=str, help='Path to input CSV file')
    parser.add_argument('--action', type=str, choices=['extract_columns', 'count_rows','fill_nan','del_rows','del_cols','drop_dup','normalize_num','performing_arithmetic'], help='Action to perform')
    parser.add_argument("--method", help="Method to use", choices=["mean", "median", "mode","min_max","zscore","add","sub","mul","div"])
    parser.add_argument("--column", help="Column(s) to use") ##for fuction 3,7
    parser.add_argument("--new_column", help="New column")
    parser.add_argument("--ratio", help="Max missing ratios for each row (between 0 and 1)") #for fuction 4,5
    parser.add_argument("--out", help="Output filename")

    #Parse the command line arguments
    args = parser.parse_args()

    #Call the appropriate function based on the action argument
    if args.action == 'extract_columns':
        extract_columns_with_missing_values(args.input_file)
    elif args.action == 'count_rows':
        count_missing_rows(args.input_file)
    elif args.action == 'fill_nan':
        fill_missing_values(args.input_file,args.method,args.column,args.out)
    elif args.action == 'del_rows':
        del_rows(args.input_file, float(args.ratio),args.out)
    elif args.action == 'del_cols':
        del_cols(args.input_file, float(args.ratio),args.out)
    elif args.action == 'drop_dup':
        drop_duplicate(args.input_file,args.out)
    elif args.action == 'normalize_num':
        normalize_numeric(args.input_file,args.method,args.column,args.out)
    elif args.action == 'performing_arithmetic':
        performing_arithmetic_operations(args.input_file,args.method,args.column,args.new_column,args.out)
    else:
        print("No action specified. Use --action to specify an action (extract_columns, count_rows,fill_nan,del_rows,del_cols,drop_dup,normalize_num,performing_arithmetic)")

if __name__ == '__main__':
    main()


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

5. Deleting columns containing more than a particular number of missing values 
(Example: delete columns with the number of missing values is more than 50% of the number of samples).

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