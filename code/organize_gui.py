from Organize import * 
import os

def main():
    print('|-------------------------------------------------------------------------------|')
    print('|----------------------------- Organize files ----------------------------------|')
    print('|-------------------------------------------------------------------------------|\n')

    path = str(input("Enter a valid path or just type nothing to exit... "))

    if not os.path.isdir(path):
        print('Exiting...')
        exit()
        
    else:
        print('I Will Organize: ', path)
        print('\n********** Options **********')
        print('( 1 ) - Organize by extension')
        print('( 2 ) - Organize by size')
        print('( 3 ) - Organize by date')
        print('( 4 ) - Exit\n')

        option = int(input('Choose wisely: '))

        if option == 1:
            obj = organize_by_extension(path)
            obj.create_dirs()
            obj.move_dirs()
        elif option == 2:
            obj = organize_by_bytes(path)
            obj.create_dirs()
            obj.move_dirs()
        elif option == 3:
            obj = organize_by_date(path)
            obj.create_dirs()
            obj.move_dirs()
        else:
            print('Exiting!!!!')
            exit()

if __name__ == "__main__":
    main()
