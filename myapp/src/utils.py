import pandas as pd

def remove_duplicates(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Remove duplicates based on entire rows
    # df = df.drop_duplicates()

    # Alternatively, remove duplicates based on specific columns (e.g., 'id')
    df = df.drop_duplicates(subset=['id'])

    # Save the cleaned DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

    print(f"Duplicates removed and saved to '{file_path}'")

def main():
    choice = input("1) Remove Song Duplicates\n2) Remove Artist Duplicates?\nEnter Choice: ")
    if choice == "1":
        csv_path = "../data/songs_data.csv"
    elif choice == "2":
        csv_path = "../data/artists_data.csv"
    else:
        return
    remove_duplicates(csv_path)

if __name__ == "__main__":
    main()