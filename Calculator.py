from tkinter import *

total_label_font = ("Times", 20)
current_label_font = ("Times", 40)
buttons_font = ("Times", 16)

buttons_height = 3
buttons_width = 6
buttons_bg = "#505050"


class Calculator():
    def __init__(self):
        self.window = Tk()
        self.window.geometry("375x667")
        self.window.resizable(False, False)
        self.window.config(bg="black")
        self.window.title("Calculator")

        self.total_expression = ""
        self.current_expression = ""
        self.total_label = self.create_total_label()
        self.current_label = self.create_current_label()

        self.digits = {  '7': (0,0), '8': (0,1), '9': (0,2),
                    '4': (1,0), '5': (1,1), '6': (1,2),
                    '1': (2,0), '2': (2,1), '3': (2,2),
                    '0': (3,0), '.': (3,1)}

        self.operations = { '*': (0,3),
                            '-': (1,3),
                            '+': (2,3),
                            '/': (3,3)}

        self.other = { '=': (3,2),
                      'C': (4,0), '►': (4,1), 'x²': (4,2), '√x': (4,3)}
        self.other_commands = (self.solve, self.clear_labels, self.del_last, self.power, self.square_root)
        
        self.button_frame = Frame(self.window, relief=RAISED)
        self.create_digit_buttons()
        self.create_operations_buttons()
        self.create_other_buttons()
        self.binding_keys()
        self.button_frame.place(x=187, y=210, anchor=N)
        
        self.window.mainloop()
        
        
    def create_total_label(self):
        total_label = Label(self.window, text=self.total_expression,
                              font=total_label_font,
                              height=2, width=22, bg="#768271",
                              )
        total_label.place(x=187, y=20, anchor=N)
        return total_label
    
    def create_current_label(self):
        current_label = Label(self.window, text=self.current_expression,
                              font=current_label_font,
                              height=2, width=11, bg="#768271")
        current_label.place(x=187, y=70, anchor=N)
        return current_label
    
    
    def create_digit_buttons(self):
        for key,value in self.digits.items():
            Button(self.button_frame,
                   height=buttons_height, width=buttons_width,
                   bg=buttons_bg,
                   command=lambda digit=key: self.add_to_expression(digit),
                   text=key,
                   font=buttons_font).grid(row=value[0], column=value[1])
            
    def add_to_expression(self, digit):
        self.current_expression += str(digit)
        self.update_current_label()
            
            
    def create_operations_buttons(self):
        for key,value in self.operations.items():
            Button(self.button_frame,
                   height=buttons_height, width=buttons_width,
                   bg=buttons_bg,
                   command=lambda operator=key: self.append_operator(operator),
                   text=key,
                   font=buttons_font).grid(row=value[0], column=value[1])
            
    def append_operator(self, operator):
        self.current_expression += str(operator)
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_current_label()
           
            
    def create_other_buttons(self):
        i = 0
        for key,value in self.other.items():
            Button(self.button_frame,
                   height=buttons_height, width=buttons_width,
                   bg=buttons_bg,
                   command=self.other_commands[i],
                   text=key,
                   font=buttons_font).grid(row=value[0], column=value[1])
            i+=1
        
    def solve(self):
        self.total_expression += self.current_expression
        try:
            self.current_expression = str(eval(self.total_expression))
        except Exception:
            self.clear_labels
        self.total_expression = ""
        self.update_current_label()
        self.update_total_label()
       
    def clear_labels(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_current_label()
        self.update_total_label()
       
    def del_last(self):
        self.current_expression = self.current_expression[:-1]
        self.update_current_label()
        
    def power(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_current_label()
    
    def square_root(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_current_label()
               
    
    def update_total_label(self):
        if(len(self.total_expression) > 22):
            self.total_expression = self.total_expression[:-1] #last charcter is an operator
            self.solve()
        self.total_label.config(text=self.total_expression)
        
    def update_current_label(self):
        self.current_expression = self.current_expression[:12]
        self.current_label.config(text=self.current_expression)


    def binding_keys(self):
        for key in self.digits:
            self.window.bind("<KP_{}>".format(key), lambda event, digit=key: self.add_to_expression(digit)) #idk how to fix it so that 1-5 don't count as a mouse clicks
            
        for key in self.operations:
            try:
                self.window.bind("<{}>".format(key), lambda event, digit=key: self.append_operator(digit))
            except: # binding minus key is not working
                pass
            
        self.window.bind("<=>", lambda event: self.solve())
        self.window.bind("<c>", lambda event: self.clear_labels())

if __name__ == "__main__":
    calculator = Calculator()