class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
class CircularLinkedList:
    def __init__(self):
        self.tail = None
    def is_empty(self):
        return self.tail is None
    def display(self):
        print("Playlist (CLL):")
        if self.is_empty():
            print("Empty")
        else:
            current = self.tail.next
            while True:
                print(current.data, "-> ", end="")
                current = current.next
                if current == self.tail.next:
                    print(current.data)
                    return
        
    def add_to_playlist(self, name):
        # You should write here appropriate statements to complete this function.
        # --------------------------------------------------------
        new_node = Node(name)
        if self.is_empty():
            self.tail = new_node
            self.tail.next = self.tail 
        else:
            new_node.next = self.tail.next 
            self.tail.next = new_node      
            self.tail = new_node
    
    def reverse(self):
        prev = self.tail
        current = self.tail.next
        head = self.tail.next
        while True:
            nextNode = current.next
            current.next = prev
            prev = current
            current = nextNode
            if current == head:
                break
        self.tail = head
    def remove(self, name):
        if self.is_empty():
            return
        current = self.tail
        while True:
            target = current.next
            if target == name:
                if target == current:
                    self.tail == None
                else:
                    if target == self.tail:
                        current.next = self.tail.next
                current.next = target.next
            current = current.next
            if current == self.tail:
                break
    def search(self, name):
        founds = []
        current = self.tail.next
        while True:
            if current.data.lower() == name.lower():
                founds.append(current.data)
            current = current.next
            if current == self.tail.next:
                break
        return founds
def main():
    cll = CircularLinkedList()
    cll.add_to_playlist("Sơn Tùng")
    cll.add_to_playlist("Jack - J97")
    cll.add_to_playlist("Kenzoyu")
    cll.add_to_playlist("Taylor")
    cll.add_to_playlist("Masew")
    cll.display()
    print(cll.search("sơn tùn"))
main()