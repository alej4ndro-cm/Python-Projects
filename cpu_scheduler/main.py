from process import Process
from mlfq import MLFQ
from fcfs import FCFS
from sjf import SJF

def create_processes():
    p1 = Process(1, [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4])
    p2 = Process(2, [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8])
    p3 = Process(3, [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6])
    p4 = Process(4, [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3])
    p5 = Process(5, [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4])
    p6 = Process(6, [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8])
    p7 = Process(7, [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10])
    p8 = Process(8, [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6])
    return [p1, p2, p3, p4, p5, p6, p7, p8]

def main():
    processes = create_processes()
    
    while True:
        print("\nSelect a scheduler:")
        print("1. MLFQ")
        print("2. FCFS")
        print("3. SJF")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            scheduler = MLFQ()
        elif choice == '2':
            scheduler = FCFS()
        elif choice == '3':
            scheduler = SJF()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
            continue
        
        for process in processes:
            process.parse()
            scheduler.add(process)
        
        scheduler.start()
        
        # Reset processes for next run
        processes = create_processes()

if __name__ == "__main__":
    main()