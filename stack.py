class CharStackNode:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node


class CharStack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = CharStackNode(data, self.top)
        self.top = new_node

    def print_stack(self):
        self._print_stack(self.top)

    def _print_stack(self, top):
        help_ptr = top
        while help_ptr is not None:
            print(f"{help_ptr.get_data()}, ", end="")
            help_ptr = help_ptr.get_next()
        print()


# Create an instance of IntStack
stack = CharStack()

while True:
    print("1. Push")
    print("2. Print Stack")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        char = input("Enter the character to push: ")
        stack.push(char)
    elif choice == '2':
        stack.print_stack()
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please enter a valid option.")
